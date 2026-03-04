# Recommendations and Examples

This file provides guidance and targeted examples for working with this package.

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
