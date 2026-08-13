# FAIR4AI-Bio Checklist & Agent — Review Progress

*Living document. The running record of how the checklist, the rating rubric, and the
`fair4ai-eval-agent` have been reviewed and updated. Update it at the end of every review pass,
checklist edit, and scoring change. Read it first.*

**Maintainer:** Eric Sokol · **Home:** `FAIR4AI-checklists/agent_and_checklist_review/`
**Live artifacts under review:** `../fair4ai-eval-agent/CHECKLIST.csv`,
`../fair4ai-eval-agent/RATING_RUBRIC.md`, `../fair4ai-eval-agent/scripts/compute_fair4ai_scores.py`
**Frozen baseline:** `snapshot/` (checklist + rubric + overview as of the persona review, v20260726)

---

## 1. How the work runs

An **iterate-and-re-score loop** (see `NOTES_workflow.md`): update the checklist/rubric → re-run
the persona/archetype-driven review → apply/decide on recommendations → repeat. The checklist is
an **evaluation instrument, not a metadata template**: each item poses one assessable question
rated `meets | partial | does not meet | N/A`, scored `1 / 0.5 / 0 / excluded`. The organizing
frame is the **Question–Data–Model (Q–D–M) Triangle**; the checklist evaluates the **Data** vertex.

Two assessments are computed deterministically by `compute_fair4ai_scores.py`:
- **Traditional FAIR** (from `FAIR category`): findable / accessible / interoperable / reusable.
- **AI-FAIR** (from `Criteria`): `ml_ready` (structural), `ai_ready_for_task` (structural+scientific),
  `traceable` (provenance+structural), `care_compliance` (governance).

---

## 2. Iteration log

*(Iterations 1–6 seeded from the pre-migration working tracker; see `gap_analysis_results.md`
for the full gap/recommendation detail those iterations produced.)*

| # | Checklist in → out | Driven by | What happened | Status |
|---|---|---|---|---|
| 1 | v20260722 → v20260723 | gap analysis 2026-07-23 | R1–R5 (P0) applied by build script + 2 consolidation fixes; 106→97 rows | ✅ |
| 2 | v20260723 → **v20260724** | Eric's manual review | Reframed as *evaluation instrument, not metadata template*; reverted R2 structured defs; **dropped** the controlled-vocab / severity / example columns; 25→15 cols | ✅ |
| 3 | v20260724 (no CSV change) | formalize rubric | Authored `RATING_RUBRIC.md` (meets/partial/does-not-meet/N/A levels, N/A rule keyed to `Use-case scope`, per-criteria guidance) | ✅ |
| 4 | v20260724 + rubric | re-run gap analysis | Re-scored against archetypes A1–A7; appended Current-State banner + §8 to `gap_analysis_results.md`; verdict → 🟡 pilot-ready | ✅ |
| 5 | v20260724 → **v20260726** (+ agent sync + pilot) | reproducible scoring (R14, R16) | Added `FAIR4AI category` column (16th); built deterministic `compute_fair4ai_scores.py` + `fair4ai-scoring` skill; synced agent repo; NEON Ground Beetles pilot (96 items; overall 0.733, AI-ready 0.556) | ✅ |
| 6 | v20260726 (no CSV change) | repo clean-up | Aligned rubric labels to the agent's 4 machine statuses; consolidated skills under `.claude/skills/`; single current-format example output | ✅ |
| 7 | **CHECKLIST.csv** (this repo) | **Governance→Criteria + review scaffolding** (2026-08-07) | **(a)** Migrated the persona review into this folder. **(b)** Moved **Governance** into the `Criteria` column: renamed the header to `Criteria: Structural/Scientific/Provenance/Governance` and appended `/Governance` to the 5 governance rows (kept the `Governance` Broad-category section). **(c)** Rewired `compute_fair4ai_scores.py` so `care_compliance` reads governance from `Criteria` (union with the `Governance` section as a backward-compatible fallback); `--selftest` PASS; both example outputs re-score identically (AI-FAIR 0.746 / 0.603, care 0.5 / 0.3). **(d)** Updated `RATING_RUBRIC.md` (§4d + §6), `CLAUDE.md`, `CHECKLIST_OVERVIEW.md`, `README.md`, and both skills. **(e)** Logged the review proposals below (§3–§5). | ✅ applied + proposals logged |
| 8 | **CHECKLIST.csv** 16→15 cols (this repo) | **Apply reviewed proposals 4a–4c + full scorer refactor** (2026-08-12) | **(A)** Reworded items 72/73 as conditional disclosure **statements** (good state = `meets`/`N/A`, never `does not meet` for a clean dataset); **(B)** added 72/73 as worked **N/A** examples in `evaluate-dataset/SKILL.md`. **(C)** Filled/re-tagged `Criteria`: 9 *Keywords/Tags*→`Structural/Scientific`, 17 *Related paper*→`Scientific/Provenance`, 47 *controlled vocabulary*→`Structural`, 42 *Labeling*→`Scientific/Provenance` (left 60 *Reporting Issues* as `Provenance`). **(D/P1)** Dropped the sparse `use case` column (folded 7 notes into `Note`), 16→15 cols. **(E/P3-P4)** Canonicalized every blended `Criteria` to **Structural<Scientific<Provenance<Governance**; `Data structure`→`Data Structure`. **(F/P5)** Filled the one blank `Required` (*Preparation*→`core`). **(G/P2)** Renamed column `FAIR4AI category`→`FAIR category`, removed the dead `AI-ready` token, audited all 96 FAIR mappings (21 carried `AI-ready`: 6 kept another dim, 11 retagged `Reusable`, 4 left blank as pure-ML). **Refactored the scorer**: renamed JSON field `fair4ai_category`→`fair_category`, removed legacy AI-ready code, hardened exception handling, updated `--selftest` (PASS). Synced all docs/skills/rubric. Example outputs pending regeneration (old field name superseded). | ✅ applied (examples pending regen) |

