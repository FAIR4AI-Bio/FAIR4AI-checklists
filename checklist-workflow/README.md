# Google Form Automation Guide

Follow these steps to configure a service account, download its key, share your form, and run the helper scripts (`download_google_form.py` and `update_google_form.py`) to export or update Google Form content.

My notes:
- service account: google-form-app@fair4ai.iam.gserviceaccount.com
- target form: https://docs.google.com/forms/d/1gz570yBe2zDJFI__iIhLkWjK69Yy7KIkmVYiWYTQMLw/edit
- target form id: 1gz570yBe2zDJFI__iIhLkWjK69Yy7KIkmVYiWYTQMLw


## 1. Enable the Google Forms API
1. Sign in to https://console.cloud.google.com/ with a Google account that can access the form.
2. Choose or create a Google Cloud project.
3. Open **APIs & Services → Library**, search for **Google Forms API**, and click **Enable**.

## 2. Create a Service Account
1. Navigate to **APIs & Services → Credentials → Create Credentials → Service account**.
2. Provide a name (e.g., `forms-exporter`) and optional description; click **Create and Continue**.
3. Assign a role that allows Forms access:
   - Recommended: **Forms Admin (roles/forms.admin)** for read/write, or
   - **Viewer/Editor** if Forms Admin is unavailable (ensure the account can call the API).
4. Finish the wizard and note the service account email (looks like `service-name@project-id.iam.gserviceaccount.com`).

## 3. Generate and Download the JSON Key
1. Still on the service account detail page, open the **Keys** tab.
2. Click **Add Key → Create new key**, choose **JSON**, then **Create**.
3. A `*.json` file downloads immediately. Move it into your project folder, e.g., `service_account.json` beside `download_google_form.py`.
4. Treat this file like a password: do not commit it to source control or share it publicly.

## 4. Share the Google Form with the Service Account
1. Open the form in Google Forms.
2. Click the three-dot menu (top right) → **Add collaborators**.
3. Enter the service account email from Step 2 and set the access level to **Editor**.
4. Save. The service account now has permission to read or edit the form structure via the API.

## 5. Install Dependencies
Run the following in your project directory (Python 3.9+ recommended):

```bash
pip install google-api-python-client google-auth
```

## 6. Run the Download Script
Use the script’s CLI to download the form definition and emit a CSV:

```bash
python download_google_form.py \
    --form-id=YOUR_FORM_ID \
    --credentials=service_account.json \
    --output=form_questions.csv
```

- The `form-id` is the value between `/d/` and `/edit` in the form’s URL.
- `service_account.json` should match the downloaded key file path.
- `form_questions.csv` is any destination path; parent folders are created automatically.

## 7. Enable Write Access (for uploads)
To push updates back into a form you must:
1. Use the broader scope `https://www.googleapis.com/auth/forms.body` (already set in `update_google_form.py`).
2. Grant the service account a role with write privileges (e.g., **Forms Admin** or **Editor**) and keep the form shared with that account as an Editor.
3. Confirm the form ID belongs to the same account realm; otherwise sharing fails even if the API is enabled.

## 8. Upload or Modify a Form
`update_google_form.py` writes questions to an existing form using two modes:

- **Replace mode** wipes the form items first, then recreates everything from your payload.
- **Append mode** leaves existing questions and inserts the payload at the end.

### JSON input
Provide a file that already matches the Google Forms API schema:

```bash
python update_google_form.py \
    --form-id=YOUR_FORM_ID \
    --credentials=service_account.json \
    --input=form_structure.json \
    --input-format=json \
    --mode=replace
```

### CSV input
You can feed the exported `form_questions.csv` (from the downloader) back into the uploader. The script converts the rows to the API format automatically:

```bash
python update_google_form.py \
    --form-id=YOUR_FORM_ID \
    --credentials=service_account.json \
    --input=form_questions.csv \
    --input-format=csv \
    --mode=append \
    --dry-run
```

- Omit `--dry-run` to apply the changes.
- Edit the CSV to tweak titles, descriptions, options, required flags, or section markers before uploading.

## 9. Helper Shell Scripts
- `run_form_download.sh` wraps the downloader; edit the defaults (or export `FORM_ID`, `CREDS_PATH`, `OUTPUT_PATH`) and run `./run_form_download.sh`.
- `run_form_upload.sh` wraps the uploader; configure `FORM_ID`, `CREDS_PATH`, `INPUT_PATH`, `INPUT_FORMAT`, `MODE`, and optional `DRY_RUN=true`, then execute `./run_form_upload.sh`.

Both scripts expect a Bash environment (e.g., WSL) and a `python` interpreter on `PATH` that has the required dependencies.

## 10. Verify & Troubleshoot
- If the script reports `403` or `permission denied`, confirm the form is shared with the service account and that the Forms API is enabled.
- For `404` errors, double-check the `form-id` and that the account has access.
- Regenerate the JSON key if the original file is lost (delete old keys to keep access limited).
