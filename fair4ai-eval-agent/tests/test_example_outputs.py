#!/usr/bin/env python
"""Validation suite for the committed FAIR4AI example evaluation outputs.

These are *structural / invariant* tests, not exact-value tests: the evaluations
themselves are produced by an LLM (a Sonnet sub-agent, see tests/README.md) and are
non-deterministic, so we assert the properties that MUST hold for any valid run
against the current 89-item CHECKLIST.csv, plus that the deterministic scorer
reproduces the stored scores.

What is checked, per file in example_outputs/FAIR4AI_eval_*.json:
  - exactly 89 responses (one per checklist item)
  - every response has exactly the 8 current fields and none of the legacy ones
    (section / sub_section / question / criteria)
  - every status is one of the four canonical values
  - every response.item is a real checklist Item, all 89 are covered exactly once
  - fair_category and ai_fair_criteria are copied verbatim from the checklist row
  - summary.fair4ai_scores.{traditional_fair,ai_fair}.overall are present, non-null,
    and within [0, 1]
  - re-running compute_fair4ai_scores.score_document() reproduces the stored scores
    exactly and emits no warnings

Run (stdlib only, no pip):
    python -m unittest discover -s tests
    # or: python tests/test_example_outputs.py
"""
import csv
import json
import sys
import unittest
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
EXAMPLE_OUTPUTS = AGENT_DIR / "example_outputs"
CHECKLIST = AGENT_DIR / "CHECKLIST.csv"
SCRIPTS = AGENT_DIR / "scripts"

# Import the scoring module directly from scripts/ (stdlib-only, no install).
sys.path.insert(0, str(SCRIPTS))
import compute_fair4ai_scores as scorer  # noqa: E402

EXPECTED_ITEM_COUNT = 89
REQUIRED_FIELDS = {
    "item",
    "requirement_definition",
    "status",
    "evidence",
    "notes",
    "recommendation",
    "fair_category",
    "ai_fair_criteria",
}
LEGACY_FIELDS = {"section", "sub_section", "question", "criteria"}
VALID_STATUSES = {"meets", "partial", "does not meet", "N/A"}
# The two datasets whose outputs are committed as examples.
EXPECTED_DATASETS = ("neon_beetles", "img_tol_200m")