---

## 3. Iteration 7 — applied change: Governance is now a Criteria facet

**Decision (with Eric):** *add facet, keep section.* Governance joins Scientific / Structural /
Provenance as a 4th `Criteria` value. The 5 governance rows keep their existing facets
(`Provenance` → `Provenance/Governance`; row 94 `Provenance/Scientific` → `Provenance/Scientific/Governance`)
so they still feed the provenance / traceable facets, and they remain in the `Governance` Broad
category. The scorer treats an item as governance if its `criteria` includes `Governance` **or**
(fallback) its `section` is `Governance` — so old evaluation JSONs still score `care_compliance`.

Files changed: `CHECKLIST.csv`, `scripts/compute_fair4ai_scores.py`, `RATING_RUBRIC.md`,
`CLAUDE.md`, `CHECKLIST_OVERVIEW.md`, `README.md`,
`.claude/skills/evaluate-dataset/SKILL.md`, `.claude/skills/fair4ai-scoring/SKILL.md`.

---

## 4. Proposals — pending review (not yet applied)

Status legend: 🔲 proposed · ✅ applied · ⏭️ deferred. **Metadata mappings
(`mappedEML`/`mappedDataCite`/`mappedSOSO`/`mappedCroissant` + `Croissant scope`) are explicitly
out of scope for reduction — keep them.**

### 4a. Other categorical columns vs. the scoring rubric (Part 2b)

