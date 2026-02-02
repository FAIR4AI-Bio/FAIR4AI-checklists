"""
Summarize FAIR4AI evaluation results across all datasets in the results_v1 folder.

This script:
1. Searches all subfolders in results_v1 for fair4ai_evaluation.json files
2. Extracts FAIR scores from the summary section
3. Creates histograms showing distribution of scores across datasets
4. Generates a summary report
"""

import json
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re


def extract_fair_scores(summary_dict):
    """
    Extract FAIR scores from the summary section.
    
    The scores are in format like "7/10 - description"
    Returns dict with keys: findable, accessible, interoperable, reusable
    """
    scores = {}
    
    if 'fair_score_estimate' not in summary_dict:
        return None
    
    fair_scores = summary_dict['fair_score_estimate']
    
    for category in ['findable', 'accessible', 'interoperable', 'reusable']:
        if category in fair_scores:
            score_str = fair_scores[category]
            # Extract the numeric score using regex (e.g., "7/10" -> 7)
            match = re.match(r'(\d+)/10', score_str)
            if match:
                scores[category] = int(match.group(1))
            else:
                scores[category] = None
        else:
            scores[category] = None
    
    return scores


def find_evaluation_files(results_dir):
    """
    Find all fair4ai_evaluation.json files in subdirectories of results_dir.
    
    Returns list of tuples: (dataset_name, file_path)
    """
    results_path = Path(results_dir)
    evaluation_files = []
    
    for subdir in results_path.iterdir():
        if subdir.is_dir():
            eval_file = subdir / 'fair4ai_evaluation.json'
            if eval_file.exists():
                dataset_name = subdir.name
                evaluation_files.append((dataset_name, eval_file))
    
    return evaluation_files


def load_evaluations(evaluation_files):
    """
    Load all evaluation files and extract FAIR scores.
    
    Returns DataFrame with columns: dataset, findable, accessible, interoperable, reusable
    """
    data = []
    
    for dataset_name, file_path in evaluation_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                eval_data = json.load(f)
            
            if 'summary' in eval_data:
                scores = extract_fair_scores(eval_data['summary'])
                if scores:
                    scores['dataset'] = dataset_name
                    data.append(scores)
                else:
                    print(f"Warning: No FAIR scores found for {dataset_name}")
            else:
                print(f"Warning: No summary section found for {dataset_name}")
                
        except Exception as e:
            print(f"Error processing {dataset_name}: {e}")
    
    if not data:
        return None
    
    df = pd.DataFrame(data)
    # Reorder columns to put dataset first
    cols = ['dataset', 'findable', 'accessible', 'interoperable', 'reusable']
    df = df[cols]
    
    return df


def create_histograms(df, output_dir):
    """
    Create histograms for each FAIR category and save to output_dir.
    """
    categories = ['findable', 'accessible', 'interoperable', 'reusable']
    
    # Create a figure with vertically stacked subplots
    # Sized for right half of PowerPoint slide (approximately 5.5" wide x 9" tall)
    fig, axes = plt.subplots(4, 1, figsize=(5.5, 9), sharex=True)
    fig.suptitle('FAIR4AI Score Distribution\nAcross Datasets', 
                 fontsize=18, fontweight='bold', y=0.995)
    
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    
    for idx, category in enumerate(categories):
        ax = axes[idx]
        
        # Remove rows with None values for this category
        valid_scores = df[category].dropna()
        
        if len(valid_scores) == 0:
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
            ax.set_title(category.capitalize(), fontsize=16, fontweight='bold')
            continue
        
        # Create histogram
        bins = np.arange(0, 11, 1)  # 0 to 10
        counts, bin_edges, patches = ax.hist(valid_scores, bins=bins, 
                                            color=colors[idx], alpha=0.7, 
                                            edgecolor='black', linewidth=1.5)
        
        # Customize appearance
        ax.set_ylabel('Number of\nDatasets', fontsize=14, fontweight='bold')
        ax.set_title(f'{category.capitalize()}', fontsize=16, fontweight='bold', 
                    pad=10, loc='left')
        ax.set_xticks(range(0, 11))
        ax.tick_params(axis='both', labelsize=12)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Set y-axis to show integers only
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        
        # Add statistics text - larger font
        mean_score = valid_scores.mean()
        median_score = valid_scores.median()
        stats_text = f'Mean: {mean_score:.1f}\nMedian: {median_score:.1f}\nn={len(valid_scores)}'
        ax.text(0.98, 0.98, stats_text, 
               transform=ax.transAxes, 
               verticalalignment='top', 
               horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, pad=0.5),
               fontsize=12, fontweight='bold')
    
    # Only show x-axis label on bottom subplot
    axes[-1].set_xlabel('Score (out of 10)', fontsize=14, fontweight='bold')
    
    plt.tight_layout(rect=[0, 0, 1, 0.985])
    
    # Save figure
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    histogram_file = output_path / 'fair_score_histograms.png'
    plt.savefig(histogram_file, dpi=300, bbox_inches='tight')
    print(f"\nHistograms saved to: {histogram_file}")
    
    # Also create individual histograms
    for idx, category in enumerate(categories):
        fig_single, ax = plt.subplots(figsize=(8, 6))
        
        valid_scores = df[category].dropna()
        
        if len(valid_scores) > 0:
            bins = np.arange(0, 11, 1)
            ax.hist(valid_scores, bins=bins, 
                   color=colors[idx], alpha=0.7, 
                   edgecolor='black', linewidth=1.2)
            
            ax.set_xlabel('Score (out of 10)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Number of Datasets', fontsize=12, fontweight='bold')
            ax.set_title(f'FAIR4AI Score Distribution - {category.capitalize()}', 
                        fontsize=14, fontweight='bold')
            ax.set_xticks(range(0, 11))
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            
            mean_score = valid_scores.mean()
            median_score = valid_scores.median()
            stats_text = f'Mean: {mean_score:.1f}\nMedian: {median_score:.1f}\nn={len(valid_scores)}'
            ax.text(0.98, 0.98, stats_text, 
                   transform=ax.transAxes, 
                   verticalalignment='top', 
                   horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                   fontsize=10)
            
            plt.tight_layout()
            single_file = output_path / f'fair_score_{category}.png'
            plt.savefig(single_file, dpi=300, bbox_inches='tight')
            plt.close(fig_single)
    
    plt.close(fig)


