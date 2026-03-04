"""
Example script showing how to use the FAIR4AI Agent programmatically.

This demonstrates the Python API for the agent, as an alternative to
the command-line interface.
"""

from fair4ai_agent import FAIR4AIAgent
import os
from pathlib import Path


def example_evaluation():
    """Run a simple example evaluation."""
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: No API key found!")
        print("Please set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
        print("\nExample:")
        print('  export OPENAI_API_KEY="your-key-here"')
        print("  or in PowerShell:")
        print('  $env:OPENAI_API_KEY="your-key-here"')
        return
    
    # Determine which provider to use
    provider = "openai" if os.getenv("OPENAI_API_KEY") else "anthropic"
    
    print(f"Using LLM provider: {provider}\n")
    
    # Initialize the agent
    agent = FAIR4AIAgent(llm_provider=provider)
    
    # Find metadata files (can be in parent directory or local)
    metadata_dir = Path("../metadata_downloads")
    if not metadata_dir.exists():
        metadata_dir = Path("metadata_downloads")
    metadata_files = list(metadata_dir.glob("*.json"))
    
    if not metadata_files:
        print(f"No metadata files found in {metadata_dir}")
        print("Please add JSON metadata files to evaluate")
        return
    
    print(f"Found {len(metadata_files)} metadata files:")
    for f in metadata_files:
        print(f"  - {f.name}")
    print()
    
    # Run the evaluation
    output_prefix = "example_evaluation"
    
    try:
        json_path, csv_path = agent.run_evaluation(
            form_csv="form_ai_checklist_automated.csv",
            metadata_files=[str(f) for f in metadata_files],
            output_prefix=output_prefix,
            dataset_name=None  # Auto-detect from metadata
        )
        
        print(f"\n✓ Evaluation complete!")
        print(f"  JSON: {json_path}")
        print(f"  CSV:  {csv_path}")
        
    except Exception as e:
        print(f"\n✗ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()


def example_custom_questions():
    """Example of processing specific questions only."""
    
    from fair4ai_agent import FAIR4AIAgent
    import pandas as pd
    
    # Initialize agent
    agent = FAIR4AIAgent(llm_provider="openai")
    
    # Load form and metadata
    agent.load_form_questions("form_ai_checklist_automated.csv")
    agent.load_metadata_files(["metadata_downloads/neon_DP1.10022.001_schema_org.json"])
    
    # Build context
    metadata_context = agent._build_context_prompt()
    
    # Process just the first few questions
    print("Processing first 5 questions as a demo:\n")
    
    for idx, row in agent.form_questions.head(10).iterrows():
        if row['question_type'] in ['SECTION_BREAK', 'textItem']:
            continue
            
        print(f"Question: {row['title']}")
        
        result = agent.answer_question(row, metadata_context)
        
        if result:
            print(f"  Response: {result['response']}")
            print(f"  Evidence: {result['evidence'][:100]}...")
            print()


if __name__ == "__main__":
    print("=" * 70)
    print("FAIR4AI Agent - Example Usage")
    print("=" * 70)
    print()
    
    # Run the example
    example_evaluation()
    
    # Uncomment to try custom processing:
    # example_custom_questions()
