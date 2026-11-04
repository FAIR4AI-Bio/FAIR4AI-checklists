# Plan — Fix subagent failures & make dataset evaluation cheaper/faster

**Date:** 2026-08-21 · **Branch:** `post-hdr2026-checklist-clean-up` · **Status:** ✅ **implemented
2026-08-21** — both scripts + tests written (23 tests green, all `--selftest` PASS), both skills
reworked, hygiene rule reworded, docs synced. Only §7 step 3's *live* end-to-end run remains (the
reconstruction test already proves output-equivalence offline). See `progress.md` §4f for the
implementation record.

**Goal (from Eric):** diagnose why evaluation sub-agents started failing after the CHECKLIST.csv
restructure (they worked before), and rework the workflow to use **fewer tokens**, run **faster**,
and **write the output JSON incrementally** so progress is visible and resumable.

**Approved architecture decisions:**
1. **Scaffold + rating-only merge** — two blessed, committed, stdlib, absolute-path scripts
   pre-fill the verbatim fields and merge the agent's judgments. The agent only produces ratings.
2. **Per-section incremental writes** — merge/write after each of the 9 `Broad categories`
   sections; the file grows section-by-section and a failure loses only one section.

---

## 1. Diagnosis — why sub-agents fail now (they didn't before)

Evidence-backed; the failure surfaces "at the write step" because the write *is* the oversized
payload. Four compounding causes:

1. **Context bloat from the new per-item `Scoring:` columns.** The pre-restructure checklist
   (`git show da71e5d^`) had **no** `Scoring:` columns — rating guidance lived only in
   `RATING_RUBRIC.md` (read once, shared). The restructured CSV adds
   `Scoring: Meets/Partial/Does Not Meet/NA` = **35.5 KB (~9k tokens)** of item-specific rubric
   text; the whole CSV is now **~78 KB (~20k tokens)**, all loaded into each sub-agent's context at
   Step 3.
2. **Monolithic single Write of all 89 responses (Step 6–7).** The entire `responses[]` array is
   emitted in **one Write tool call** — one very long, very large assistant turn. Now worse because
   each object also carries the longer verbatim `requirement_definition` (avg 134 chars × 89). A
   large `tool_use` payload generated over a long turn is exactly what triggers
   ECONNRESET / timeout / 403.
3. **Verbatim-transcription tax + the "no helper scripts" rule.** The skill forbids generator
   scripts (`evaluate-dataset/SKILL.md:55-58,273`), forcing the model to hand-copy four verbatim
   fields (`item`, `requirement_definition`, `fair_category`, `ai_fair_criteria`) for all 89 items —
   ~17 KB (~4.3k tokens) of pure output transcription with zero reasoning value, and the reason the
   last session abandoned the Sonnet sub-agents for an inline CSV-merge builder.
4. **No checkpointing.** If the giant turn dies, the whole evaluation is lost; retries restart from
   zero, multiplying the token/time cost.

### On the "no helper scripts" rule (why relaxing it is safe)