| ID | Column / issue | Observation | Proposal | Status |
|---|---|---|---|---|
| P1 | `use case` (col 9) | Only 7 of 96 rows filled; holds long prose that overlaps `Use-case scope (Condition)` | Remove the column (or fold the 7 annotations into `Note`). Not read by the scorer. | ✅ Iter 8 — folded 7 into `Note`, column dropped (16→15 cols) |
| P2 | `FAIR4AI category` — `AI-ready` token | The `AI-ready` token is **ignored** by the Traditional-FAIR scorer (AI-readiness is now the AI-FAIR assessment) — 15 items are tagged only `AI-ready`, so they feed **no** Traditional-FAIR dimension | Deprecate/remove the `AI-ready` token and re-map those 15 items to the FAIR dimension(s) they actually serve (most are Reusable/Interoperable), so no item is a no-op for Traditional FAIR | ✅ Iter 8 — column renamed `FAIR category`, token removed, all 96 audited (see 4d); JSON field also renamed `fair_category` + scorer refactored |
| P3 | Blended-value order | `Structural/Scientific` (9) vs `Scientific/Structural` (10); `Provenance/Structural` (8) vs `Structural/Provenance` (2) | Canonicalize token order (scorer is order-insensitive, so purely cosmetic/readability) | ✅ Iter 8 — canonical **Structural<Scientific<Provenance<Governance** |
| P4 | Capitalization | `Broad categories` value `Data structure` vs "Data Structure" heading in `CHECKLIST_OVERVIEW.md` | Normalize to `Data Structure` | ✅ Iter 8 — normalized; matches overview `## 2. Data Structure` |
| P5 | Blank cells | `Criteria` blank on rows 9 (*Keywords/Tags*) & 17 (*Related paper*); 1 blank `Required` row | Fill (see 4b for the Criteria proposals) | ✅ Iter 8 — 9/17 filled (4b); blank `Required` (*Preparation*) → `core` |
| P6 | Governance section membership | Rows 94–95 (*Timestamp of observation*, *Action and timestamp taken towards observation*) sit in the `Governance` section but have `Sub category = Collection` | Review whether these belong in Governance or in Provenance/Collection; they now carry the `Governance` Criteria token regardless | ✅ Iter 8 — **kept** in Governance (Eric); `Criteria` carries Provenance+Governance (94 `Scientific/Provenance/Governance`, 95 `Provenance/Governance`) |

### 4b. Criteria categorization audit (Part 3a)

Reviewed all 96 items' `Criteria` against their definitions and the rubric §4 facet meanings.
The checklist is largely sound; candidates that look mis-tagged:

| Item | Current | Proposed | Rationale | Confidence |
|---|---|---|---|---|
| 9 *Keywords/Tags* | *(blank)* | `Structural/Scientific` | Machine-discoverable descriptors — a structural/findability facet; blank feeds no AI-FAIR facet today | high |
| 17 *Related paper* | *(blank)* | `Provenance/Scientific` | Links to related literature — matches item 14 *Paper* and 16 *Related dataset* (both `Provenance/Scientific`) | high |
| 47 *controlled vocabulary* | `Scientific/Structural` | `Structural` | Controlled vocab is primarily machine-actionable/interoperable; the scientific facet is weak | medium |
| 42 *Labeling/re-labeling* | `Scientific` | `Scientific/Provenance` | *Who* labeled and *how* is annotation provenance as much as scientific content | medium |
| 60 *Reporting Issues* | `Provenance` | `Scientific` or leave | A feedback/roundtripping mechanism rather than origin/rights; provenance is a stretch | low |

**✅ Applied in Iteration 8:** 9, 17 (canonicalized to `Scientific/Provenance`), 47, and 42.
**Item 60 left as `Provenance`** per Eric (low-confidence proposal declined).

### 4c. Scoring-polarity audit — "meets" must always raise the score (Part 3b)

**Goal:** every item is phrased so `meets` → good/present (raises FAIR & AI-FAIR) and
`does not meet` → gap/bad (lowers it). An item must never be a yes/no *fact about a bad condition*,
or a well-behaved dataset scores 0 on it.

**Two confirmed reversed items** (from the last evaluation round; the NEON beetles vs TOL-200M
example outputs make the reversal concrete):

