# Google Form Automation Workflow

This workflow provides a complete set of scripts to automate downloading, sanitizing, and uploading Google Forms using a service account. The workflow is designed to work in both Windows PowerShell and WSL/Linux bash environments.

## Workflow Overview

1. **Set Environment Variables** - Configure credentials and form IDs
2. **Download Form** - Export form structure to CSV
3. **Sanitize CSV** - Clean formatting issues that cause API errors
4. **Upload Form** - Push updated form structure back to Google Forms

## Quick Start

### For WSL/Linux Users:
```bash
# 1. Set environment variables (run once)
source ./01_set_env_vars.sh

# 2. Download form
./02_run_form_download.sh

# 3. Sanitize the downloaded CSV
./03_sanitize_form_csv.sh

# 4. Upload the sanitized form
./04_run_form_upload.sh
```

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

## 6. Configure Environment Variables

### Option A: Using the Setup Scripts (Recommended)

The workflow includes scripts to set environment variables automatically:

#### For WSL/Linux:
```bash
# Copy the template and edit with your values
cp 01_set_env_vars.template.sh 01_set_env_vars.sh
nano 01_set_env_vars.sh  # Edit with your actual values

# Run with source to apply to current session and persist to ~/.bashrc
source ./01_set_env_vars.sh
```

The scripts will set the following environment variables:
- `FORM_ID` - Your Google Form ID (from the form URL)
- `CREDS_PATH` - Full path to your service account JSON key file

### Option B: Manual Configuration

You can also set variables manually or in the shell scripts:

#### WSL/Linux:
```bash
export FORM_ID="your_form_id_here"
export CREDS_PATH="/path/to/your/credentials.json"
```

Or uncomment and edit the USER CONFIGURATION section in each shell script.

## 7. Run the Download Script

### Using the Shell Script (Recommended):
```bash
./02_run_form_download.sh
```

The script will:
- Use environment variables for `FORM_ID` and `CREDS_PATH`
- Default to outputting `form_download.csv`
- Display configuration before running
- Validate required variables are set

You can override defaults by:
- Setting environment variables: `OUTPUT_PATH="my_output.csv" ./02_run_form_download.sh`
- Editing the USER CONFIGURATION section in the script

### Using the Python Script Directly:
```bash
python download_google_form.py \
    --form-id=YOUR_FORM_ID \
    --credentials=service_account.json \
    --output=form_questions.csv
```

- The `form-id` is the value between `/d/` and `/edit` in the form’s URL.
- `service_account.json` should match the downloaded key file path.
- `form_questions.csv` is any destination path; parent folders are created automatically.

## 8. Sanitize the Downloaded CSV

**Important:** Downloaded forms may contain newlines and formatting issues that cause "Displayed text cannot contain newlines" errors during upload. Always sanitize before uploading.

### Using the Shell Script (Recommended):
```bash
./03_sanitize_form_csv.sh
```

The script will:
- Read from `form_download.csv` (default)
- Write sanitized output to `form_upload.csv` (default)
- Remove newlines from text fields
- Clean excess whitespace
- Preserve data structure and delimiters

You can override defaults:
```bash
INPUT_CSV="my_form.csv" OUTPUT_CSV="cleaned.csv" VERBOSE="true" ./03_sanitize_form_csv.sh
```

### Using the Python Script Directly:
```bash
python sanitize_form_csv.py \
    --input form_download.csv \
    --output form_upload.csv \
    --verbose
```

The script will report:
- Number of rows processed
- Number of rows with issues fixed
- Detailed changes (with `--verbose` flag)

## 9. Enable Write Access (for uploads)
To push updates back into a form you must:
1. Use the broader scope `https://www.googleapis.com/auth/forms.body` (already set in `update_google_form.py`).
2. Grant the service account a role with write privileges (e.g., **Forms Admin** or **Editor**) and keep the form shared with that account as an Editor.
3. Confirm the form ID belongs to the same account realm; otherwise sharing fails even if the API is enabled.

## 10. Upload or Modify a Form

### Using the Shell Script (Recommended):
```bash
./04_run_form_upload.sh
```

The script will:
- Use environment variables for `FORM_ID` and `CREDS_PATH`
- Default to reading from `form_questions_edit1.csv`
- Use CSV format by default
- Run in "replace" mode (wipes existing questions first)
- Display configuration before running
- Validate required variables are set

You can override defaults:
```bash
INPUT_PATH="form_upload.csv" MODE="append" ./04_run_form_upload.sh
```

### Using the Python Script Directly:

`update_google_form.py` writes questions to an existing form using two modes:

- **Replace mode** wipes the form items first, then recreates everything from your payload.
- **Append mode** leaves existing questions and inserts the payload at the end.

#### JSON input
Provide a file that already matches the Google Forms API schema:

```bash
python update_google_form.py \
    --form-id=YOUR_FORM_ID \
    --credentials=service_account.json \
    --input=form_structure.json \
    --input-format=json \
    --mode=replace
```

#### CSV input
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

## 11. Files in This Workflow

