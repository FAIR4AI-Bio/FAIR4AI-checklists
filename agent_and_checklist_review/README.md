# Agent & Checklist Review

This folder is the in-repo home for the **persona/archetype-driven review of the FAIR4AI-Bio
checklist** and the ongoing iterations that refine the checklist, the rating rubric, and the
`fair4ai-eval-agent`. It was migrated here from a separate working directory so that the review
record lives alongside the agent and checklist it evaluates.

- **What is being reviewed:** the 96-item FAIR4AI-Bio AI-readiness checklist
  (`../fair4ai-eval-agent/CHECKLIST.csv`), its companion `RATING_RUBRIC.md`, and the
  `fair4ai-eval-agent` that applies them.
- **Running log:** [`progress.md`](progress.md) — the source of truth for iterations, decisions,
  proposals, and next steps. **Read it first.**

---

## The frame: the Question–Data–Model (Q–D–M) Triangle

A dataset's AI-readiness is **relational, not intrinsic** — it depends on the *Question* being
asked and the *Model* being used. The checklist evaluates the **Data** vertex: whether a dataset
*communicates* the metadata, provenance, structure, and access information an AI/ML user needs.
It is an **evaluation instrument, not a metadata template** — each item poses one assessable
question rated `meets | partial | does not meet | N/A`; it does not mandate a controlled
vocabulary (see `NOTES_AND_FUTURE_DIRECTIONS.md`, FD-1).

## What was done (the persona-driven review)

The analysis ran as an **iterate-and-re-score loop** in three phases
(see `NOTES_workflow.md` for the full method + a verbatim recreation prompt):

1. **Checklist review** — consolidate and clarify the checklist items.
2. **Persona / archetype development** — define 13 personas on a provider/vertex naming
   convention (**Q** question-centric, **D** data-centric, **M** model-centric, **B** balanced)
   that consolidate into **7 archetypes A1–A7** (A1 AI/ML Model Developer, A2 Applied
   Researcher/Model User, A3 Synthesis Scientist, A4 Data Steward/Information Manager, A5
   Conservation Practitioner, A6 Policy/Reporting User, A7 Educator/Student/Citizen Scientist).
   Persona **M3** *is* the `fair4ai-eval-agent` itself.
3. **Persona-driven evaluation** — score the checklist's coverage against A1–A7, producing a
   coverage matrix, gaps (G01–G15), prioritized recommendations (R1–R16), and a roadmap;
   then pilot the agent + reproducible scoring on real datasets.

The loop reframed the checklist as an *evaluation instrument* (2026-07-24), added a `FAIR4AI
category` mapping column and a deterministic 0–1 scoring tool (2026-07-26), and validated the
whole pipeline on a NEON Ground Beetles pilot. Full iteration history is in `progress.md` §
"Iteration log".

## Contents of this folder

| File | What it is |
|---|---|
| `personas_and_archetypes.md` | The 13 personas + 7 archetypes (A1–A7) — the personas/archetypes document |
| `gap_analysis_results.md` | The persona-review output: coverage matrix, gaps G01–G15, recommendations R1–R16, pilot |
| `NOTES_workflow.md` | How to (re)create the whole analysis; the recreation prompt; Google Sheet mirror link |
| `NOTES_AND_FUTURE_DIRECTIONS.md` | Out-of-scope ideas (FD-*) — gaps to *enable, not enforce* (FD-1: controlled ML-task vocabularies) |
| `progress.md` | **Running log** of reviews, decisions, proposals, and planned next steps |
| `snapshot/` | Point-in-time copies (see below) |

`snapshot/` holds the checklist and companion docs **as they stood at the persona review**
(`DRAFT AI-ready checklist_v20260726.csv`, `RATING_RUBRIC_v20260726.md`,
`CHECKLIST_OVERVIEW_v20260726.md`). These are frozen references — the **live, canonical** versions
that the agent actually reads are in `../fair4ai-eval-agent/` (`CHECKLIST.csv`, `RATING_RUBRIC.md`,
`CHECKLIST_OVERVIEW.md`). When the checklist or rubric changes, update those live files and log the
change in `progress.md`; the snapshot stays as the historical baseline.

## How to recreate the analysis

Follow `NOTES_workflow.md` (its final section contains the verbatim recreation prompt). In short:
feed the checklist snapshot + `RATING_RUBRIC` + `CHECKLIST_OVERVIEW` + `personas_and_archetypes.md`
to a review pass that scores checklist coverage against archetypes A1–A7 and emits an updated
`gap_analysis_results.md`. Reproducible scoring of a real dataset evaluation is done by the agent
repo's `../fair4ai-eval-agent/scripts/compute_fair4ai_scores.py`.
