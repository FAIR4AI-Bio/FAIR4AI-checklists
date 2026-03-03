# FAIR4AI Automated Evaluation Agent

An AI-powered system that automatically evaluates datasets against the [FAIR4AI checklist form](https://forms.gle/P3MWmJJAi5vq248E8) using Large Language Models (LLMs). The agent checks metadata files or dataset landing pages for the information requested in the checklist to provide comprehensive FAIR (Findable, Accessible, Interoperable, Reusable) assessments.

## Overview

**What it does:**
- Reads dataset metadata (JSON files or extracts from URLs)
- Uses AI (OpenAI GPT, Azure OpenAI, or Anthropic Claude) to answer 135 FAIR4AI evaluation questions
- Provides evidence-based responses with citations from metadata
- Generates structured outputs in JSON and CSV formats with FAIR score estimates

**Key Features:**
- ✅ Multiple LLM providers supported (OpenAI, Azure OpenAI, Anthropic Claude)
- ✅ URL metadata extraction from dataset landing pages
- ✅ Graphical user interface (no command-line required)
- ✅ Organized output with custom directories
- ✅ Automatic FAIR score estimates and evaluation summaries
- ✅ Progress tracking and error handling

**System Requirements:**
- Python 3.8 or higher
- API key for OpenAI, Azure OpenAI, or Anthropic

---

## Quick Start

### 1. Install Dependencies
We recommend creating a [virtual environment](https://imageomics.github.io/Collaborative-distributed-science-guide/wiki-guide/Virtual-Environments/) in which to install the requirements as described below.

```bash
pip install -r requirements_agent.txt
```

### 2. Set Up API Keys

Get the API key(s) from your preferred provider(s) through the links below. Note that Azure OpenAI  is recommended for enterprise.

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Azure OpenAI: https://portal.azure.com
- Anthropic: https://console.anthropic.com/

Now that you have at least one agent API key, it's time to set up the rest of your environment:

1. Make a copy of the [example environment file](.env.example) file and name it `.env`.
2. Paste the API key(s) that you got into the appropriate constant definitions (e.g., `OPENAI_API_KEY=sk-your-openai-key-here`).
3. Remove or comment out unused constants.

More details on API keys and setup, including options for setting up your environment without a `.env` file, are provided in [docs/agent-api-setup](docs/agent-api-setup.md).

### 3. Run the Agent

**Using GUI (Easiest):**
```bash
python fair4ai_agent_ui.py
```

**Using Command Line:**
```bash
# From metadata files
python fair4ai_agent.py --metadata metadata_downloads/*.json --output my_evaluation

# From URL
python fair4ai_agent.py --url "https://data.example.com/dataset" --output-dir results/my_dataset
```

**Windows Quick Run:**
- Double-click `run_agent.ps1` or `run_agent.bat`
- Outputs will be saved in your working directory in a subfolder named `evaluation_results`

That's it! Your evaluation results will be saved as JSON and CSV files.

---

## Usage Guide

### Command-Line Interface

#### Basic Usage

```bash
python fair4ai_agent.py --metadata metadata_downloads/*.json --output my_evaluation
```

This will:
- Use default form questions from `form_ai_checklist_automated.csv`
- Process all JSON files in `metadata_downloads/`
- Use OpenAI GPT-4o-mini (default, most cost-effective)
- Generate `my_evaluation.json` and `my_evaluation.csv` in current directory

#### URL-Based Evaluation

Extract metadata directly from dataset landing pages:

```bash
python fair4ai_agent.py \
  --url "https://data.neonscience.org/data-products/DP1.10022.001" \
  --output-dir results/neon_beetles \
  --output evaluation
```

The agent will:
1. Fetch the landing page HTML
2. Extract JSON-LD/Schema.org metadata from `<script>` tags
3. Extract meta tags (Open Graph, Dublin Core, etc.)
4. Download linked JSON files
5. Save all extracted metadata to output directory
6. Run the evaluation using extracted metadata

Supported URLs include those for NEON, DataONE, Zenodo, Dryad, Hugging Face Datasets, and other repositories with structured metadata.

#### Command-Line Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--form` | Path to form questions CSV | `form_ai_checklist_automated.csv` | `--form custom_form.csv` |
| `--metadata` | Metadata file(s) (JSON) | None | `--metadata *.json` |
| `--url` | Dataset landing page URL | None | `--url "https://..."` |
| `--output` | Output file prefix | `fair4ai_evaluation` | `--output neon_beetles` |
| `--output-dir` | Output directory | Current directory | `--output-dir results/` |
| `--dataset-name` | Dataset name | Auto-detected | `--dataset-name "My Dataset"` |
| `--provider` | LLM provider | `openai` | `--provider azure` |
| `--model` | Model name | `gpt-4o-mini` | `--model gpt-4o` |
| `--azure-endpoint` | Azure endpoint URL | From env var | `--azure-endpoint https://...` |
| `--azure-api-version` | Azure API version | `2025-01-01-preview` | `--azure-api-version 2024-08-01-preview` |

**Note:** Either `--metadata` or `--url` is required (not both).

#### Advanced Examples

```bash
# Use Anthropic Claude
python fair4ai_agent.py \
  --provider anthropic \
  --model claude-3-5-sonnet-20241022 \
  --metadata metadata_downloads/*.json \
  --output detailed_eval

# Use Azure OpenAI with specific deployment
python fair4ai_agent.py \
  --provider azure \
  --model your-gpt4-deployment \
  --metadata metadata_downloads/*.json \
  --output azure_eval

# Organize outputs in custom directory
python fair4ai_agent.py \
  --metadata metadata_downloads/*.json \
  --output-dir evaluations/project_alpha \
  --output dataset_v2_evaluation \
  --dataset-name "Research Dataset v2.0"
```

### Graphical User Interface

#### Launching the GUI

```bash
python fair4ai_agent_ui.py
```

#### GUI Components

**1. Input Source Selection**
- **Metadata Files** (default): Select one or more local JSON files
  - Click "Add Files..." to browse and select files
  - Click "Clear" to remove all selected files
- **Dataset URL**: Enter the URL of a dataset landing page
  - Must start with `http://` or `https://`

**2. Form Questions**
- Select the FAIR4AI questions CSV file
- Default: `form_ai_checklist_automated.csv`

**3. LLM Provider Configuration**
- **Provider Options**: OpenAI, Azure, or Anthropic
- **Model Selection**: Choose from available models
  - OpenAI: `gpt-4o-mini` (default), `gpt-4o`, `gpt-4-turbo`
  - Azure: Your deployment name
  - Anthropic: `claude-3-5-sonnet-20241022` (default)
- **Azure Advanced Options**:
  - Azure Endpoint (auto-loaded from environment)
  - Azure API Version (auto-loaded from environment)

**4. Output Configuration**
- **Output Directory**: Where to save all output files
  - Click "Browse..." to select existing directory
  - Click "New Folder..." to create new subfolder with custom name
- **Output File Prefix**: Base name for output files
  - Creates `{prefix}.json` and `{prefix}.csv`
- **Output Preview**: Shows filenames and directory path

**5. Execution Controls**
- **Run Evaluation**: Starts the evaluation
- **Stop**: Cancel ongoing evaluation
- **Clear Log**: Clears the log window
- **Progress Bar**: Shows completion percentage
- **Log Window**: Real-time messages and status updates

#### Example Workflow: URL-Based Evaluation

1. Launch GUI: `python fair4ai_agent_ui.py`
2. Click "Dataset URL" radio button
3. Enter: `https://data.neonscience.org/data-products/DP1.10022.001`
4. Click "Browse..." → Navigate to `results/`
5. Click "New Folder..." → Enter `neon_beetles`
6. Set prefix: `evaluation`
7. Click "Run Evaluation"
8. Wait for completion (progress bar shows status)
9. Review outputs in `results/neon_beetles/`:
   - `url_metadata_extracted.json`
   - `url_metadata_jsonld_*.json`
   - `evaluation.json`
   - `evaluation.csv`

#### Example Workflow: File-Based Evaluation

1. Launch GUI
2. Click "Metadata Files" (default)
3. Click "Add Files..." → Select all JSON metadata files
4. Select/create output directory
5. Set output prefix
6. Click "Run Evaluation"
7. Check log for progress and results

### Python API

Use the agent programmatically in your own scripts:

```python
from fair4ai_agent import FAIR4AIAgent

# Initialize agent with default provider (OpenAI)
agent = FAIR4AIAgent(llm_provider="openai", model="gpt-4o-mini")

# Run evaluation with metadata files
json_path, csv_path = agent.run_evaluation(
    form_csv="form_ai_checklist_automated.csv",
    metadata_files=["metadata_downloads/dataset_metadata.json"],
    output_prefix="my_evaluation",
    output_dir="results/",
    dataset_name="My Research Dataset"
)

print(f"Results saved to {json_path} and {csv_path}")
```

**With URL extraction:**

```python
agent = FAIR4AIAgent(llm_provider="openai")

json_path, csv_path = agent.run_evaluation(
    form_csv="form_ai_checklist_automated.csv",
    dataset_url="https://data.example.com/dataset",
    output_prefix="evaluation",
    output_dir="results/my_dataset"
)
```

**With Azure OpenAI:**

```python
agent = FAIR4AIAgent(
    llm_provider="azure",
    model="your-deployment-name",
    azure_endpoint="https://your-resource.openai.azure.com/",
    azure_api_version="2025-01-01-preview"
)

json_path, csv_path = agent.run_evaluation(
    form_csv="form_ai_checklist_automated.csv",
    metadata_files=["metadata.json"],
    output_prefix="azure_evaluation"
)
```

**With Anthropic Claude:**

```python
agent = FAIR4AIAgent(
    llm_provider="anthropic",
    model="claude-3-5-sonnet-20241022"
)

json_path, csv_path = agent.run_evaluation(
    form_csv="form_ai_checklist_automated.csv",
    metadata_files=["metadata.json"],
    output_prefix="claude_evaluation"
)
```

---

## Input and Output

### Input: Form Questions CSV

The form CSV should contain:
- `position`: Question order
- `section`: Section name (e.g., "Provenance", "Data Access")
- `title`: Question text
- `description`: Additional context
- `question_type`: Type (textQuestion, choiceQuestion, SECTION_BREAK, textItem)
- `options`: Multiple choice options (pipe-separated)
- `required`: Whether required (TRUE/FALSE)

Default form: `form_ai_checklist_automated.csv` (135 questions across 9 sections)

The code used to create this file from the [FAIR4AI Checklist form](), is in the [checklist workflow directory](../checklist-workflow/00_README.md).

### Input: Metadata Files

Any JSON-formatted metadata files. The agent supports:
- Schema.org JSON-LD
- NEON API metadata
- EML (Ecological Metadata Language)
- ML Croissant
- Custom metadata formats

The agent loads all provided JSON files and presents them to the LLM as context.

### Input: URL Metadata Extraction

When using `--url`, the agent extracts:

1. **JSON-LD Scripts**: `<script type="application/ld+json">` tags
   - Schema.org Dataset/DataCatalog markup
   - Saved as `url_metadata_jsonld_0.json`, `url_metadata_jsonld_1.json`, etc.

2. **Meta Tags**: Dataset information from HTML meta tags
   - Open Graph: `og:title`, `og:description`, `og:image`, etc.
   - Dublin Core: `dc.title`, `dc.creator`, `dc.date`, etc.
   - Twitter Cards: `twitter:title`, `twitter:description`, etc.
   - Standard: `description`, `keywords`, `author`, etc.
   - Saved as `url_metadata_extracted.json`

3. **Linked JSON Files**: Downloads files linked with `<a href="*.json">`
   - Saved with original filename or as `url_metadata_linked_*.json`

### Output Files

#### Directory Structure

**From Metadata Files:**
```
output_directory/
├── {prefix}.json  # FAIR4AI evaluation results (structured)
└── {prefix}.csv   # FAIR4AI evaluation results (tabular)
```

**From URL:**
```
output_directory/
├── url_metadata_extracted.json      # Extracted meta tags
├── url_metadata_jsonld_0.json       # Schema.org JSON-LD
├── url_metadata_jsonld_1.json       # Additional JSON-LD (if present)
├── url_metadata_linked_*.json       # Downloaded linked files
├── {prefix}.json                    # FAIR4AI evaluation results
└── {prefix}.csv                     # FAIR4AI evaluation results
```
`prefix` is the name passed to the `--output` parameter.

#### JSON Output Format

```json
{
  "metadata": {
    "generated_date": "2026-01-28",
    "dataset_evaluated": "NEON Ground Beetles",
    "dataset_url": "https://data.neonscience.org/...",
    "llm_provider": "azure",
    "llm_model": "gpt-4o-mini",
    "form_file": "form_ai_checklist_automated.csv",
    "metadata_files_analyzed": [
      "url_metadata_jsonld_0.json",
      "url_metadata_extracted.json"
    ],
    "evaluation_tool_version": "2.0"
  },
  "responses": [
    {
      "section": "Provenance",
      "question": "Citation provided?",
      "response_choices": "Yes | No",
      "response": "Yes",
      "evidence": "Citation found in schema.org JSON-LD metadata under 'citation' field...",
      "notes": "Citation provided but not in BibTeX format"
    }
  ],
  "summary": {
    "overall_assessment": "The dataset demonstrates strong FAIR compliance...",
    "strengths": [
      "Comprehensive metadata with Schema.org markup",
      "Clear licensing and access information",
      "Well-documented data collection methods"
    ],
    "weaknesses": [
      "Missing machine-readable provenance",
      "Limited interoperability standards documented"
    ],
    "fair_score_estimate": {
      "findable": "9/10 - Strong persistent identifiers and rich metadata",
      "accessible": "8/10 - Clear access protocols with some authentication requirements",
      "interoperable": "7/10 - Standard formats used but limited vocabulary mappings",
      "reusable": "8/10 - Good licensing and attribution but some documentation gaps"
    },
    "recommendations": [
      "Add machine-readable provenance using PROV-O or similar standard",
      "Document semantic vocabularies and ontologies used"
    ]
  }
}
```

#### CSV Output Format

Tabular format for easy analysis in Excel, R, or Python:

```csv
section,question,response_choices,response,evidence,notes
Provenance,Citation provided?,Yes | No,Yes,Citation found in schema.org...,Citation provided but not in BibTeX format
Provenance,Summary or Abstract,Yes | No,Yes,productAbstract field contains...,""
General Information,Dataset title,NA,NEON Ground Beetles Sampled...,Found in 'name' field of JSON-LD,""
...
```
