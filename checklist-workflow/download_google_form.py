"""Download a Google Form via the Forms API and save question metadata as CSV.

Usage:
    python download_google_form.py \
        --form-id=<FORM_ID> \
        --credentials=service_account.json \
        --output=form_questions.csv

Prerequisites:
    1. Enable the Google Forms API in your Google Cloud project.
    2. Create a service account with the Forms API scopes listed below.
    3. Share the target Google Form with the service account email and grant editor access.
    4. Install dependencies: pip install google-api-python-client google-auth
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
from typing import Any, Dict, Iterable, List, Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/forms.body.readonly"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download a Google Form definition and convert it to a tabular CSV file."
    )
    parser.add_argument(
        "--form-id",
        required=True,
        help="The ID of the Google Form (look for the IDs between /d/ and /edit in the form URL).",
    )
    parser.add_argument(
        "--credentials",
        required=True,
        help="Path to the service-account JSON credentials with Forms API access.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Destination CSV path. Parent directories will be created if needed.",
    )
    return parser.parse_args()


def build_forms_client(credentials_path: str):
    creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    return build("forms", "v1", credentials=creds, cache_discovery=False)


def describe_question_type(question: Dict[str, Any]) -> str:
    for key, value in question.items():
        if key.endswith("Question") and isinstance(value, dict):
            return key
    return "UNKNOWN"


def extract_choice_options(question: Dict[str, Any]) -> str:
    choice_block = question.get("choiceQuestion")
    if not choice_block:
        return ""

    options = [opt.get("value", "") for opt in choice_block.get("options", [])]
    return " | ".join(filter(None, options))


def format_validation(validation: Optional[Dict[str, Any]]) -> str:
    if not validation:
        return ""
    simplified = {
        "type": validation.get("type"),
        "criteria": validation.get("criterion"),
    }
    return json.dumps({k: v for k, v in simplified.items() if v is not None}, ensure_ascii=True)


def question_row(
    *,
    item_index: str,
    item_meta: Dict[str, Any],
    question: Dict[str, Any],
    section_label: str,
    group_title: Optional[str],
) -> Dict[str, Any]:
    question_type = describe_question_type(question)
    return {
        "position": item_index,
        "section": section_label,
        "group_title": group_title or "",
        "item_id": item_meta.get("itemId", ""),
        "question_id": question.get("questionId", ""),
        "title": item_meta.get("title", ""),
        "description": item_meta.get("description", ""),
        "question_type": question_type,
        "required": question.get("required", False),
        "options": extract_choice_options(question),
        "validation": format_validation(question.get("validation")),
    }


def flatten_items(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    current_section = "Form Root"
    section_counter = 1

    for idx, item in enumerate(items, start=1):
        position = str(idx)

        if "pageBreakItem" in item:
            current_section = item.get("title") or f"Section {section_counter}"
            section_counter += 1
            rows.append(
                {
                    "position": position,
                    "section": current_section,
                    "group_title": "",
                    "item_id": item.get("itemId", ""),
                    "question_id": "",
                    "title": item.get("title", ""),
                    "description": item.get("description", ""),
                    "question_type": "SECTION_BREAK",
                    "required": False,
                    "options": "",
                    "validation": "",
                }
            )
            continue

        if "questionItem" in item:
            rows.append(
                question_row(
                    item_index=position,
                    item_meta=item,
                    question=item["questionItem"].get("question", {}),
                    section_label=current_section,
                    group_title=None,
                )
            )
            continue

        group = item.get("questionGroupItem")
        if group:
            questions = group.get("questionGroup", {}).get("questions", [])
            for sub_idx, question in enumerate(questions, start=1):
                rows.append(
                    question_row(
                        item_index=f"{position}.{sub_idx}",
                        item_meta=item,
                        question=question,
                        section_label=current_section,
                        group_title=item.get("title"),
                    )
                )
            continue

        rows.append(
            {
                "position": position,
                "section": current_section,
                "group_title": "",
                "item_id": item.get("itemId", ""),
                "question_id": "",
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "question_type": next(iter(item.keys() - {"itemId", "title", "description"}), "UNKNOWN"),
                "required": False,
                "options": "",
                "validation": "",
            }
        )

    return rows


def write_csv(rows: List[Dict[str, Any]], output_path: str) -> None:
    if not rows:
        raise ValueError("No rows extracted from the form definition.")

    path = pathlib.Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    args = parse_args()
    try:
        client = build_forms_client(args.credentials)
        form = client.forms().get(formId=args.form_id).execute()
        rows = flatten_items(form.get("items", []))
        write_csv(rows, args.output)
        print(f"Saved {len(rows)} rows to {args.output}")
    except HttpError as exc:
        print(f"API error: {exc}")
    except Exception as exc:  # noqa: BLE001 - surface unexpected issues
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