| Item | FAIR4AI | What went wrong |
|---|---|---|
| 72 *Personal and Sensitive Information* | `Accessible \| Reusable` | NEON beetles (**no** sensitive data — a good state) was rated `does not meet` → 0, dragging Accessible/Reusable down; TOL-200M (documented) → `meets`. Opposite datasets, opposite polarity. |
| 73 *Restricted Data Access* | `Accessible` | NEON beetles (**openly** accessible — a good state) → `does not meet` → 0, dragging Accessibility down; TOL-200M → `meets`. |

**Root cause & fix.** The rubric §3 *already* says these items are **`N/A`** when the dataset has
no sensitive content / no access restriction — the failure was the agent rating them
`does not meet` instead. Two coordinated fixes:
1. **Reword items 72 & 73 as disclosure-quality**, following the pattern of item 74 *Secure Access*
   (which was correctly `N/A` in both example runs): e.g. *"If the dataset contains personal or
   sensitive content, is its presence and handling documented?"* and *"If access is restricted,
   are the conditions of access documented?"* — so the good state is `meets`/`N/A`, never
   `does not meet`.
2. **Reinforce the N/A rule in `evaluate-dataset/SKILL.md`** with these two as worked examples, so
   the absence of a bad condition routes to `N/A` (removed from the denominator), not `does not meet`.

**Swept and found correct (no change needed):** items 50 *Bias*, 51 *Risks*, 52 *Limitations*
(scope `All use cases`) are genuine **disclosure** items — `meets` = the bias/limitation is
disclosed, which correctly *raises* the score. Items 39 *Data Anonymization*, 40/41
*null values/gapfilling*, 42 *Labeling*, 43 *Outlier removal*, 44 *Splits*, 53 *Experimental*
are disclosure items with conditional scopes that already trigger `N/A` correctly; they need the
same N/A discipline as 72/73 but no rewording.

**✅ Applied in Iteration 8.** Items 72 & 73 reworded as conditional disclosure **statements**
(good state = `meets` when documented, `N/A` when the dimension is absent, never `does not meet`
for a clean dataset), mirroring item 74 *Secure Access*. Both added as worked **N/A** examples in
`evaluate-dataset/SKILL.md` (the belt-and-suspenders half). Verification (Task 5) confirms NEON
beetles now returns `N/A` on both.

---

## 4d. Iteration 8 — P2 FAIR-category audit: flagged mappings for Eric

All 96 `FAIR category` mappings were audited after removing the dead `AI-ready` token. **75 items
kept their mapping; 21 carried `AI-ready`** and were dispositioned: **6** dropped `AI-ready` while
keeping their other dimension (*Purpose, Is machine ready, Features, Sensor Metadata, resolution
information, Reporting Issues*); **11** retagged from AI-ready-only → `Reusable`; **4** left **blank**
as pure-ML concepts (no Traditional-FAIR home). The items below are **judgment calls — please
confirm or override:**

