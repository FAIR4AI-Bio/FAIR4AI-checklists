#!/usr/bin/env bash
# Helper script to call download_google_form.py with placeholder arguments.
# Update FORM_ID, CREDS, and OUTPUT before running or export them as env vars.

set -euo pipefail

# =============================================================================
# USER CONFIGURATION - Uncomment and set values here to override env vars
# =============================================================================
# FORM_ID="1vznBIkNQ09XadHn1gJ_p64WotNqrgmel_ub3aQmWytc" # working version form
# CREDS_PATH="/path/to/your/credentials.json"
# OUTPUT_PATH="form_output.csv"

# =============================================================================
# DEFAULT VALUES - Used if not set above or in environment variables
# =============================================================================
FORM_ID=${FORM_ID:-""}
CREDS_PATH=${CREDS_PATH:-""}
OUTPUT_PATH=${OUTPUT_PATH:-"form_download.csv"}

# =============================================================================
# DISPLAY CONFIGURATION
# =============================================================================
echo "======================================"
echo "Google Form Download Configuration"
echo "======================================"
echo "FORM_ID: ${FORM_ID}"
echo "CREDS_PATH: ${CREDS_PATH}"
echo "OUTPUT_PATH: ${OUTPUT_PATH}"
echo "======================================"
echo ""

# Validate required variables
if [ -z "$FORM_ID" ]; then
    echo "Error: FORM_ID is not set. Please set it as an environment variable or in the script."
    exit 1
fi

if [ -z "$CREDS_PATH" ]; then
    echo "Error: CREDS_PATH is not set. Please set it as an environment variable or in the script."
    exit 1
fi

# Run the download script
python download_google_form.py \
    --form-id "${FORM_ID}" \
    --credentials "${CREDS_PATH}" \
    --output "${OUTPUT_PATH}"