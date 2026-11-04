#!/usr/bin/env python3
"""
Map Google Form questions to schema.org and MLCommons Croissant metadata standards.

This script reads form_download.csv and creates:
1. A JSON-LD file with schema.org Dataset metadata
2. A Croissant metadata JSON file
3. A modified CSV indicating how each question maps to these standards

Usage:
    python map_to_standards.py --input form_download.csv --output-prefix mapped_form
"""

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List, Any, Optional


# Schema.org Dataset property mappings
SCHEMA_ORG_MAPPINGS = {
    # Basic citation metadata
    "Creators": "creator",
    "Title": "name",
    "Summary or Abstract": "description",
    "Date Created": "dateCreated",
    "Publisher": "publisher",
    "Keywords/Tags": "keywords",
    
    # Content and purpose
    "Purpose of the data": "description",
    "Content -- short description": "abstract",
    "Summary -- short summary": "description",
    
    # Spatial and temporal
    "Spatial Extent": "spatialCoverage",
    "Temporal Extent": "temporalCoverage",
    
    # Technical details
    "What file format(s) encode the data?": "encodingFormat",
    "What is the dataset layout pattern?": "distribution",
    
    # Funding
    "Funding Description and Grants": "funding",
    
    # Access
    "License": "license",
    "Homepage": "url",
    "Repository": "codeRepository",
    
    # Related work
    "Paper": "citation",
    "Related Dataset": "isBasedOn",
}


# Croissant metadata mappings
CROISSANT_MAPPINGS = {
    # Core metadata
    "Title": "@name",
    "Summary or Abstract": "description",
    "Creators": "creator",
    "Date Created": "datePublished",
    "Publisher": "publisher",
    "Keywords/Tags": "keywords",
    "License": "license",
    
    # Distribution
    "Homepage": "url",
    "Repository": "codeRepository",
    "What file format(s) encode the data?": "encodingFormat",
    
    # RecordSet fields
    "What features or attributes": "field",
    "What is the organizational structure": "recordSet",
    "What is the primary unit of data": "field/@name",
    
    # Data collection
    "Collection Method Documentation": "conditionsOfAccess",
    "Instrumentation": "measurementTechnique",
    "Annotation Process": "annotation",
    
    # Splits
    "training, validation, and/or test sets": "RecordSet (splits)",
    
    # Quality
    "quality assurance checks": "variableMeasured",
}