def generate_summary_report(df, output_dir):
    """
    Generate a text summary report and save to output_dir.
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    report_file = output_path / 'fair_evaluation_summary.txt'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("FAIR4AI EVALUATION SUMMARY REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Total datasets evaluated: {len(df)}\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("FAIR SCORES BY CATEGORY\n")
        f.write("-" * 80 + "\n\n")
        
        categories = ['findable', 'accessible', 'interoperable', 'reusable']
        
        for category in categories:
            valid_scores = df[category].dropna()
            
            if len(valid_scores) > 0:
                f.write(f"{category.upper()}\n")
                f.write(f"  Mean:   {valid_scores.mean():.2f}/10\n")
                f.write(f"  Median: {valid_scores.median():.2f}/10\n")
                f.write(f"  Min:    {valid_scores.min():.0f}/10\n")
                f.write(f"  Max:    {valid_scores.max():.0f}/10\n")
                f.write(f"  Std:    {valid_scores.std():.2f}\n")
                f.write(f"  N:      {len(valid_scores)}\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("INDIVIDUAL DATASET SCORES\n")
        f.write("-" * 80 + "\n\n")
        
        # Sort by dataset name
        df_sorted = df.sort_values('dataset')
        
        f.write(f"{'Dataset':<30} {'Find':>6} {'Access':>6} {'Interop':>7} {'Reuse':>6}\n")
        f.write(f"{'-'*30} {'-'*6} {'-'*6} {'-'*7} {'-'*6}\n")
        
        for _, row in df_sorted.iterrows():
            f.write(f"{row['dataset']:<30} ")
            for cat in categories:
                val = row[cat]
                if pd.isna(val):
                    f.write(f"{'N/A':>6} ")
                else:
                    f.write(f"{int(val):>6} ")
            f.write("\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")
    
    print(f"Summary report saved to: {report_file}")


def save_csv(df, output_dir):
    """
    Save the DataFrame to a CSV file.
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    csv_file = output_path / 'fair_evaluation_scores.csv'
    df.to_csv(csv_file, index=False)
    print(f"Scores CSV saved to: {csv_file}")


def main():
    """
    Main function to orchestrate the analysis.
    """
    # Set the results directory
    script_dir = Path(__file__).parent
    results_dir = script_dir / 'results_v1'
    output_dir = script_dir / 'fair_summary'
    
    print("=" * 80)
    print("FAIR4AI EVALUATION SUMMARY TOOL")
    print("=" * 80)
    print(f"\nSearching for evaluation files in: {results_dir}")
    
    # Find all evaluation files
    evaluation_files = find_evaluation_files(results_dir)
    print(f"\nFound {len(evaluation_files)} evaluation files:")
    for dataset_name, _ in evaluation_files:
        print(f"  - {dataset_name}")
    
    if not evaluation_files:
        print("\nNo evaluation files found. Exiting.")
        return
    
    # Load evaluations
    print("\nLoading evaluation data...")
    df = load_evaluations(evaluation_files)
    
    if df is None or len(df) == 0:
        print("\nNo valid FAIR scores found. Exiting.")
        return
    
    print(f"\nSuccessfully loaded scores for {len(df)} datasets.")
    
    # Display basic statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    categories = ['findable', 'accessible', 'interoperable', 'reusable']
    for category in categories:
        valid_scores = df[category].dropna()
        if len(valid_scores) > 0:
            print(f"\n{category.capitalize()}:")
            print(f"  Mean:   {valid_scores.mean():.2f}/10")
            print(f"  Median: {valid_scores.median():.2f}/10")
            print(f"  Range:  {valid_scores.min():.0f} - {valid_scores.max():.0f}")
    
    # Create visualizations
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    create_histograms(df, output_dir)
    
    # Generate reports
    print("\n" + "=" * 80)
    print("GENERATING REPORTS")
    print("=" * 80)
    generate_summary_report(df, output_dir)
    save_csv(df, output_dir)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"\nAll outputs saved to: {output_dir}")


if __name__ == "__main__":
    main()
