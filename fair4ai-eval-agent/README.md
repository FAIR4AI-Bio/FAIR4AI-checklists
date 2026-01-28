# FAIR4AI Automated Evaluation Agent

An AI-powered system that automatically evaluates datasets against the FAIR4AI checklist using Large Language Models (LLMs). The agent analyzes metadata files or dataset landing pages to provide comprehensive FAIR (Findable, Accessible, Interoperable, Reusable) assessments.

## Overview

**What it does:**
- Reads dataset metadata (JSON files or extracts from URLs)
- Uses AI (OpenAI GPT, Azure OpenAI, or Anthropic Claude) to answer 135 FAIR4AI evaluation questions
- Provides evidence-based responses with citations from metadata
- Generates structured outputs in JSON and CSV formats with FAIR score estimates

**Key Features:**
- ✅ Multiple LLM providers (OpenAI, Azure OpenAI, Anthropic Claude)
- ✅ URL metadata extraction from dataset landing pages
- ✅ Graphical user interface (no command-line required)
- ✅ Organized output with custom directories
- ✅ Automatic FAIR score estimates and evaluation summaries
- ✅ Progress tracking and error handling

**System Requirements:**
- Python 3.8 or higher
- API key for OpenAI, Azure OpenAI, or Anthropic
- Dependencies: pandas, openai, anthropic, requests, beautifulsoup4

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_agent.txt
```

Or install individually:
```bash
pip install openai pandas requests beautifulsoup4  # For OpenAI
# OR
pip install anthropic pandas requests beautifulsoup4  # For Anthropic Claude
```

### 2. Set Up API Keys

**Option A: Azure OpenAI (Recommended for Enterprise)**

```powershell
$env:OPENAI_SUBSCRIPTION_KEY="your-azure-key"
$env:OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
$env:OPENAI_DEPLOYMENT="gpt-4o-mini"
$env:OPENAI_API_VERSION="2025-01-01-preview"
```

**Option B: Standard OpenAI**

```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

**Option C: Anthropic Claude**

```powershell
$env:ANTHROPIC_API_KEY="your-anthropic-key"
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Azure OpenAI: https://portal.azure.com
- Anthropic: https://console.anthropic.com/

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

Supported URLs include NEON, DataONE, Zenodo, Dryad, and other repositories with structured metadata.

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

---

## Azure OpenAI Configuration

### Why Use Azure OpenAI?

- ✅ **Enterprise Control**: Data stays within your organization's Azure tenant
- ✅ **Compliance**: Meet data residency and compliance requirements
- ✅ **Billing**: Costs appear on your Azure subscription
- ✅ **Networking**: Can use private endpoints and VNets
- ✅ **Integration**: Works with Azure AD for authentication

### Azure Setup Steps

#### 1. Get Your Azure Credentials

From Azure Portal (https://portal.azure.com):
- **API Key**: Found in your Azure OpenAI resource under "Keys and Endpoint"
- **Endpoint**: Your resource endpoint (e.g., `https://your-resource.openai.azure.com/`)
- **Deployment Name**: The name of your deployed model
- **API Version**: Usually `2025-01-01-preview` (check Azure docs for latest)

#### 2. Set Environment Variables

```powershell
$env:OPENAI_SUBSCRIPTION_KEY="your-api-key-here"
$env:OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
$env:OPENAI_DEPLOYMENT="your-deployment-name"
$env:OPENAI_API_VERSION="2025-01-01-preview"
```

**Alternative variable names (also supported):**
```powershell
$env:AZURE_OPENAI_API_KEY="your-api-key-here"
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT="your-deployment-name"
$env:AZURE_OPENAI_API_VERSION="2025-01-01-preview"
```

#### 3. Run with Azure Provider

```bash
python fair4ai_agent.py \
  --provider azure \
  --metadata metadata_downloads/*.json \
  --output results
```

### Azure Command-Line Options

```bash
# Override endpoint and API version
python fair4ai_agent.py \
  --provider azure \
  --azure-endpoint https://your-resource.openai.azure.com/ \
  --azure-api-version 2025-01-01-preview \
  --metadata metadata_downloads/*.json \
  --output results

# Specify deployment (model) name
python fair4ai_agent.py \
  --provider azure \
  --model your-gpt4-deployment \
  --metadata metadata_downloads/*.json \
  --output results
```

### Azure Troubleshooting

**Error: "OPENAI_SUBSCRIPTION_KEY environment variable not set"**
- Solution: Set your Azure OpenAI API key using either variable name:
  ```powershell
  $env:OPENAI_SUBSCRIPTION_KEY="your-key-here"
  # or
  $env:AZURE_OPENAI_API_KEY="your-key-here"
  ```

