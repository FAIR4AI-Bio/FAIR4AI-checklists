# tests/

Reproducible tests for the FAIR4AI evaluation agent.

Two kinds of things are pinned down here:

1. **Cached metadata fixtures** — `example_inputs/example_metadata/<short_name>/` holds the
   metadata retrieved once (via the `retrieve-metadata` skill) for each example dataset, plus a
   `retrieval_manifest.json`. Committing these makes evaluations reproducible **without re-fetching
   from the network** — the evaluation reads from disk.
2. **A deterministic validation suite** — `test_example_outputs.py` checks that the committed
   example outputs in `example_outputs/` are structurally valid for the current **89-item**
   `CHECKLIST.csv` and that the scorer reproduces their stored scores.

The evaluation itself is produced by an LLM (a **Sonnet** sub-agent), so it is *not*
deterministic — the suite therefore asserts **invariants**, not exact statuses/scores. Regenerating
the outputs (step B below) is an agent-driven step; validating them (step C) is plain Python.

## What the suite checks (`test_example_outputs.py`)

For every `example_outputs/FAIR4AI_eval_*.json`:

- exactly **89** responses (one per checklist item), covering the 89 items **exactly once**;
- every response has exactly the **8 current fields** — `item`, `requirement_definition`, `status`,
  `evidence`, `notes`, `recommendation`, `fair_category`, `ai_fair_criteria` — and **none** of the
  dropped legacy fields (`section`, `sub_section`, `question`, `criteria`);
- every `status` ∈ `{meets, partial, does not meet, N/A}`;
- `fair_category` and `ai_fair_criteria` are copied **verbatim** from the item's `CHECKLIST.csv` row;
- `summary.fair4ai_scores.traditional_fair.overall` and `…ai_fair.overall` are present, non-null,
  and within `[0, 1]`;
- re-running `compute_fair4ai_scores.score_document()` **reproduces the stored scores exactly and
  emits no warnings** (guards against scorer regressions and stale/hand-edited score blocks).

It also guards against stale files: exactly **one** committed output per expected dataset
(`neon_beetles`, `img_tol_200m`).

## How to run

Stdlib only — **no pip, no venv**:

```bash
cd fair4ai-eval-agent
python -m unittest discover -s tests          # or: python tests/test_example_outputs.py
```

(Use `python`; on Windows fall back to `py -3`, never `python3`.)

## How to (re)generate the fixtures and outputs

These steps use LLM sub-agents on the **current Sonnet** model, so they are driven from a Claude
Code session (e.g. by asking the agent to run them), not from a plain shell.

**A. Refresh the cached metadata** (only when the upstream dataset metadata changes):
run the `retrieve-metadata` skill for each dataset in URL mode and save into
`example_inputs/example_metadata/<short_name>/`:

- `neon_beetles` — <https://data.neonscience.org/data-products/DP1.10022.001>
- `img_tol_200m` — <https://huggingface.co/datasets/imageomics/TreeOfLife-200M>

**B. Regenerate the evaluation outputs** from the cached metadata (no network):
run the `evaluate-dataset` skill in **local-path mode** with the dataset source pointed at
`example_inputs/example_metadata/<short_name>/`, using a Sonnet sub-agent. It rates all 89 items in
the current schema and writes `example_outputs/FAIR4AI_eval_<short_name>_<timestamp>.json`, then
scores it via:

```bash
python scripts/compute_fair4ai_scores.py example_outputs/FAIR4AI_eval_<short_name>_<timestamp>.json
```

Replace (don't accumulate) the prior output for that dataset so the "exactly one per dataset" check
holds.

**C. Validate** with `python -m unittest discover -s tests`.

## Notes

- The scorer's own math is unit-tested separately by `python scripts/compute_fair4ai_scores.py
  --selftest`; this suite tests the *committed example documents*, not the scoring formulas.
- If a test fails after a checklist edit, it usually means the outputs need regenerating (step B) so
  their `item` / `fair_category` / `ai_fair_criteria` values match the new `CHECKLIST.csv`.