def load_form_csv(input_path: str) -> List[Dict[str, Any]]:
    """Load the form CSV file."""
    rows = []
    with open(input_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def find_mapping(title: str, mappings: Dict[str, str]) -> Optional[str]:
    """Find if a question title maps to a standard field."""
    # Exact match
    if title in mappings:
        return mappings[title]
    
    # Partial match (case insensitive)
    title_lower = title.lower()
    for key, value in mappings.items():
        if key.lower() in title_lower or title_lower in key.lower():
            return value
    
    return None


def create_schema_org_jsonld(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a schema.org JSON-LD Dataset representation."""
    dataset = {
        "@context": "https://schema.org/",
        "@type": "Dataset",
        "@id": "",
        "name": "",
        "description": "",
        "creator": [],
        "keywords": [],
        "dateCreated": "",
        "publisher": {},
        "distribution": [],
        "spatialCoverage": {},
        "temporalCoverage": "",
        "measurementTechnique": [],
        "variableMeasured": [],
        "funding": {},
        "license": "",
        "url": "",
        "citation": []
    }
    
    # Map form fields to schema.org properties
    for row in rows:
        title = row.get('title', '')
        schema_prop = find_mapping(title, SCHEMA_ORG_MAPPINGS)
        
        if schema_prop:
            # This is a placeholder - in real use, actual form response data would populate these
            if schema_prop not in dataset:
                dataset[schema_prop] = f"[From form question: {title}]"
    
    return dataset


def create_croissant_metadata(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a Croissant metadata representation."""
    croissant = {
        "@context": {
            "@language": "en",
            "@vocab": "https://schema.org/",
            "sc": "https://schema.org/",
            "ml": "http://mlcommons.org/croissant/"
        },
        "@type": "sc:Dataset",
        "@id": "",
        "name": "",
        "description": "",
        "creator": [],
        "datePublished": "",
        "publisher": {},
        "keywords": [],
        "license": "",
        "url": "",
        "distribution": [],
        "recordSet": [],
        "field": []
    }
    
    # Map form fields to Croissant properties
    for row in rows:
        title = row.get('title', '')
        croissant_prop = find_mapping(title, CROISSANT_MAPPINGS)
        
        if croissant_prop:
            # This is a placeholder
            if croissant_prop not in croissant:
                croissant[croissant_prop] = f"[From form question: {title}]"
    
    return croissant


def add_mapping_to_descriptions(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Add standard mappings to the description field of each row."""
    modified_rows = []
    
    for row in rows:
        modified_row = row.copy()
        title = row.get('title', '')
        original_desc = row.get('description', '')
        
        schema_mapping = find_mapping(title, SCHEMA_ORG_MAPPINGS)
        croissant_mapping = find_mapping(title, CROISSANT_MAPPINGS)
        
        # Build mapping information
        mapping_info = []
        if schema_mapping:
            mapping_info.append(f"schema.org: {schema_mapping}")
        if croissant_mapping:
            mapping_info.append(f"Croissant: {croissant_mapping}")
        
        # Append mapping info to description
        if mapping_info:
            separator = " | " if original_desc else ""
            mapping_text = " | ".join(mapping_info)
            modified_row['description'] = f"{original_desc}{separator}MAPS TO: {mapping_text}"
        
        modified_rows.append(modified_row)
    
    return modified_rows


def write_csv(rows: List[Dict[str, Any]], output_path: str) -> None:
    """Write rows to a CSV file."""
    if not rows:
        return
    
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    fieldnames = list(rows[0].keys())
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(data: Dict[str, Any], output_path: str) -> None:
    """Write data to a JSON file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_mapping_report(rows: List[Dict[str, Any]]) -> str:
    """Generate a text report of all mappings found."""
    report_lines = ["# Metadata Standard Mappings Report\n"]
    report_lines.append("## Questions Mapped to Standards\n")
    
    schema_count = 0
    croissant_count = 0
    unmapped_count = 0
    
    for row in rows:
        title = row.get('title', '')
        if not title or row.get('question_type') == 'SECTION_BREAK':
            continue
            
        schema_mapping = find_mapping(title, SCHEMA_ORG_MAPPINGS)
        croissant_mapping = find_mapping(title, CROISSANT_MAPPINGS)
        
        if schema_mapping or croissant_mapping:
            report_lines.append(f"\n### {title}")
            if schema_mapping:
                report_lines.append(f"- **schema.org**: `{schema_mapping}`")
                schema_count += 1
            if croissant_mapping:
                report_lines.append(f"- **Croissant**: `{croissant_mapping}`")
                croissant_count += 1
        else:
            unmapped_count += 1
    
    # Summary
    summary = [
        "\n## Summary\n",
        f"- Questions mapped to schema.org: {schema_count}",
        f"- Questions mapped to Croissant: {croissant_count}",
        f"- Unmapped questions: {unmapped_count}",
        f"- Total questions analyzed: {schema_count + unmapped_count}"
    ]
    
    report_lines = summary + ["\n---\n"] + report_lines
    
    return "\n".join(report_lines)


def main():
    parser = argparse.ArgumentParser(
        description='Map form questions to schema.org and Croissant metadata standards'
    )
    parser.add_argument(
        '--input',
        '-i',
        required=True,
        help='Input CSV file (e.g., form_download.csv)'
    )
    parser.add_argument(
        '--output-prefix',
        '-o',
        default='mapped_form',
        help='Output file prefix (default: mapped_form)'
    )
    
    args = parser.parse_args()
    
    print(f"Loading form data from {args.input}...")
    rows = load_form_csv(args.input)
    print(f"Loaded {len(rows)} rows")
    
    print("\nCreating schema.org JSON-LD...")
    schema_jsonld = create_schema_org_jsonld(rows)
    schema_output = f"{args.output_prefix}_schema_org.json"
    write_json(schema_jsonld, schema_output)
    print(f"✓ Saved to {schema_output}")
    
    print("\nCreating Croissant metadata...")
    croissant_metadata = create_croissant_metadata(rows)
    croissant_output = f"{args.output_prefix}_croissant.json"
    write_json(croissant_metadata, croissant_output)
    print(f"✓ Saved to {croissant_output}")
    
    print("\nAdding mapping annotations to CSV...")
    mapped_rows = add_mapping_to_descriptions(rows)
    csv_output = f"{args.output_prefix}_with_mappings.csv"
    write_csv(mapped_rows, csv_output)
    print(f"✓ Saved to {csv_output}")
    
    print("\nGenerating mapping report...")
    report = generate_mapping_report(rows)
    report_output = f"{args.output_prefix}_mapping_report.md"
    Path(report_output).write_text(report, encoding='utf-8')
    print(f"✓ Saved to {report_output}")
    
    print("\n" + "="*60)
    print("Mapping complete!")
    print("="*60)
    print("\nOutput files:")
    print(f"  1. {schema_output} - schema.org JSON-LD")
    print(f"  2. {croissant_output} - Croissant metadata")
    print(f"  3. {csv_output} - CSV with mapping annotations")
    print(f"  4. {report_output} - Mapping report")
    

if __name__ == '__main__':
    main()