### Setup Scripts
- **`01_set_env_vars.sh`** - Sets environment variables for WSL/Linux (add to .gitignore)
- **`01_set_env_vars.template.sh`** - Template for WSL/Linux setup (safe to commit)

### Workflow Scripts
- **`02_run_form_download.sh`** - Downloads form structure to CSV
- **`03_sanitize_form_csv.sh`** - Cleans CSV to prevent upload errors
- **`04_run_form_upload.sh`** - Uploads form structure from CSV

### Python Modules
- **`download_google_form.py`** - Core Python script for downloading forms
- **`update_google_form.py`** - Core Python script for uploading forms
- **`sanitize_form_csv.py`** - Removes newlines and formatting issues from CSV

### Data Files (examples)
- **`form_download.csv`** - Output from download script
- **`form_upload.csv`** - Sanitized CSV ready for upload

## 12. Shell Script Configuration

All shell scripts (02, 03, 04) follow a consistent structure with three configuration sections:

1. **USER CONFIGURATION** - Uncomment and set values to override environment variables
2. **DEFAULT VALUES** - Fallback values if not set elsewhere
3. **DISPLAY CONFIGURATION** - Shows current values when script runs

This allows flexible configuration via:
- Environment variables set by `01_set_env_vars` scripts
- One-time overrides: `INPUT_PATH="my_file.csv" ./04_run_form_upload.sh`
- Permanent script edits in the USER CONFIGURATION section

## 13. Helper Shell Scripts
## 13. Git Repository Setup

To safely work with this repository:

### Files to Add to .gitignore:
```gitignore
# Sensitive configuration files
checklist-workflow/01_set_env_vars.ps1
checklist-workflow/01_set_env_vars.sh
checklist-workflow/00_my_local_notes.txt

# Service account credentials
*.json
!package.json

# Generated data files (optional)
checklist-workflow/form_download.csv
checklist-workflow/form_upload.csv
```

### Files Safe to Commit:
- Template scripts (`*.template.sh`, `*.template.ps1`)
- All numbered shell scripts (`02_*.sh`, `03_*.sh`, `04_*.sh`)
- All Python scripts (`*.py`)
- This README (`00_README.md`)

## 14. Environment Variables Reference

| Variable | Description | Used By | Example |
|----------|-------------|---------|---------|
| `FORM_ID` | Google Form ID from URL | All scripts | `1gz570yBe...` |
| `CREDS_PATH` | Path to service account JSON | All scripts | `/path/to/key.json` |
| `OUTPUT_PATH` | Download destination file | 02_download | `form_download.csv` |
| `INPUT_CSV` | Input file for sanitization | 03_sanitize | `form_download.csv` |
| `OUTPUT_CSV` | Output file from sanitization | 03_sanitize | `form_upload.csv` |
| `INPUT_PATH` | Upload source file | 04_upload | `form_upload.csv` |
| `INPUT_FORMAT` | Format of upload file | 04_upload | `csv` or `json` |
| `MODE` | Upload mode | 04_upload | `replace` or `append` |
| `VERBOSE` | Show detailed output | 03_sanitize | `true` or `false` |

## 15. Verify & Troubleshoot

### Common Issues

#### "Displayed text cannot contain newlines" Error
- **Cause:** The downloaded CSV contains newline characters in text fields
- **Solution:** Always run `03_sanitize_form_csv.sh` before uploading

#### Environment Variables Not Set
- **Cause:** Variables not configured or terminal not restarted
- **Solution:** 
  - Run the `01_set_env_vars` script for your platform
  - Restart your terminal after running the PowerShell version
  - For bash, use `source ./01_set_env_vars.sh` (not `./01_set_env_vars.sh`)

#### Windows Path Issues in WSL
- **Cause:** Windows paths need to be converted for WSL
- **Solution:** WSL paths use `/mnt/c/` instead of `C:\`
  - Windows: `C:\Users\name\file.json`
  - WSL: `/mnt/c/Users/name/file.json`

#### Permission Errors (403)
- If the script reports `403` or `permission denied`, confirm:
  - The form is shared with the service account as Editor
  - The Google Forms API is enabled in your project
  - The service account has the correct role (Forms Admin recommended)

#### Not Found Errors (404)
- For `404` errors, double-check:
  - The `FORM_ID` is correct (from form URL between `/d/` and `/edit`)
  - The account has access to the form
  - The form exists and hasn't been deleted

#### Lost Credentials
- Regenerate the JSON key if the original file is lost
- Delete old keys in Google Cloud Console to keep access limited

### Testing Your Setup

```bash
# 1. Verify environment variables are set
echo $FORM_ID
echo $CREDS_PATH

# 2. Test download
./02_run_form_download.sh

# 3. Verify output exists
ls -lh form_download.csv

# 4. Test sanitization
./03_sanitize_form_csv.sh

# 5. Test upload (dry run first in the Python script if needed)
# Edit 04_run_form_upload.sh to add --dry-run flag for testing
```

### Getting Help

1. Check script output - all scripts display configuration before running
2. Use `--verbose` flag with sanitize script for detailed information
3. Review the form permissions in Google Forms
4. Verify API is enabled in Google Cloud Console
