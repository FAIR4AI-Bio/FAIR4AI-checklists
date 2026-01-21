#!/usr/bin/env bash
# Helper script to call download_google_form.py with placeholder arguments.
# Update FORM_ID, CREDS, and OUTPUT before running or export them as env vars.

set -euo pipefail

FORM_ID=${FORM_ID:-"1AJKy7ZYi67P81KF5MCK_w5T2YZj8iMiDXRl2606yYzI"}
CREDS_PATH=${CREDS_PATH:-"fair4ai-f47a43a6a4df.json"}
OUTPUT_PATH=${OUTPUT_PATH:-"form_test.csv"}

python download_google_form.py \
    --form-id "${FORM_ID}" \
    --credentials "${CREDS_PATH}" \
    --output "${OUTPUT_PATH}"

python download_google_form.py \
    --form-id 1AJKy7ZYi67P81KF5MCK_w5T2YZj8iMiDXRl2606yYzI \
    --credentials fair4ai-f47a43a6a4df.json \
    --output form_test.csv