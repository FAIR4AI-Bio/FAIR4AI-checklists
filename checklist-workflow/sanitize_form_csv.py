#!/usr/bin/env python3
"""
Sanitize Google Forms CSV for upload.

This script reads a CSV file intended for Google Forms upload and removes
formatting issues that could cause API errors, particularly:
- Newlines in displayed text fields
- Excess whitespace
- Invalid characters

Usage:
    python sanitize_form_csv.py --input form_download.csv --output form_upload.csv
"""

import argparse
import csv
import re
import sys
from pathlib import Path


def sanitize_text(text):
    """
    Remove newlines and clean up whitespace in text fields.
    
    Args:
        text: String to sanitize
        
    Returns:
        Cleaned string with newlines replaced by spaces and excess whitespace removed
    """
    if not text:
        return text
    
    # Replace newlines with spaces
    text = text.replace('\n', ' ').replace('\r', ' ')
    
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def sanitize_row(row, headers):
    """
    Sanitize a single row of form data.
    
    Args:
        row: Dictionary representing a CSV row
        headers: List of column headers
        
    Returns:
        Sanitized dictionary
    """
    sanitized = {}
    
    # Fields that should have text sanitization applied
    text_fields = ['title', 'description', 'group_title']
    
    # Options field needs special handling - preserve | delimiters
    for header in headers:
        value = row.get(header, '')
        
        if header in text_fields:
            sanitized[header] = sanitize_text(value)
        elif header == 'options':
            # For options, sanitize each option but preserve the | delimiter
            if value:
                options = value.split('|')
                cleaned_options = [sanitize_text(opt) for opt in options]
                sanitized[header] = ' | '.join(cleaned_options)
            else:
                sanitized[header] = value
        else:
            # For other fields, just strip whitespace but preserve structure
            sanitized[header] = value.strip() if value else value
    
    return sanitized


def sanitize_form_csv(input_path, output_path, verbose=False):
    """
    Read a form CSV, sanitize it, and write to output.
    
    Args:
        input_path: Path to input CSV file
        output_path: Path to output CSV file
        verbose: If True, print detailed information
        
    Returns:
        Tuple of (rows_processed, issues_found)
    """
    input_file = Path(input_path)
    output_file = Path(output_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    rows_processed = 0
    issues_found = 0
    
    with open(input_file, 'r', encoding='utf-8', newline='') as infile:
        reader = csv.DictReader(infile)
        headers = reader.fieldnames
        
        if not headers:
            raise ValueError("CSV file appears to be empty or malformed")
        
        rows = []
        for row in reader:
            original_row = row.copy()
            sanitized_row = sanitize_row(row, headers)
            rows.append(sanitized_row)
            rows_processed += 1
            
            # Check if any changes were made
            if original_row != sanitized_row:
                issues_found += 1
                if verbose:
                    print(f"Row {rows_processed}: Fixed formatting issues")
                    for key in headers:
                        if original_row.get(key) != sanitized_row.get(key):
                            print(f"  - {key}: Changed")
        
        # Write sanitized data
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
    
    return rows_processed, issues_found


def main():
    parser = argparse.ArgumentParser(
        description='Sanitize Google Forms CSV to remove newlines and formatting issues'
    )
    parser.add_argument(
        '--input',
        '-i',
        required=True,
        help='Input CSV file path'
    )
    parser.add_argument(
        '--output',
        '-o',
        required=True,
        help='Output CSV file path'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Print detailed information about changes'
    )
    
    args = parser.parse_args()
    
    try:
        print(f"Sanitizing {args.input}...")
        rows_processed, issues_found = sanitize_form_csv(
            args.input,
            args.output,
            args.verbose
        )
        
        print(f"\n✓ Success!")
        print(f"  Rows processed: {rows_processed}")
        print(f"  Rows with issues fixed: {issues_found}")
        print(f"  Output written to: {args.output}")
        
        if issues_found == 0:
            print(f"\n  No formatting issues found - file was already clean.")
        
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
