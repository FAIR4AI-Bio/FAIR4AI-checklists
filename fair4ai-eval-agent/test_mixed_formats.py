"""
Test script to verify markdown and XML metadata support.
Creates sample metadata files and tests the agent's ability to load them.
"""

import json
from pathlib import Path
import sys

# Add parent directory to path to import fair4ai_agent
sys.path.insert(0, str(Path(__file__).parent))

from fair4ai_agent import FAIR4AIAgent


def create_test_files(test_dir: Path):
    """Create sample metadata files in different formats."""
    test_dir.mkdir(exist_ok=True)
    
    # Create a JSON metadata file
    json_data = {
        "@context": "https://schema.org/",
        "@type": "Dataset",
        "name": "Test Dataset",
        "description": "A test dataset for validation",
        "creator": {
            "@type": "Organization",
            "name": "Test Organization"
        },
        "license": "https://creativecommons.org/licenses/by/4.0/"
    }
    
    json_file = test_dir / "test_metadata.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)
    print(f"✓ Created: {json_file}")
    
    # Create a Markdown metadata file
    markdown_content = """# Test Dataset Metadata

## Overview
This is a test dataset created to validate markdown metadata support.

## Dataset Information
- **Title**: Test Dataset for Mixed Format Support
- **Creator**: Research Team
- **Date Created**: 2026-02-01
- **License**: CC-BY 4.0

## Description
This dataset contains sample data for testing the FAIR4AI evaluation agent's
ability to process natural language metadata in markdown format.

## Access Information
- **Repository**: https://example.com/dataset
- **Format**: CSV, JSON
- **Size**: 1.5 MB

## Citation
Please cite this dataset as:
Research Team (2026). Test Dataset for Mixed Format Support. https://example.com/dataset
"""
    
    md_file = test_dir / "test_metadata.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    print(f"✓ Created: {md_file}")
    
    # Create an XML metadata file (simple EML-style)
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<metadata>
  <dataset>
    <title>Test Dataset XML Metadata</title>
    <creator>
      <individualName>
        <givenName>Jane</givenName>
        <surName>Researcher</surName>
      </individualName>
      <organizationName>Test University</organizationName>
    </creator>
    <abstract>
      <para>This XML metadata describes a test dataset used to validate
      the FAIR4AI evaluation agent's support for XML-formatted metadata.</para>
    </abstract>
    <keywordSet>
      <keyword>test data</keyword>
      <keyword>validation</keyword>
      <keyword>FAIR principles</keyword>
    </keywordSet>
    <intellectualRights>
      <para>This dataset is released under CC-BY 4.0 license.</para>
    </intellectualRights>
    <coverage>
      <geographicCoverage>
        <geographicDescription>Global</geographicDescription>
      </geographicCoverage>
      <temporalCoverage>
        <rangeOfDates>
          <beginDate>2026-01-01</beginDate>
          <endDate>2026-12-31</endDate>
        </rangeOfDates>
      </temporalCoverage>
    </coverage>
  </dataset>
</metadata>
"""
    
    xml_file = test_dir / "test_metadata.xml"
    with open(xml_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"✓ Created: {xml_file}")
    
    return json_file, md_file, xml_file


def test_agent_load():
    """Test that the agent can load different metadata formats."""
    print("\n" + "="*60)
    print("Testing FAIR4AI Agent - Mixed Format Support")
    print("="*60 + "\n")
    
    # Create test directory and files
    test_dir = Path(__file__).parent / "test_metadata"
    json_file, md_file, xml_file = create_test_files(test_dir)
    
    print("\n" + "-"*60)
    print("Testing Metadata Loading")
    print("-"*60 + "\n")
    
    try:
        # Initialize agent (no API key needed for loading test)
        agent = FAIR4AIAgent.__new__(FAIR4AIAgent)
        agent.metadata_content = {}
        
        # Test loading files
        files = [str(json_file), str(md_file), str(xml_file)]
        agent.load_metadata_files(files)
        
        print("\n" + "-"*60)
        print("Loaded Metadata Summary")
        print("-"*60 + "\n")
        
        for filename, content in agent.metadata_content.items():
            print(f"📄 {filename}")
            if isinstance(content, dict):
                print(f"   Type: JSON/Dictionary")
                print(f"   Keys: {list(content.keys())[:5]}")
            elif isinstance(content, str):
                print(f"   Type: Text (Markdown/XML)")
                print(f"   Length: {len(content)} characters")
                print(f"   Preview: {content[:100]}...")
            print()
        
        # Test context building
        print("-"*60)
        print("Testing Context Prompt Building")
        print("-"*60 + "\n")
        
        context = agent._build_context_prompt()
        print(f"✓ Context prompt built successfully")
        print(f"  Total length: {len(context)} characters")
        print(f"  Number of files: {len(agent.metadata_content)}")
        
        # Show sample of context
        print("\n" + "-"*60)
        print("Context Preview (first 500 chars)")
        print("-"*60)
        print(context[:500] + "...\n")
        
        print("="*60)
        print("✅ All tests passed!")
        print("="*60 + "\n")
        
        print("The agent can now process:")
        print("  • JSON and JSON-LD files (schema.org, croissant)")
        print("  • Markdown files (README, natural language metadata)")
        print("  • XML files (EML, ISO 19115, DataCite)")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up test files
        print("\nCleaning up test files...")
        for f in [json_file, md_file, xml_file]:
            if f.exists():
                f.unlink()
        if test_dir.exists():
            test_dir.rmdir()
        print("✓ Cleanup complete\n")


if __name__ == "__main__":
    success = test_agent_load()
    sys.exit(0 if success else 1)