Introduced in commit **`ad18c4d`** ("Add file-hygiene rule to prevent sub-agents polluting the
repo/workspace"). The real problem it fixed: sub-agents **authored ad-hoc generator scripts that
read `CHECKLIST.csv` by a bare relative path** and, with cwd in the source tree, wrote the script
and its JSON into the wrong place, leaving stray `eval_*.py` / orphan `*_evaluation.json`. The rule
bundles two concerns: **(1) location discipline** (never write outside the run folder; absolute
paths; never touch `fair4ai-eval-agent/`) — the genuine intent — and **(2) a blanket "no scripts"**,
which was only the enforcement mechanism. The skill already sanctions invoking one committed script
every run (`compute_fair4ai_scores.py`). Adding two more **committed, stdlib, absolute-path** scripts
is the opposite of the ad-hoc/relative-path/cwd-dependent generators the rule targeted, so it does
**not** reopen that hole. We relax only (2), for two named scripts; all of (1) stays intact and the
agent still may not author its own scripts.

---

## 2. New scripts (stdlib-only, committed in `scripts/`, absolute-path args)

### `scripts/build_response_scaffold.py`
- **Input:** `--checklist <abs CHECKLIST.csv>`, `--out <abs scaffold.json path in run folder>`,
  plus session fields (dataset title/urls/evaluator) via `--session-json <abs path>` or flags.
- **Output:** a full evaluation document with:
  - `session` populated from the passed values (unknowns → `null`);
  - `responses[]` = **89 objects in CSV order**, each with `item`, `requirement_definition`,
    `fair_category`, `ai_fair_criteria` **copied verbatim from the CSV** and
    `status`/`evidence`/`notes`/`recommendation` set to `""` (pending);
  - `summary` skeleton with `fair4ai_scores: {}`.
- **Also emits a compact rating guide to stdout** (`--emit-guide`): per section (`Broad
  categories`), the items with only their `Item`, `Requirement Definition`, four `Scoring:` cells,
  `FAIR category`, `AI FAIR Criteria`, and `Note`. This is what the agent reads for rating — so the
  full 78 KB CSV (incl. the ~12.5 KB of `mapped*` / `Croissant` / `Sub category` columns irrelevant
  to scoring) never enters the reasoning context.
- Verbatim fields become **correct-by-construction** → the `tests/` verbatim check passes
  automatically.

### `scripts/merge_ratings.py`
- **Input:** `--scaffold <abs scaffold.json>`, `--ratings <abs ratings.json>` (a list of
  `{item, status, evidence, notes, recommendation}` — a **partial** batch is fine).
- **Behavior:** merge by exact `item` match, in place. **Validates:** every rated `item` exists in
  the scaffold (reject unknown/misspelled items — this catches transcription drift), `status ∈
  {meets, partial, does not meet, N/A}`; leaves un-rated items pending. **Idempotent** and
  order-independent so it can run once per section.
- Prints a one-line progress summary: `merged <k> ratings; <n>/89 items now rated`.

---

## 3. Rework `evaluate-dataset/SKILL.md`

- **Step 3 (load checklist):** stop reading the raw CSV into context. Run
  `build_response_scaffold.py` to (a) write the scaffold JSON into the run folder and (b) obtain the
  compact per-section rating guide; the agent reasons from the guide, not the 78 KB CSV.
- **Step 4 (metadata):** read the metadata **once** and keep it in context across all sections; do
  **not** re-read raw EML/JSON-LD per section. (Fixtures already cached from last session.)
- **Step 5 (evaluate):** rate **one `Broad categories` section at a time**. For each section, emit a
  compact ratings batch (`item → {status, evidence, notes, recommendation}`) and immediately run
  `merge_ratings.py` to write those into the on-disk scaffold. Repeat for all 9 sections. Rubric
  logic (per-item `Scoring:` cells authoritative; N/A rule; blended-criteria "take the lower";
  conditional-disclosure polarity) is unchanged — only the batching and the fact that verbatim
  fields are pre-filled change.
- **Step 6 (build JSON):** the scaffold already carries the schema; the agent no longer transcribes
  verbatim fields. The `responses[]` schema and the 8-field contract are unchanged.
- **Step 7 (score & report):** after the last section merges, run `compute_fair4ai_scores.py` on the
  file, resolve any `WARNING:`, then report. Reporting unchanged.
- **Resume:** on re-invocation over an existing run folder, read the scaffold, find responses with
  empty `status`, and rate only those sections (dovetails with the batch coordinator's resume).

## 4. Rework the hygiene rule wording (both `evaluate-dataset` and `batch-evaluate-datasets`)

Keep **all** location discipline. Change only the "no scripts" clause to:

> *You may invoke the committed helper scripts in `scripts/` (`build_response_scaffold.py`,
> `merge_ratings.py`, `compute_fair4ai_scores.py`) with the **absolute paths** given. You may **not**
> author your own scripts, read `CHECKLIST.csv` by a bare relative name, `cd` into the agent source
> tree, or write any intermediate/renamed JSON or scratch file. Your only writes are inside the run
> folder.*

Update `batch-evaluate-datasets/SKILL.md:134-143` to state the same, and note the scaffold/merge
scripts write **only** into the run folder (they take an absolute `--out`/`--scaffold` in
`evaluation_results/`).

## 5. Docs, tests, tracking

- **Docs:** `CLAUDE.md` (Scripts section + workflow), `QUICKSTART.md` (Files-involved + flow),
  `tests/README.md` (regeneration steps B now = scaffold → per-section merge → score).
- **Tests (`tests/`):** add `test_scaffold_and_merge.py` — (a) scaffold produces 89 responses with
  verbatim fields matching the CSV and empty ratings; (b) merge rejects unknown items and invalid
  statuses; (c) merge is idempotent and supports partial/section batches; (d) scaffold + full merge
  → a doc that passes the existing `test_example_outputs.py` invariants. Existing 10 tests must stay
  green.
- **Tracking:** append an **Iteration 10** row to `progress.md` (diagnosis + scaffold/merge +
  per-section incremental + hygiene-rule relaxation).

---

## 6. Expected wins

- **Output tokens:** ~4.3k/dataset of verbatim transcription eliminated (scaffold fills it).
- **Input tokens:** ~3k/dataset saved by feeding the compact guide instead of the 78 KB CSV
  (drops the ~12.5 KB of `mapped*`/`Croissant`/`Sub category` columns from reasoning context).
- **Reliability:** no single giant Write — the largest turn is now one section (~10 items), well
  under the payload/turn-length that was triggering ECONNRESET/403.
- **Time & resumability:** per-section merges checkpoint progress; a failure re-rates one section,
  not all 89, and the file is watchable as it fills.

## 7. Verification (after implementation)

1. `python scripts/build_response_scaffold.py … --emit-guide` → 89 pending responses, verbatim
   fields exact; guide omits `mapped*`/`Croissant`/`Sub category`.
2. `python scripts/merge_ratings.py …` on a partial batch → correct count, rejects a bad item and a
   bad status.
3. Re-run **both cached fixtures** through the new scaffold→section-merge→score flow; outputs match
   the current committed scores (or diffs are explained), `--selftest` PASS, `tests/` green
   (existing 10 + new scaffold/merge tests).
4. Grep the skills for any lingering "build the JSON yourself / do not author a generator script"
   wording that contradicts the relaxed rule.
