# FAIR4AI Dataset Evaluation Agent

An AI agent that evaluates biodiversity, ecology, and environmental science datasets for AI-readiness using the **FAIR4AI-Bio checklist**. The agent reads a dataset's landing page or local metadata files, scores each of ~80 checklist items as *meets / partial / does not meet / N/A*, and produces a structured JSON report with FAIR4AI scores across five dimensions (Findable, Accessible, Interoperable, Reusable, AI-ready — each out of 10).

The core thesis: **FAIR compliance is necessary but not sufficient for AI-ready data.** This agent surfaces the gap.

See `example_outputs/` for complete evaluation reports for two NEON datasets.

---

## Requirements

- A dataset source: URL to a landing page, or a local directory containing metadata files (JSON-LD, EML, DataCite XML, README, etc.)
- Access to **Claude Code**, **GitHub Copilot Chat**, or **ChatGPT**

---

## Setup: Claude Code

Run these commands once from the **root of this repository**:

```bash
mkdir -p fair4ai-eval-agent/.claude/commands
cp fair4ai-eval-agent/skills/evaluate-dataset.md \
   fair4ai-eval-agent/.claude/commands/evaluate-dataset.md
```

Then open Claude Code with `fair4ai-eval-agent/` as the working directory:

```bash
cd fair4ai-eval-agent
claude
```

In the Claude Code chat, type:

```
/evaluate-dataset
```

The agent will prompt you for the dataset source and other parameters. Press Enter to accept defaults for optional parameters.

> **Note:** `.claude/` is in `.gitignore` — this setup step is local only and will not be committed to the repository.

---

## Setup: GitHub Copilot

Run these commands once from the **root of this repository**:

```bash
mkdir -p fair4ai-eval-agent/.github
cp fair4ai-eval-agent/skills/evaluate-dataset.md \
   fair4ai-eval-agent/.github/copilot-instructions.md
```

Open the `fair4ai-eval-agent/` folder in VS Code. GitHub Copilot Chat will automatically apply the instructions from `.github/copilot-instructions.md`.

Start a Copilot Chat session and provide the parameters in natural language, following the format in `QUICKSTART_evaluate-dataset.md`. For example:

> "Please evaluate this dataset for AI-readiness using the FAIR4AI-Bio checklist. The dataset source is https://data.neonscience.org/data-products/DP1.10022.001. Use CHECKLIST.csv as the checklist file and save the output as FAIR4AI_eval_my_dataset_2026-05-12.json."

> **Note:** Copilot Chat does not support named slash commands natively — provide parameters in natural language. `.github/` is in `.gitignore` and will not be committed.

---

## Setup: ChatGPT

### Option A: Custom GPT (recommended for repeated use)

1. Go to [chatgpt.com](https://chatgpt.com) → **Explore GPTs** → **Create a GPT**
2. In the **Instructions** field, paste the full contents of [`skills/evaluate-dataset.md`](skills/evaluate-dataset.md)
3. Under **Knowledge**, upload [`CHECKLIST.csv`](CHECKLIST.csv)
4. Save the GPT
5. Start a conversation and provide your dataset source URL or paste metadata file contents

### Option B: One-off conversation

1. Open a new ChatGPT conversation
2. Paste the full contents of `skills/evaluate-dataset.md` as your first message
3. Follow up with your dataset source and parameters as described in `QUICKSTART_evaluate-dataset.md`

---

## Output format

The JSON report has three top-level sections:

- **`session`** — evaluation date, AI model, metadata sources used, dataset identity (title, DOI, landing page URL, citation), and evaluator information
- **`responses`** — one object per checklist item with `section`, `sub_section`, `question`, `status` (`meets` / `partial` / `does not meet` / `N/A`), `evidence`, `notes`, and `recommendation`
- **`summary`** — `strengths`, `gaps`, `overall_assessment` (2–3 sentence narrative), and `fair4ai_scores` (each dimension scored /10 with a one-line rationale)

Output filename convention: `FAIR4AI_eval_<dataset-name>_<YYYY-MM-DD>.json`

See `example_outputs/` for complete examples.

---

## Files in this directory

| File | Description |
|------|-------------|
| `skills/evaluate-dataset.md` | Platform-agnostic skill definition — the canonical evaluation prompt |
| `CHECKLIST.csv` | 80-item FAIR4AI-Bio checklist (8 sections, mapped to EML, DataCite, Schema.org, Croissant) |
| `CHECKLIST_OVERVIEW.md` | Narrative description of all 8 checklist sections |
| `QUICKSTART_evaluate-dataset.md` | Step-by-step usage guide with example sessions |
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
