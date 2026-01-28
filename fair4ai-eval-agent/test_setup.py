"""
Test script to verify FAIR4AI Agent setup and functionality.

This script checks:
1. Python dependencies are installed
2. API keys are configured
3. Required files exist
4. Agent can be imported and initialized

Run this before your first evaluation to catch any setup issues.
"""

import sys
from pathlib import Path


def test_imports():
    """Test that required packages are installed."""
    print("🔍 Checking Python dependencies...")
    
    required = {
        'pandas': 'pandas',
        'json': 'json (built-in)',
        'csv': 'csv (built-in)',
    }
    
    llm_packages = []
    
    # Check required packages
    for module, name in required.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT FOUND")
            return False
    
    # Check LLM packages (need at least one)
    try:
        __import__('openai')
        print(f"  ✓ openai")
        llm_packages.append('openai')
    except ImportError:
        print(f"  ⚠ openai - not installed")
    
    try:
        __import__('anthropic')
        print(f"  ✓ anthropic")
        llm_packages.append('anthropic')
    except ImportError:
        print(f"  ⚠ anthropic - not installed")
    
    if not llm_packages:
        print(f"\n  ✗ ERROR: No LLM package found!")
        print(f"     Install one with: pip install openai")
        print(f"                   or: pip install anthropic")
        return False
    
    print(f"\n  ✓ Found LLM provider(s): {', '.join(llm_packages)}")
    return True


def test_api_keys():
    """Test that API keys are configured."""
    import os
    
    print("\n🔑 Checking API keys...")
    
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    if openai_key:
        print(f"  ✓ OPENAI_API_KEY is set")
        print(f"    Key starts with: {openai_key[:10]}...")
    else:
        print(f"  ⚠ OPENAI_API_KEY not set")
    
    if anthropic_key:
        print(f"  ✓ ANTHROPIC_API_KEY is set")
        print(f"    Key starts with: {anthropic_key[:10]}...")
    else:
        print(f"  ⚠ ANTHROPIC_API_KEY not set")
    
    if not openai_key and not anthropic_key:
        print(f"\n  ✗ ERROR: No API key found!")
        print(f"     Set one with:")
        print(f"       $env:OPENAI_API_KEY='your-key-here'  (PowerShell)")
        print(f"       export OPENAI_API_KEY='your-key-here'  (Mac/Linux)")
        return False
    
    return True


def test_files():
    """Test that required files exist."""
    print("\n📁 Checking required files...")
    
    required_files = [
        'fair4ai_agent.py',
        'form_ai_checklist_automated.csv',
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = Path(filename)
        if filepath.exists():
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} - NOT FOUND")
            all_exist = False
    
    # Check metadata directory
    metadata_dir = Path('metadata_downloads')
    if metadata_dir.exists():
        json_files = list(metadata_dir.glob('*.json'))
        if json_files:
            print(f"  ✓ metadata_downloads/ ({len(json_files)} JSON files)")
            for f in json_files:
                print(f"    - {f.name}")
        else:
            print(f"  ⚠ metadata_downloads/ exists but no JSON files found")
            print(f"    Add metadata files to test with real data")
    else:
        print(f"  ✗ metadata_downloads/ - NOT FOUND")
        all_exist = False
    
    return all_exist


def test_agent_import():
    """Test that the agent can be imported and initialized."""
    print("\n🤖 Testing agent import...")
    
    try:
        from fair4ai_agent import FAIR4AIAgent
        print(f"  ✓ FAIR4AIAgent imported successfully")
        
        # Try to initialize (this will check for API keys)
        import os
        if os.getenv('OPENAI_API_KEY'):
            agent = FAIR4AIAgent(llm_provider='openai')
            print(f"  ✓ Agent initialized with OpenAI")
            print(f"    Model: {agent.model}")
            return True
        elif os.getenv('ANTHROPIC_API_KEY'):
            agent = FAIR4AIAgent(llm_provider='anthropic')
            print(f"  ✓ Agent initialized with Anthropic")
            print(f"    Model: {agent.model}")
            return True
        else:
            print(f"  ⚠ Agent cannot initialize without API key")
            return False
            
    except Exception as e:
        print(f"  ✗ Error importing/initializing agent: {e}")
        return False


def run_quick_test():
    """Run a quick test with a single question (if API key is available)."""
    print("\n🧪 Running quick functionality test...")
    
    try:
        from fair4ai_agent import FAIR4AIAgent
        import os
        import pandas as pd
        
        if not os.getenv('OPENAI_API_KEY') and not os.getenv('ANTHROPIC_API_KEY'):
            print("  ⚠ Skipping (no API key)")
            return True
        
        # Initialize agent
        provider = 'openai' if os.getenv('OPENAI_API_KEY') else 'anthropic'
        agent = FAIR4AIAgent(llm_provider=provider)
        
        # Load form
        agent.load_form_questions('form_ai_checklist_automated.csv')
        
        # Load metadata if available
        metadata_dir = Path('metadata_downloads')
        json_files = list(metadata_dir.glob('*.json'))
        
        if not json_files:
            print("  ⚠ Skipping (no metadata files to test with)")
            return True
        
        agent.load_metadata_files([str(json_files[0])])
        
        # Test answering one simple question
        print(f"  Testing with 1 question using {provider}...")
        
        # Find a simple text question
        test_question = None
        for idx, row in agent.form_questions.iterrows():
            if row['question_type'] == 'textQuestion' and 'Dataset title' in str(row.get('title', '')):
                test_question = row
                break
        
        if test_question is None:
            print("  ⚠ Could not find suitable test question")
            return True
        
        metadata_context = agent._build_context_prompt()
        result = agent.answer_question(test_question, metadata_context)
        
        if result and result.get('response'):
            print(f"  ✓ Successfully processed test question")
            print(f"    Question: {test_question['title']}")
            print(f"    Response: {result['response'][:100]}...")
            return True
        else:
            print(f"  ✗ Test question failed")
            return False
            
    except Exception as e:
        print(f"  ✗ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("FAIR4AI Agent - Setup Verification")
    print("=" * 70)
    print()
    
    results = {
        'imports': test_imports(),
        'api_keys': test_api_keys(),
        'files': test_files(),
        'agent': test_agent_import(),
    }
    
    # Only run functionality test if basics pass
    if all(results.values()):
        results['quick_test'] = run_quick_test()
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}  {test_name}")
    
    print()
    
    if all(results.values()):
        print("🎉 All tests passed! You're ready to run evaluations.")
        print()
        print("Try running:")
        print("  python fair4ai_agent.py --metadata metadata_downloads/*.json --output test")
        return 0
    else:
        print("⚠️  Some tests failed. Please fix the issues above before running evaluations.")
        print()
        print("Common fixes:")
        print("  - Install dependencies: pip install -r requirements_agent.txt")
        print("  - Set API key: $env:OPENAI_API_KEY='your-key-here'")
        print("  - Check that all files are present")
        return 1


if __name__ == "__main__":
    sys.exit(main())
