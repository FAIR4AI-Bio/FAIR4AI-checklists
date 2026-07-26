# FAIR4AI Dataset Evaluation Agent

An AI agent that evaluates biodiversity, ecology, and environmental science datasets for AI-readiness using the **FAIR4AI-Bio checklist**. The agent reads a dataset's landing page or local metadata files, rates each of the 96 checklist items as *meets / partial / does not meet / N/A* (per `RATING_RUBRIC.md`), and produces a structured JSON report with reproducible FAIR4AI scores across five dimensions (Findable, Accessible, Interoperable, Reusable, AI-ready) plus an overall score — each in **0–1, where 1 is "most FAIR4AI"**, computed by the `fair4ai-scoring` skill.

The core thesis: **FAIR compliance is necessary but not sufficient for AI-ready data.** This agent surfaces the gap.

See `example_outputs/` for complete evaluation reports for two NEON datasets.

---

## Requirements

- A dataset source: URL to a landing page, or a local directory containing metadata files (JSON-LD, EML, DataCite XML, README, etc.)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed

---

## Setup

Open Claude Code with `fair4ai-eval-agent/` as the working directory:

```bash
cd fair4ai-eval-agent
claude
```

No additional setup steps are required. The `/evaluate-dataset` command is defined in `.claude/commands/evaluate-dataset.md` and is tracked in this repository.

In the Claude Code chat, type:

```
/evaluate-dataset
```

The agent will prompt you for the dataset source and other parameters. Press Enter to accept defaults for optional parameters.

---

## How the agent files work

Claude Code reads these files automatically when you start a session in this directory:

- **`CLAUDE.md`** — project context loaded into every session: what the agent does, how the checklist is structured, the output JSON schema, and expected score patterns.
- **`.claude/commands/evaluate-dataset.md`** — defines the `/evaluate-dataset` slash command. Contains the step-by-step evaluation workflow: gather parameters, load the checklist, fetch metadata, rate each item, build the output JSON, and compute scores.
- **`RATING_RUBRIC.md`** — the authority for how each item's `meets / partial / does not meet / N/A` status is chosen (including the N/A rule).
- **`.claude/skills/fair4ai-scoring/`** + **`scripts/compute_fair4ai_scores.py`** — the skill and deterministic tool that compute `summary.fair4ai_scores` (0–1) from the per-item statuses and each item's `FAIR4AI category`.

To modify agent behavior, edit these files directly. Changes are tracked in git and shared across the team.

---

## Output format

The JSON report has three top-level sections:

- **`session`** — evaluation date, AI model, metadata sources used, dataset identity (title, DOI, landing page URL, citation), and evaluator information
- **`responses`** — one object per checklist item with `section`, `sub_section`, `question`, `status` (`meets` / `partial` / `does not meet` / `N/A`), `evidence`, `notes`, `recommendation`, and `fair4ai_category` (the dimension(s) the item counts toward)
- **`summary`** — `strengths`, `gaps`, `overall_assessment` (2–3 sentence narrative), and `fair4ai_scores` (each dimension plus an overall score in 0–1, with per-dimension `details` counts) computed by the `fair4ai-scoring` skill

Output filename convention: `FAIR4AI_eval_<dataset-name>_<YYYY-MM-DD>.json`

See `example_outputs/` for complete examples.

---

## Files in this directory

| File | Description |
|------|-------------|
| `CLAUDE.md` | Project context auto-loaded by Claude Code each session |
| `.claude/commands/evaluate-dataset.md` | Defines the `/evaluate-dataset` slash command and evaluation workflow |
| `CHECKLIST.csv` | 80-item FAIR4AI-Bio checklist (8 sections, mapped to EML, DataCite, Schema.org, Croissant) |
| `CHECKLIST_OVERVIEW.md` | Narrative description of all 8 checklist sections |
| `QUICKSTART.md` | Step-by-step usage guide with example sessions |
| `example_outputs/` | Complete evaluation reports for two NEON datasets |

---

## Checklist sections

1. **General Information** — bibliographic metadata, data dictionary, machine-readiness flag
2. **Data Structure** — file formats, dataset organization, variables, technical specs
3. **Source Data** — collection type, instrumentation/sensor metadata, sampling design
4. **Data Processing** — transformations, gap-filling, annotation provenance, train/val/test split definitions
5. **Data Quality** — completeness, consistency, integrity, timeliness
6. **Guidance & Recommendations** — biases, class imbalance, non-detections, prior AI/ML usage history
7. **Data Access** — delivery options, format openness, license (SPDX identifier), privacy controls
8. **Provenance** — citation (DOI, ORCIDs, checksums), processing platform, CARE Principles and ethical governance
