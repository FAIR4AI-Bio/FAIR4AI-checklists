#!/usr/bin/env bash
# Helper script to sanitize Google Form CSV files before upload.
# Removes newlines and formatting issues that cause API errors.

set -euo pipefail

# =============================================================================
# USER CONFIGURATION - Uncomment and set values here to override env vars
# =============================================================================
# INPUT_CSV="form_download.csv"
# OUTPUT_CSV="form_upload.csv"
# VERBOSE="false"

# =============================================================================
# DEFAULT VALUES - Used if not set above or in environment variables
# =============================================================================
INPUT_CSV=${INPUT_CSV:-"form_download.csv"}
OUTPUT_CSV=${OUTPUT_CSV:-"form_upload.csv"}
VERBOSE=${VERBOSE:-"false"}

# =============================================================================
# DISPLAY CONFIGURATION
# =============================================================================
echo "======================================"
echo "Form CSV Sanitization"
echo "======================================"
echo "INPUT_CSV: ${INPUT_CSV}"
echo "OUTPUT_CSV: ${OUTPUT_CSV}"
echo "VERBOSE: ${VERBOSE}"
echo "======================================"
echo ""

# Validate required variables
if [ -z "$INPUT_CSV" ]; then
    echo "Error: INPUT_CSV is not set. Please set it as an environment variable or in the script."
    exit 1
fi

if [ -z "$OUTPUT_CSV" ]; then
    echo "Error: OUTPUT_CSV is not set. Please set it as an environment variable or in the script."
    exit 1
fi

# Check if input file exists
if [ ! -f "$INPUT_CSV" ]; then
    echo "Error: Input file not found: $INPUT_CSV"
    exit 1
fi

# Run the sanitization script
if [ "$VERBOSE" = "true" ]; then
    python sanitize_form_csv.py \
        --input "${INPUT_CSV}" \
        --output "${OUTPUT_CSV}" \
        --verbose
else
    python sanitize_form_csv.py \
        --input "${INPUT_CSV}" \
        --output "${OUTPUT_CSV}"
fi