**Error: "OPENAI_ENDPOINT environment variable not set"**
- Solution: Set your Azure endpoint URL:
  ```powershell
  $env:OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
  # or
  $env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
  ```

**Error: "The API deployment for this resource does not exist"**
- Solution: Check your deployment name matches Azure Portal. Use `--model your-deployment-name`

**Error: "Invalid API version"**
- Solution: Check Azure documentation for current API version, update with `--azure-api-version`

---

## Cost and Performance

### Pricing Estimates (Per Evaluation)

| Model | Cost | Time | Quality |
|-------|------|------|---------|
| **OpenAI GPT-4o-mini** | $0.15-0.60 | 5-10 min | ⭐⭐⭐ Good (Recommended) |
| **OpenAI GPT-4o** | $2-8 | 5-15 min | ⭐⭐⭐⭐⭐ Excellent |
| **Anthropic Claude 3.5 Sonnet** | $3-12 | 5-15 min | ⭐⭐⭐⭐⭐ Excellent |
| **Azure OpenAI** | Similar to OpenAI | 5-15 min | ⭐⭐⭐⭐⭐ Excellent |

**Recommendation:** Start with GPT-4o-mini for cost-effectiveness, upgrade to GPT-4o or Claude for critical evaluations.

### Token Usage

For typical evaluation (~135 questions with standard metadata):
- **Input tokens**: 50K-200K (metadata + questions + instructions)
- **Output tokens**: 10K-50K (responses + evidence + notes)
- **Total per question**: ~1K-2K tokens average

### Processing Time

- **Sequential processing**: Questions processed one at a time to maintain context
- **Batch updates**: Progress shown every 5 questions
- **Total time**: 5-15 minutes depending on metadata size and model speed

---

## Technical Details

### Architecture

The agent is built with:
- **Class-based design**: `FAIR4AIAgent` class with clear methods
- **Provider abstraction**: Easy switching between OpenAI/Azure/Anthropic
- **Error handling**: Graceful failures with informative messages
- **Progress tracking**: Real-time updates during processing

### LLM Integration

- **System prompt**: Instructs LLM to act as FAIR metadata expert
- **Context window**: Provides all metadata as context for each question
- **Structured output**: Requests JSON responses for consistent parsing
- **Temperature**: Set to 0.1 for consistent, factual responses

### Evaluation Sections

The agent processes questions from these FAIR4AI sections:

1. **Respondent Information** (11 questions)
2. **Provenance** (18 questions)
3. **General Information** (10 questions)
4. **Data Structure** (7 questions)
5. **Data Origin** (13 questions)
6. **Data Processing** (12 questions)
7. **Data Quality** (22 questions)
8. **Guidance and Recommendations** (14 questions)
9. **Data Access** (16 questions)

**Total:** 135 questions

### URL Metadata Extraction

The `extract_metadata_from_url()` method:
1. Fetches HTML with `requests` library
2. Parses HTML with `BeautifulSoup`
3. Extracts JSON-LD scripts and meta tags
4. Downloads linked JSON files
5. Saves all extracted content
6. Adds content to `self.metadata_content` for evaluation

---

## Files and Structure

### Core Files
- **fair4ai_agent.py** - Main agent script (600+ lines) with LLM integration
- **fair4ai_agent_ui.py** - Graphical user interface with tkinter
- **requirements_agent.txt** - Python dependencies
- **form_ai_checklist_automated.csv** - FAIR4AI form questions (135 questions)

### Helper Scripts
- **example_usage.py** - Python API usage examples
- **test_setup.py** - Test API configuration
- **test_summary.py** - Test summary generation
- **run_agent.ps1** - PowerShell convenience script
- **run_agent.bat** - Batch file convenience script

### Templates
- **TEMPLATE_RESPONSE_neon_DP1.10022.001_form_responses.json** - Example JSON output
- **TEMPLATE_RESPONSE_TABULAR_neon_DP1.10022.001_form_response.csv** - Example CSV output

### Configuration
- **.env.example** - Example environment variables template

The agent is fully self-contained in this directory and doesn't require files from parent directories.

---

## Troubleshooting

### Installation Issues

**Error: "ModuleNotFoundError: No module named 'openai'"**
- Solution: Install dependencies
  ```bash
  pip install -r requirements_agent.txt
  # or
  pip install openai pandas requests beautifulsoup4
  ```

