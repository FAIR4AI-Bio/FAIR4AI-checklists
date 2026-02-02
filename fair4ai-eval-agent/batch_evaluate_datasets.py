"""
Batch evaluation script for FAIR4AI datasets.

This script processes all datasets listed in FAIROS_biodata_dataset_list_v1.csv,
evaluating each one in parallel using the FAIR4AI agent.

Results are stored in OUTPUT_DIR/<dataset_short_name>/ directories.
Configure the OUTPUT_DIR variable at the top of this script.
"""

import pandas as pd
import os
from pathlib import Path
from fair4ai_agent import FAIR4AIAgent
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
import sys
import traceback


# ============================================================================
# CONFIGURATION - Edit these paths as needed
# ============================================================================
DATASET_LIST_CSV = "FAIROS_biodata_dataset_list_v1.csv"  # Input CSV with dataset list
FORM_CSV = "form_ai_checklist_automated.csv"              # FAIR4AI evaluation form
OUTPUT_DIR = "results_v1.1"                                 # Base output directory
MAX_WORKERS = 8                                           # Max parallel workers
# ============================================================================


def evaluate_single_dataset(row_dict, form_csv_path, output_base_dir):
    """
    Evaluate a single dataset from the CSV.
    
    Args:
        row_dict: Dictionary containing row data from CSV
        form_csv_path: Path to the form CSV file
        output_base_dir: Base directory for output files
        
    Returns:
        Dictionary with results and status
    """
    dataset_name = row_dict['dataset_short_name']
    url = row_dict['url']
    
    print(f"\n{'='*70}")
    print(f"Processing: {dataset_name}")
    print(f"URL: {url}")
    print(f"Output: {Path(output_base_dir).absolute() / dataset_name}")
    print(f"{'='*70}")
    
    # Create output directory
    output_dir = Path(output_base_dir) / dataset_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Check for API keys
        api_key = None
        provider = None
        
        if os.getenv("OPENAI_SUBSCRIPTION_KEY") or os.getenv("AZURE_OPENAI_API_KEY"):
            provider = "azure"
            api_key = os.getenv("OPENAI_SUBSCRIPTION_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
        elif os.getenv("OPENAI_API_KEY"):
            provider = "openai"
            api_key = os.getenv("OPENAI_API_KEY")
        elif os.getenv("ANTHROPIC_API_KEY"):
            provider = "anthropic"
            api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key:
            raise ValueError("No API key found. Set OPENAI_API_KEY, OPENAI_SUBSCRIPTION_KEY, or ANTHROPIC_API_KEY")
        
        # Initialize agent
        agent = FAIR4AIAgent(llm_provider=provider)
        
        # Run evaluation
        json_path, csv_path = agent.run_evaluation(
            form_csv=form_csv_path,
            dataset_url=url,
            output_prefix="fair4ai_evaluation",
            dataset_name=dataset_name,
            output_dir=str(output_dir)
        )
        
        return {
            "dataset": dataset_name,
            "status": "SUCCESS",
            "url": url,
            "json_output": str(json_path),
            "csv_output": str(csv_path),
            "error": None
        }
        
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"\n✗ Error processing {dataset_name}: {error_msg}")
        traceback.print_exc()
        
        return {
            "dataset": dataset_name,
            "status": "FAILED",
            "url": url,
            "json_output": None,
            "csv_output": None,
            "error": error_msg
        }


def main():
    """Main batch processing function."""
    print("="*70)
    print("FAIR4AI Batch Dataset Evaluation")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check for API keys
    if not any([
        os.getenv("OPENAI_API_KEY"),
        os.getenv("OPENAI_SUBSCRIPTION_KEY"),
        os.getenv("AZURE_OPENAI_API_KEY"),
        os.getenv("ANTHROPIC_API_KEY")
    ]):
        print("ERROR: No API key found!")
        print("Please set one of the following environment variables:")
        print("  - OPENAI_API_KEY (for OpenAI)")
        print("  - OPENAI_SUBSCRIPTION_KEY or AZURE_OPENAI_API_KEY (for Azure)")
        print("  - ANTHROPIC_API_KEY (for Anthropic)")
        sys.exit(1)
    
    # Load the dataset list
    csv_path = Path(DATASET_LIST_CSV)
    if not csv_path.exists():
        print(f"ERROR: Dataset list not found: {csv_path}")
        sys.exit(1)
    
    df = pd.read_csv(csv_path)
    print(f"Found {len(df)} datasets to process\n")
    
    # Check for form CSV
    form_csv = Path(FORM_CSV)
    if not form_csv.exists():
        print(f"ERROR: Form CSV not found: {form_csv}")
        sys.exit(1)
    
    # Create results directory
    results_dir = Path(OUTPUT_DIR)
    results_dir.mkdir(exist_ok=True)
    print(f"Output directory: {results_dir.absolute()}\n")
    
    # Convert DataFrame rows to dictionaries for parallel processing
    datasets_to_process = df.to_dict('records')
    
    # Process datasets in parallel
    max_workers = min(MAX_WORKERS, len(datasets_to_process))  # Limit concurrent jobs
    print(f"Processing with {max_workers} parallel workers\n")
    
    results = []
    completed = 0
    total = len(datasets_to_process)
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_dataset = {
            executor.submit(evaluate_single_dataset, row_dict, str(form_csv), OUTPUT_DIR): row_dict['dataset_short_name']
            for row_dict in datasets_to_process
        }
        
        # Process completed tasks as they finish
        for future in as_completed(future_to_dataset):
            dataset_name = future_to_dataset[future]
            completed += 1
            
            try:
                result = future.result()
                results.append(result)
                
                status_symbol = "✓" if result['status'] == 'SUCCESS' else "✗"
                print(f"\n[{completed}/{total}] {status_symbol} {dataset_name}: {result['status']}")
                
            except Exception as e:
                print(f"\n[{completed}/{total}] ✗ {dataset_name}: EXCEPTION - {e}")
                results.append({
                    "dataset": dataset_name,
                    "status": "EXCEPTION",
                    "url": None,
                    "json_output": None,
                    "csv_output": None,
                    "error": str(e)
                })
    
    # Save summary report
    print("\n" + "="*70)
    print("Batch Processing Complete!")
    print("="*70)
    
    summary_df = pd.DataFrame(results)
    summary_path = results_dir / f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    summary_df.to_csv(summary_path, index=False)
    
    # Print summary statistics
    success_count = len(summary_df[summary_df['status'] == 'SUCCESS'])
    failed_count = len(summary_df[summary_df['status'] != 'SUCCESS'])
    
    print(f"\nTotal datasets: {total}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failed_count}")
    print(f"\nSummary saved to: {summary_path}")
    
    # List failed datasets if any
    if failed_count > 0:
        print("\nFailed datasets:")
        for _, row in summary_df[summary_df['status'] != 'SUCCESS'].iterrows():
            print(f"  - {row['dataset']}: {row['error']}")
    
    print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