| Item | Iter-8 mapping | Question for Eric |
|---|---|---|
| *Is machine ready (IO/ESIP)* | `Interoperable` | "Ready to insert into an ML pipeline" is arguably pure AI-readiness — leave `Interoperable`, or blank? |
| *Is task ready (list of tasks)* | *(blank)* | Pure-ML "engineered-for tasks" — confirm no FAIR home. |
| *Splits* | *(blank)* | Train/val/test — confirm pure-ML, blank. |
| *Supported ML Tasks* | *(blank)* | Pure-ML — confirm blank. |
| *Benchmark / Leaderboard results* | *(blank)* | Pure-ML — confirm blank. |
| *Have null values/gaps been filled?* · *Is the gapfilling method described?* · *Labeling/re-labeling* | `Reusable` | Retagged from AI-ready → Reusable as processing/annotation **disclosure** items; OK? |
| *Bias* · *Risks* · *Limitations* | `Reusable` | Disclosure items needed for responsible reuse — confirm `Reusable`. |
| *Is it experimantal data* · *if yes, design description* | `Reusable` | Experimental-design disclosure → `Reusable`; or treat as ML-only (blank)? |
| *Usage Guidelines - Recommendations* · *Usage Recommendations: Out-of-Scope* | `Reusable` | Controlled-vocab ML-task guidance → `Reusable`; or blank? |
| *AI/ML Usage History* | `Reusable` | Prior-use links → `Reusable`; consider adding `Findable`? |
| *Repository (IO)* | `Findable` (unchanged) | Points to a curation/processing toolbox — may fit `Reusable`/`Accessible` better. |
| *Technical specs* | `Interoperable` (unchanged) | `Interoperable` is a weak fit for file/dataset size — consider `Accessible`/`Reusable`. |
| *collection date or date range* | `Reusable` (unchanged) | Near-duplicate of *date created* (`Findable \| Reusable`) — add `Findable` for consistency? |
| *Multiple Formats* | `Accessible` (unchanged) | Availability in multiple formats may also warrant `Interoperable`. |
| *Source data checksums* · *checksums (of full, images, etc.)* | `Reusable` (unchanged) | Integrity checksums — could also be `Interoperable`/`Accessible`; confirm consistent treatment. |
| *Storage Conditions* · *Permission to take observations* · *Agent granting permission* · *People stewarding observations* · *Action and timestamp taken towards observation* | `Reusable` (unchanged) | Governance/CARE items score via `care_compliance` (AI-FAIR); confirm you still want them counting toward `Reusable` in Traditional FAIR (vs. blank). |

Also flagged: **P5 blank `Required`** was filled *Preparation* → `core` (inferred from its Source-Data
siblings, which are all `core`); confirm the tier.

---

## 5. Planned next steps

1. **Confirm the Iteration-8 flagged mappings** (§4d) — Eric to accept/override the ~20 judgment-call
   `FAIR category` mappings and the *Preparation* `Required` tier.
2. **Archetype-driven review round** (scaffolded below) — the next major pass. Re-run against the
   **regenerated** example outputs (which now carry `fair_category` and the 72/73 `N/A` fix).
3. Sync the updated checklist into the Google Sheet mirror (link in `NOTES_workflow.md`).
4. Revisit FD-1 (controlled ML-task/use vocabularies) as a deferred future direction.
5. Scope P1 gaps R6–R9 (sensor block, taxonomic backbone, sampling design, record-level
   annotation provenance) as new rated criteria.

### Next round (scaffold) — Archetype-driven review of the checklist + rubric

*Goal:* re-review the (updated) checklist and rubric from the perspective of the 7 archetypes
(A1–A7 in `personas_and_archetypes.md`), using the two example evaluation outputs as concrete
evidence of how the current instrument behaves. To be run in a later session.

**Inputs:** `../fair4ai-eval-agent/CHECKLIST.csv` + `RATING_RUBRIC.md`; the example outputs
`../fair4ai-eval-agent/example_outputs/FAIR4AI_eval_neon_beetles_*.json` and
`…_img_tol_200m_*.json`; `personas_and_archetypes.md`; `gap_analysis_results.md` (baseline coverage).

**Method (outline):**
1. **Map archetypes → score categories.** For each archetype A1–A7, state which AI-FAIR categories
   (`ml_ready`, `ai_ready_for_task`, `traceable`, `care_compliance`) and Traditional-FAIR dimensions
   matter most (e.g. A1 AI/ML Model Developer → ml_ready + ai_ready_for_task; A4 Data Steward →
   traceable + care_compliance; A5 Conservation Practitioner → care_compliance + reusable).
2. **Read the two example outputs through each archetype's lens.** Do the per-item statuses and the
   rolled-up scores tell that archetype what it needs? Where does a `meets` mislead, or a gap not
   surface? (Feed the 4c polarity findings back in — did reversed items distort an archetype's read?)
3. **Per-archetype gap pass.** Identify checklist items missing or mis-weighted for each archetype;
   check whether the new Governance/Criteria facet improved A4/A5 coverage.
4. **Emit proposals** — concrete checklist/rubric edits (new items, re-tags, rubric clarifications),
   appended here as the next iteration and cross-referenced into `gap_analysis_results.md`.
