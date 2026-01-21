#!/usr/bin/env bash
# Helper script to call update_google_form.py with placeholder arguments.
# Update FORM_ID, CREDS_PATH, INPUT_PATH, and MODE or export them as env vars.

set -euo pipefail

FORM_ID=${FORM_ID:-"1gz570yBe2zDJFI__iIhLkWjK69Yy7KIkmVYiWYTQMLw"}
CREDS_PATH=${CREDS_PATH:-"fair4ai-f47a43a6a4df.json"}
INPUT_PATH=${INPUT_PATH:-"form_questions_edit1.csv"}
INPUT_FORMAT=${INPUT_FORMAT:-"csv"}
MODE=${MODE:-"replace"}

python update_google_form.py \
    --form-id 1AJKy7ZYi67P81KF5MCK_w5T2YZj8iMiDXRl2606yYzI \
    --credentials fair4ai-f47a43a6a4df.json \
    --input form_test.csv \
    --input-format csv \
    --mode replace

python update_google_form.py \
    --form-id 1AJKy7ZYi67P81KF5MCK_w5T2YZj8iMiDXRl2606yYzI \
    --credentials fair4ai-f47a43a6a4df.json \
    --input form_test.csv \
    --input-format csv \
    --mode append