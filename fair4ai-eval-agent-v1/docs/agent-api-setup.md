# Agent API Selection Considerations

This page presents key information for API setup, some [details on the recommended API (Azure OpenAI)](#azure-openai-configuration), followed by [cost and performance](#cost-and-performance) information for all supported/tested providers.

### Set Up API Keys

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

## Azure OpenAI Configuration

This section contains information specific to working with Azure OpenAI and motivation to select it.

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
