"""
Quick test script to verify summary generation is working.
Run this to test that the summary section is properly added to JSON output.
"""

import os
from fair4ai_agent import FAIR4AIAgent

# Check for API key
if not os.getenv("OPENAI_SUBSCRIPTION_KEY") and not os.getenv("OPENAI_API_KEY"):
    print("ERROR: No API key found. Set OPENAI_SUBSCRIPTION_KEY or OPENAI_API_KEY environment variable.")
    exit(1)

# Determine provider
provider = "azure" if os.getenv("OPENAI_SUBSCRIPTION_KEY") else "openai"

print(f"Testing summary generation with {provider}...")
print()

# Create agent
agent = FAIR4AIAgent(provider=provider)

# Create a small test set of responses
test_responses = [
    {
        "section": "Provenance",
        "question": "Dataset title",
        "response_choices": "",
        "response": "Test Dataset",
        "evidence": "Found in metadata",
        "notes": "Clear title present"
    },
    {
        "section": "Data Access",
        "question": "Is the dataset publicly accessible?",
        "response_choices": "Yes | No",
        "response": "Yes",
        "evidence": "isAccessibleForFree: true",
        "notes": "Free and open access"
    },
    {
        "section": "Data Structure",
        "question": "Are data files available in standard formats?",
        "response_choices": "Yes | No",
        "response": "Yes",
        "evidence": "Format: CSV, JSON",
        "notes": "Multiple standard formats provided"
    }
]

# Generate summary
print("Generating summary...")
summary = agent.generate_summary(test_responses, "Test Dataset")

print("\nGenerated Summary:")
print("=" * 70)
print(f"\nStrengths ({len(summary.get('strengths', []))}):")
for strength in summary.get('strengths', []):
    print(f"  - {strength}")

print(f"\nWeaknesses ({len(summary.get('weaknesses', []))}):")
for weakness in summary.get('weaknesses', []):
    print(f"  - {weakness}")

print(f"\nOverall Assessment:")
print(f"  {summary.get('overall_assessment', 'N/A')}")

print(f"\nFAIR Score Estimate:")
for principle, score in summary.get('fair_score_estimate', {}).items():
    print(f"  {principle.capitalize()}: {score}")

print("\n" + "=" * 70)
print("Summary generation test complete!")
