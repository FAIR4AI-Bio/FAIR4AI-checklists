# FAIR4AI Evaluation Agent Cheat-Sheet

Common and important values and commands.

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

## Environment Variables

| Variable | Provider | Required | Example |
|----------|----------|----------|---------|
| `OPENAI_API_KEY` | OpenAI | Yes* | `sk-...` |
| `OPENAI_SUBSCRIPTION_KEY` | Azure | Yes* | `abc123...` |
| `OPENAI_ENDPOINT` | Azure | Yes* | `https://...` |
| `OPENAI_DEPLOYMENT` | Azure | No | `gpt-4o-mini` |
| `OPENAI_API_VERSION` | Azure | No | `2025-01-01-preview` |
| `ANTHROPIC_API_KEY` | Anthropic | Yes* | `sk-ant-...` |

*One provider required

## Common Commands

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
