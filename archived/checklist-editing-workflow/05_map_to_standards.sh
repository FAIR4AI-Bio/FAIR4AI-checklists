#!/usr/bin/env bash
# Helper script to map form questions to schema.org and Croissant metadata standards.
# Maps questions from a CSV file and generates JSON-LD, Croissant metadata, and annotated CSV.

set -euo pipefail

# =============================================================================
# USER CONFIGURATION - Uncomment and set values here to override env vars
# =============================================================================
# INPUT_CSV="form_download.csv"
# OUTPUT_PREFIX="mapped_form"

# =============================================================================
# DEFAULT VALUES - Used if not set above or in environment variables
# =============================================================================
INPUT_CSV=${INPUT_CSV:-"form_download.csv"}
OUTPUT_PREFIX=${OUTPUT_PREFIX:-"mapped_form"}

# =============================================================================
# DISPLAY CONFIGURATION
# =============================================================================
echo "======================================"
echo "Metadata Standards Mapping"
echo "======================================"
echo "INPUT_CSV: ${INPUT_CSV}"
echo "OUTPUT_PREFIX: ${OUTPUT_PREFIX}"
echo "======================================"
echo ""

# Validate required variables
if [ -z "$INPUT_CSV" ]; then
    echo "Error: INPUT_CSV is not set. Please set it as an environment variable or in the script."
    exit 1
fi

if [ -z "$OUTPUT_PREFIX" ]; then
    echo "Error: OUTPUT_PREFIX is not set. Please set it as an environment variable or in the script."
    exit 1
fi

# Check if input file exists
if [ ! -f "$INPUT_CSV" ]; then
    echo "Error: Input file not found: $INPUT_CSV"
    exit 1
fi

# Run the mapping script
python map_to_standards.py \
    --input "${INPUT_CSV}" \
    --output-prefix "${OUTPUT_PREFIX}"