**Error: "No module named 'tkinter'" (Linux)**
- Solution: Install tkinter
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-tk
  # Fedora
  sudo dnf install python3-tkinter
  ```

### API Key Issues

**Error: "OPENAI_API_KEY environment variable not set"**
- Solution: Set your API key
  ```powershell
  $env:OPENAI_API_KEY="sk-your-key-here"
  ```
- Make sure to set it in the same terminal session before running

**Error: "Incorrect API key provided"**
- Solution: Verify your API key is correct
- Check for extra spaces or quotes
- Get a new key from the provider's console

**Error: "You exceeded your current quota"**
- Solution: Add credits to your account or check billing settings
- OpenAI: https://platform.openai.com/account/billing
- Anthropic: https://console.anthropic.com/settings/billing

### URL Extraction Issues

**Error: "No metadata found at URL"**
- Solution: 
  - Verify URL is accessible in browser
  - Check if page has structured metadata (View Page Source → search for "json-ld")
  - Try downloading metadata files manually and use `--metadata` instead
  - Some sites block automated scraping

**Error: "Invalid URL format"**
- Solution: URL must start with `http://` or `https://`

### File Issues

**Error: "No metadata files found"**
- Solution: 
  - Check files are in correct directory
  - Use absolute paths or wildcards: `--metadata c:/path/to/*.json`
  - Verify files are valid JSON format

**Error: "Permission denied" when creating folder**
- Solution:
  - Choose directory with write permissions
  - Run as administrator (if needed)
  - Check available disk space

### Processing Issues

**Error: "JSON parse error" from LLM**
- Solution: Rare formatting issue - try running again
- The LLM sometimes returns invalid JSON; retry usually succeeds

**Error: "Rate limit exceeded"**
- Solution:
  - Wait a moment and retry
  - Reduce concurrent requests
  - Upgrade API tier if frequent

**Partial results after error**
- The agent saves progress - check output files for partial results
- Review log for specific question that failed
- Can manually fix or re-run failed sections

### GUI Issues

**GUI doesn't open**
- Solution: Run from command line to see error messages
  ```bash
  python fair4ai_agent_ui.py
  ```
- Check tkinter is installed (see Installation Issues above)

**"Browse" button doesn't work**
- Solution: Ensure you have file dialog support
- Try using command-line interface instead

---

## Best Practices

### Organizing Your Evaluations

**Directory Structure:**
```
results/
├── project_alpha/
│   ├── dataset1_evaluation/
│   │   ├── url_metadata_*.json
│   │   ├── evaluation.json
│   │   └── evaluation.csv
│   ├── dataset2_evaluation/
│   └── dataset3_evaluation/
├── project_beta/
└── archived/
    └── old_evaluations/
```

**Naming Conventions:**

✅ **Good prefixes:**
- `neon_DP1_10022_001_2024`
- `inat_observations_v2`
- `climate_data_evaluation`

❌ **Bad prefixes:**
- `test`
- `output1`
- `data`

### Before Running Large Evaluations

1. ✅ Test with a small dataset first
2. ✅ Verify API keys are working
3. ✅ Check available API quota/credits
4. ✅ Create organized output directory structure
5. ✅ Use descriptive file prefixes

### After Completing Evaluation

1. ✅ Review log for errors or warnings
2. ✅ Verify both JSON and CSV files created
3. ✅ Check extracted metadata files (if using URL mode)
4. ✅ Backup results to long-term storage
5. ✅ Document evaluation settings and date

### Cost Management

1. **Use GPT-4o-mini by default** - Best balance of cost and quality
2. **Test with small metadata first** - Verify before processing large files
3. **Monitor your usage** - Check API dashboards regularly
4. **Use Azure for enterprise** - Better cost tracking and controls

---

## Examples and Workflows

### Example 1: Quick Evaluation from Files

```bash
# Prepare metadata
cd metadata_downloads/

# Run evaluation
python ../fair4ai_agent.py \
  --metadata *.json \
  --output quick_eval

# Check results
cat quick_eval.json
```

### Example 2: URL-Based Evaluation

```bash
# Single command evaluation
python fair4ai_agent.py \
  --url "https://data.neonscience.org/data-products/DP1.10022.001" \
  --output-dir results/neon_beetles \
  --output evaluation

# Results in:
# results/neon_beetles/url_metadata_*.json
# results/neon_beetles/evaluation.json
# results/neon_beetles/evaluation.csv
```

### Example 3: Batch Evaluations