def load_checklist():
    """Return {Item: {'fair_category': str, 'ai_fair_criteria': str}} for the 89 rows."""
    items = {}
    with open(CHECKLIST, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        # The AI-FAIR criteria column has a long header; match it robustly.
        crit_col = next(
            (h for h in reader.fieldnames if h and h.strip().startswith("AI FAIR Criteria")),
            None,
        )
        assert crit_col, f"could not find the 'AI FAIR Criteria' column in {CHECKLIST.name}"
        for row in reader:
            item = (row.get("Item") or "").strip()
            if not item:
                continue  # blank-Item rows are skipped by the agent too
            items[item] = {
                "fair_category": (row.get("FAIR category") or "").strip(),
                "ai_fair_criteria": (row.get(crit_col) or "").strip(),
            }
    return items


def discover_output_files():
    return sorted(EXAMPLE_OUTPUTS.glob("FAIR4AI_eval_*.json"))


class ExampleOutputsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checklist = load_checklist()
        cls.files = discover_output_files()
        cls.docs = {}
        for path in cls.files:
            with open(path, encoding="utf-8") as f:
                cls.docs[path] = json.load(f)

    def test_checklist_has_expected_item_count(self):
        self.assertEqual(
            len(self.checklist),
            EXPECTED_ITEM_COUNT,
            f"CHECKLIST.csv should have {EXPECTED_ITEM_COUNT} non-blank items",
        )

    def test_example_outputs_present(self):
        self.assertTrue(self.files, f"no FAIR4AI_eval_*.json found in {EXAMPLE_OUTPUTS}")
        names = " ".join(p.name for p in self.files)
        for slug in EXPECTED_DATASETS:
            self.assertIn(
                slug, names, f"expected an example output for dataset '{slug}'"
            )

    def test_exactly_one_output_per_expected_dataset(self):
        # Guard against stale files piling up (e.g. an old + a new run of the same dataset).
        for slug in EXPECTED_DATASETS:
            matches = [p for p in self.files if slug in p.name]
            self.assertEqual(
                len(matches),
                1,
                f"expected exactly one committed example output for '{slug}', found: "
                + ", ".join(p.name for p in matches),
            )

    def test_response_count(self):
        for path, doc in self.docs.items():
            with self.subTest(file=path.name):
                self.assertEqual(len(doc.get("responses", [])), EXPECTED_ITEM_COUNT)

    def test_response_fields_are_exactly_the_current_schema(self):
        for path, doc in self.docs.items():
            for i, resp in enumerate(doc["responses"]):
                with self.subTest(file=path.name, response=i):
                    keys = set(resp)
                    self.assertEqual(
                        keys,
                        REQUIRED_FIELDS,
                        f"response[{i}] fields {sorted(keys)} != required {sorted(REQUIRED_FIELDS)}",
                    )
                    self.assertFalse(
                        keys & LEGACY_FIELDS,
                        f"response[{i}] carries dropped legacy field(s): {sorted(keys & LEGACY_FIELDS)}",
                    )

    def test_statuses_valid(self):
        for path, doc in self.docs.items():
            for i, resp in enumerate(doc["responses"]):
                with self.subTest(file=path.name, response=i):
                    self.assertIn(resp["status"], VALID_STATUSES)

    def test_items_cover_checklist_exactly_once(self):
        expected = set(self.checklist)
        for path, doc in self.docs.items():
            with self.subTest(file=path.name):
                items = [r["item"].strip() for r in doc["responses"]]
                self.assertEqual(
                    len(items), len(set(items)), "duplicate item(s) in responses"
                )
                self.assertEqual(
                    set(items),
                    expected,
                    "responses must cover exactly the 89 checklist items "
                    f"(missing: {sorted(expected - set(items))}; "
                    f"extra: {sorted(set(items) - expected)})",
                )

    def test_fair_and_criteria_copied_verbatim_from_checklist(self):
        for path, doc in self.docs.items():
            for i, resp in enumerate(doc["responses"]):
                item = resp["item"].strip()
                expected = self.checklist.get(item)
                with self.subTest(file=path.name, response=i, item=item):
                    self.assertIsNotNone(expected, f"item {item!r} not in checklist")
                    self.assertEqual(
                        resp["fair_category"].strip(),
                        expected["fair_category"],
                        "fair_category must match the checklist row verbatim",
                    )
                    self.assertEqual(
                        resp["ai_fair_criteria"].strip(),
                        expected["ai_fair_criteria"],
                        "ai_fair_criteria must match the checklist row verbatim",
                    )

    def test_overall_scores_present_and_in_range(self):
        for path, doc in self.docs.items():
            with self.subTest(file=path.name):
                fs = doc.get("summary", {}).get("fair4ai_scores", {})
                self.assertTrue(fs, "summary.fair4ai_scores is missing/empty")
                for assessment in ("traditional_fair", "ai_fair"):
                    overall = fs.get(assessment, {}).get("overall")
                    self.assertIsNotNone(
                        overall, f"{assessment}.overall must be non-null"
                    )
                    self.assertGreaterEqual(overall, 0.0)
                    self.assertLessEqual(overall, 1.0)

    def test_scores_are_reproducible_and_clean(self):
        for path, doc in self.docs.items():
            with self.subTest(file=path.name):
                stored = doc.get("summary", {}).get("fair4ai_scores")
                recomputed, warnings = scorer.score_document(doc)
                self.assertEqual(
                    warnings,
                    [],
                    f"scorer emitted warnings for {path.name}: {warnings}",
                )
                self.assertEqual(
                    recomputed,
                    stored,
                    f"stored summary.fair4ai_scores for {path.name} does not match a fresh "
                    "compute_fair4ai_scores.score_document() run",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
