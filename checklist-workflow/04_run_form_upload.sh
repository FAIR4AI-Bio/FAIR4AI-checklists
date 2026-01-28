#!/usr/bin/env bash
# Helper script to call update_google_form.py with placeholder arguments.
# Update FORM_ID, CREDS_PATH, INPUT_PATH, and MODE or export them as env vars.

set -euo pipefail

# =============================================================================
# USER CONFIGURATION - Uncomment and set values here to override env vars
# =============================================================================
# FORM_ID="your_form_id_here"
# CREDS_PATH="/path/to/your/credentials.json"
# INPUT_PATH="form_upload.csv"
# INPUT_FORMAT="csv"
# MODE="replace" # options are "replace" or "append"

# =============================================================================
# DEFAULT VALUES - Used if not set above or in environment variables
# =============================================================================
FORM_ID=${FORM_ID:-""}
CREDS_PATH=${CREDS_PATH:-""}
INPUT_PATH=${INPUT_PATH:-"form_upload.csv"}
INPUT_FORMAT=${INPUT_FORMAT:-"csv"}
MODE=${MODE:-"replace"}

# =============================================================================
# DISPLAY CONFIGURATION
# =============================================================================
echo "======================================"
echo "Google Form Upload Configuration"
echo "======================================"
echo "FORM_ID: ${FORM_ID}"
echo "CREDS_PATH: ${CREDS_PATH}"
echo "INPUT_PATH: ${INPUT_PATH}"
echo "INPUT_FORMAT: ${INPUT_FORMAT}"
echo "MODE: ${MODE}"
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

if [ -z "$INPUT_PATH" ]; then
    echo "Error: INPUT_PATH is not set. Please set it as an environment variable or in the script."
    exit 1
fi

# Run the upload script
python update_google_form.py \
    --form-id "${FORM_ID}" \
    --credentials "${CREDS_PATH}" \
    --input "${INPUT_PATH}" \
    --input-format "${INPUT_FORMAT}" \
    --mode "${MODE}"