```bash
# Create project structure
mkdir -p results/comparison_study

# Evaluate dataset 1
python fair4ai_agent.py \
  --url "https://dataset1.example.com" \
  --output-dir results/comparison_study/dataset1 \
  --output evaluation

# Evaluate dataset 2
python fair4ai_agent.py \
  --url "https://dataset2.example.com" \
  --output-dir results/comparison_study/dataset2 \
  --output evaluation

# Compare results
python -c "
import pandas as pd
df1 = pd.read_csv('results/comparison_study/dataset1/evaluation.csv')
df2 = pd.read_csv('results/comparison_study/dataset2/evaluation.csv')
print('Dataset 1:', df1[df1['response']=='Yes'].shape[0], 'Yes responses')
print('Dataset 2:', df2[df2['response']=='Yes'].shape[0], 'Yes responses')
"
```

### Example 4: GUI Batch Evaluation

1. Launch GUI: `python fair4ai_agent_ui.py`
2. For each dataset:
   - Switch to URL mode
   - Enter dataset URL
   - Click "New Folder..." → Enter dataset name
   - Set output prefix
   - Click "Run Evaluation"
   - Wait for completion
   - Repeat for next dataset

### Example 5: Custom Python Integration

```python
#!/usr/bin/env python3
"""Custom evaluation script with post-processing"""

import json
from pathlib import Path
from fair4ai_agent import FAIR4AIAgent

# Initialize agent
agent = FAIR4AIAgent(llm_provider="openai", model="gpt-4o-mini")

# List of datasets to evaluate
datasets = [
    {
        "url": "https://data.neonscience.org/data-products/DP1.10022.001",
        "name": "NEON Beetles"
    },
    {
        "url": "https://data.neonscience.org/data-products/DP1.10058.001",
        "name": "NEON Plants"
    }
]

# Evaluate each dataset
results_summary = []

for dataset in datasets:
    print(f"\nEvaluating {dataset['name']}...")
    
    output_dir = f"results/{dataset['name'].lower().replace(' ', '_')}"
    
    json_path, csv_path = agent.run_evaluation(
        form_csv="form_ai_checklist_automated.csv",
        dataset_url=dataset['url'],
        output_prefix="evaluation",
        output_dir=output_dir
    )
    
    # Load results
    with open(json_path) as f:
        data = json.load(f)
    
    # Extract summary
    summary = {
        "dataset": dataset['name'],
        "fair_scores": data.get('summary', {}).get('fair_score_estimate', {}),
        "output_dir": output_dir
    }
    results_summary.append(summary)
    
    print(f"  Completed: {json_path}")

# Print comparison
print("\n=== FAIR Score Comparison ===")
for result in results_summary:
    print(f"\n{result['dataset']}:")
    for dimension, score in result['fair_scores'].items():
        print(f"  {dimension.capitalize()}: {score}")
```

---

## Version and Updates

**Current Version:** 2.0

**Recent Updates:**
- ✅ URL metadata extraction with BeautifulSoup
- ✅ Output directory organization
- ✅ GUI with input mode selection
- ✅ Automatic FAIR score estimates and summaries
- ✅ Enhanced error handling and validation
- ✅ Progress tracking improvements

**Last Updated:** January 2026

---

## License

This agent is part of the FAIR4AI project. See project documentation for licensing information.

---

## Quick Reference

### Environment Variables

| Variable | Provider | Required | Example |
|----------|----------|----------|---------|
| `OPENAI_API_KEY` | OpenAI | Yes* | `sk-...` |
| `OPENAI_SUBSCRIPTION_KEY` | Azure | Yes* | `abc123...` |
| `OPENAI_ENDPOINT` | Azure | Yes* | `https://...` |
| `OPENAI_DEPLOYMENT` | Azure | No | `gpt-4o-mini` |
| `OPENAI_API_VERSION` | Azure | No | `2025-01-01-preview` |
| `ANTHROPIC_API_KEY` | Anthropic | Yes* | `sk-ant-...` |

*One provider required

### Common Commands

```bash
# Basic file evaluation
python fair4ai_agent.py --metadata *.json --output results

# URL evaluation
python fair4ai_agent.py --url "https://..." --output-dir results/dataset

# Azure OpenAI
python fair4ai_agent.py --provider azure --metadata *.json --output results

# Anthropic Claude
python fair4ai_agent.py --provider anthropic --metadata *.json --output results

# GUI
python fair4ai_agent_ui.py

# Quick run (Windows)
.\run_agent.ps1
```

### File Locations

- **Agent**: `fair4ai_agent.py`
- **GUI**: `fair4ai_agent_ui.py`
- **Form**: `form_ai_checklist_automated.csv`
- **Requirements**: `requirements_agent.txt`
- **Examples**: `example_usage.py`, `test_setup.py`, `test_summary.py`
