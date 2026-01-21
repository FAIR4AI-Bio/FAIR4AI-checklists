"""Update a Google Form by overwriting or appending items defined in a JSON file.

Example JSON payload (matches Google Forms API structure):
{
  "info": {
    "title": "My Survey",
    "description": "Demo form"
  },
  "items": [
    {
      "title": "What is your name?",
      "questionItem": {
        "question": {
          "required": true,
          "textQuestion": {}
        }
      }
    },
    {
      "title": "Pick a color",
      "questionItem": {
        "question": {
          "choiceQuestion": {
            "type": "RADIO",
            "options": [
              {"value": "Red"},
              {"value": "Blue"}
            ]
          }
        }
      }
    }
  ]
}

Usage:
    python update_google_form.py \
        --form-id=<FORM_ID> \
        --credentials=service_account.json \
        --input=form_structure.json \
        --input-format=json \
        --mode=replace

    python update_google_form.py \
        --form-id=<FORM_ID> \
        --credentials=service_account.json \
        --input=form_questions.csv \
        --input-format=csv \
        --mode=append

Modes:
    replace - deletes all existing items before inserting payload items.
    append  - leaves existing items and inserts payload items at the end.
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
from typing import Any, Dict, List, Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/forms.body"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write questions to a Google Form.")
    parser.add_argument("--form-id", required=True, help="Target Google Form ID.")
    parser.add_argument("--credentials", required=True, help="Path to the service-account JSON key.")
    parser.add_argument("--input", required=True, help="Path to JSON or CSV payload describing the form items.")
    parser.add_argument(
        "--input-format",
        choices=["json", "csv"],
        help="Parse the --input file as JSON or CSV (defaults to file extension).",
    )
    parser.add_argument(
        "--mode",
        choices=["replace", "append"],
        default="append",
        help="replace deletes all existing items first; append adds items at the end.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the API requests without sending them.",
    )
    return parser.parse_args()


def build_forms_client(credentials_path: str):
    creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    return build("forms", "v1", credentials=creds, cache_discovery=False)


def infer_input_format(path: str, override: Optional[str]) -> str:
    if override:
        return override
    suffix = pathlib.Path(path).suffix.lower()
    if suffix == ".csv":
        return "csv"
    return "json"


def load_payload(path: str, *, input_format: str) -> Dict[str, Any]:
    if input_format == "json":
        data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        if "items" not in data or not isinstance(data["items"], list):
            raise ValueError("Input JSON must contain an 'items' list matching the Forms API schema.")
        return data
    return csv_to_payload(path)


def csv_to_payload(path: str) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    with pathlib.Path(path).open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            item = csv_row_to_item(row)
            if item:
                rows.append(item)
    if not rows:
        raise ValueError("CSV input did not contain any recognizable items.")
    return {"items": rows}


def csv_row_to_item(row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    question_type_raw = (row.get("question_type") or "").strip()
    if not question_type_raw:
        return None

    title = row.get("title") or row.get("group_title") or row.get("section") or "Untitled item"
    description = row.get("description") or ""

    if question_type_raw.upper() == "SECTION_BREAK":
        item: Dict[str, Any] = {"pageBreakItem": {}}
        if title:
            item["title"] = title
        if description:
            item["description"] = description
        return item

    if question_type_raw.lower() == "textitem":
        item = {"textItem": {}}
        if title:
            item["title"] = title
        if description:
            item["description"] = description
        return item

    question: Dict[str, Any] = {"required": to_bool(row.get("required"))}
    validation = parse_validation(row.get("validation"))
    if validation:
        question["validation"] = validation

    block_key, block_payload = build_question_block(question_type_raw, row)
    question[block_key] = block_payload

    item = {
        "title": title,
        "description": description,
        "questionItem": {"question": question},
    }
    return item


def build_question_block(question_type: str, row: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
    key = question_type
    payload: Dict[str, Any] = {}

    if question_type == "choiceQuestion":
        options = parse_options(row.get("options"))
        choice_type = (row.get("choice_type") or "RADIO").upper()
        payload = {
            "type": choice_type,
            "options": [{"value": option} for option in options] if options else [],
        }
    elif question_type == "textQuestion":
        payload = {"paragraph": to_bool(row.get("paragraph"))}
    else:
        payload = {}

    return key, payload


def parse_options(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    cleaned = raw.replace("\r", "").strip()
    if not cleaned:
        return []
    if "|" in cleaned:
        parts = cleaned.split("|")
    elif "," in cleaned:
        parts = cleaned.split(",")
    else:
        parts = cleaned.split("\n")
    return [part.strip() for part in parts if part.strip()]


def parse_validation(value: Optional[str]) -> Optional[Dict[str, Any]]:
    if not value:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return None
    if isinstance(parsed, dict):
        return parsed
    return None


def to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def fetch_existing_items(client, form_id: str) -> List[Dict[str, Any]]:
    form = client.forms().get(formId=form_id).execute()
    return form.get("items", [])


def batch_request(client, form_id: str, requests: List[Dict[str, Any]], *, dry_run: bool) -> Optional[Dict[str, Any]]:
    if not requests:
        return None
    if dry_run:
        print(json.dumps({"formId": form_id, "requests": requests}, indent=2))
        return None
    return client.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()


def delete_all_items(client, form_id: str, items: List[Dict[str, Any]], *, dry_run: bool) -> None:
    requests = []
    for idx in reversed(range(len(items))):
        requests.append({"deleteItem": {"location": {"index": idx}}})
    batch_request(client, form_id, requests, dry_run=dry_run)


def add_items(client, form_id: str, items: List[Dict[str, Any]], start_index: int, *, dry_run: bool) -> None:
    for offset, item in enumerate(items):
        location_index = start_index + offset
        requests = [
            {
                "createItem": {
                    "item": item,
                    "location": {"index": location_index},
                }
            }
        ]
        batch_request(client, form_id, requests, dry_run=dry_run)


def update_form_info(client, form_id: str, info: Dict[str, Any], *, dry_run: bool) -> None:
    clean_info = {k: v for k, v in info.items() if v is not None}
    if not clean_info:
        return
    update_mask = ",".join(clean_info.keys())
    requests = [
        {
            "updateFormInfo": {
                "info": clean_info,
                "updateMask": update_mask,
            }
        }
    ]
    batch_request(client, form_id, requests, dry_run=dry_run)


def main() -> None:
    args = parse_args()
    input_format = infer_input_format(args.input, args.input_format)
    payload = load_payload(args.input, input_format=input_format)

    try:
        client = build_forms_client(args.credentials)
        existing_items = fetch_existing_items(client, args.form_id)

        if args.mode == "replace":
            delete_all_items(client, args.form_id, existing_items, dry_run=args.dry_run)
            start_index = 0
        else:
            start_index = len(existing_items)

        info = payload.get("info") or {}
        if info:
            update_form_info(client, args.form_id, info, dry_run=args.dry_run)

        add_items(client, args.form_id, payload["items"], start_index, dry_run=args.dry_run)
        if args.dry_run:
            print("Dry run complete. No changes applied.")
        else:
            print("Form update completed successfully.")
    except HttpError as exc:
        print(f"API error: {exc}")
    except Exception as exc:  # noqa: BLE001
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
