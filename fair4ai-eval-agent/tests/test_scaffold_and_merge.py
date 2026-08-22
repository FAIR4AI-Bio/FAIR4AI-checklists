#!/usr/bin/env python
"""Tests for the two blessed eval-workflow helpers: build_response_scaffold + merge_ratings.

These back the Iteration-10 rework (see agent_and_checklist_review/PLAN_eval_efficiency_
reliability.md): the scaffold pre-fills the four verbatim fields deterministically and the
agent only produces ratings, which merge_ratings.py writes in per section.

What is checked:
  - scaffold has exactly 89 responses, each with exactly the 8 current fields, verbatim
    fields copied from CHECKLIST.csv, and empty ratings;
  - the compact --emit-guide output groups all 89 items into 9 sections and omits the
    non-rating (mapped*) columns;
  - merge validates (unknown item / invalid / missing status all rejected with no mutation),
    normalizes status spelling, supports partial batches, and is idempotent;
  - RECONSTRUCTION: scaffold + merge(ratings extracted from each committed example) +
    the example's own session/summary reproduces that example's responses EXACTLY, and the
    scorer then yields the committed scores with no warnings.

Run (stdlib only, no pip):
    python -m unittest discover -s tests
    # or: python tests/test_scaffold_and_merge.py
"""
import csv
import copy
import json
import sys
import unittest
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
EXAMPLE_OUTPUTS = AGENT_DIR / "example_outputs"
CHECKLIST = AGENT_DIR / "CHECKLIST.csv"
SCRIPTS = AGENT_DIR / "scripts"

sys.path.insert(0, str(SCRIPTS))
import build_response_scaffold as scaffold  # noqa: E402
import merge_ratings as merger  # noqa: E402
import compute_fair4ai_scores as scorer  # noqa: E402

EXPECTED_ITEM_COUNT = 89
RESPONSE_FIELDS = [
    "item", "requirement_definition", "status", "evidence",
    "notes", "recommendation", "fair_category", "ai_fair_criteria",
]
RATING_FIELDS = ["status", "evidence", "notes", "recommendation"]
EXPECTED_SECTIONS = 9


def load_checklist_verbatim():
    """{Item: {'requirement_definition','fair_category','ai_fair_criteria'}} for the 89 rows."""
    items = {}
    with open(CHECKLIST, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        crit = next(h for h in reader.fieldnames if h and h.strip().startswith("AI FAIR Criteria"))
        for row in reader:
            item = (row.get("Item") or "").strip()
            if not item:
                continue
            items[item] = {
                "requirement_definition": (row.get("Requirement Definition") or "").strip(),
                "fair_category": (row.get("FAIR category") or "").strip(),
                "ai_fair_criteria": (row.get(crit) or "").strip(),
            }
    return items


class ScaffoldTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.colmap = scaffold.load_rows(str(CHECKLIST))
        cls.doc = scaffold.build_document(cls.rows, cls.colmap)
        cls.checklist = load_checklist_verbatim()

    def test_count_and_fields(self):
        resps = self.doc["responses"]
        self.assertEqual(len(resps), EXPECTED_ITEM_COUNT)
        for i, r in enumerate(resps):
            with self.subTest(response=i):
                self.assertEqual(list(r.keys()), RESPONSE_FIELDS)

    def test_verbatim_fields_match_checklist(self):
        for r in self.doc["responses"]:
            item = r["item"].strip()
            exp = self.checklist.get(item)
            with self.subTest(item=item):
                self.assertIsNotNone(exp, f"{item!r} not in checklist")
                self.assertEqual(r["requirement_definition"], exp["requirement_definition"])
                self.assertEqual(r["fair_category"], exp["fair_category"])
                self.assertEqual(r["ai_fair_criteria"], exp["ai_fair_criteria"])

    def test_ratings_start_empty_and_scores_blank(self):
        for r in self.doc["responses"]:
            for field in RATING_FIELDS:
                self.assertEqual(r[field], "", f"{field} should start empty")
        self.assertEqual(self.doc["summary"]["fair4ai_scores"], {})

    def test_items_cover_checklist_exactly_once_in_order(self):
        items = [r["item"].strip() for r in self.doc["responses"]]
        self.assertEqual(len(items), len(set(items)), "duplicate items")
        self.assertEqual(set(items), set(self.checklist))

    def test_guide_groups_into_nine_sections_without_mapped_columns(self):
        guide = scaffold.format_guide(self.rows, self.colmap)
        self.assertEqual(guide.count("## Section:"), EXPECTED_SECTIONS)
        self.assertEqual(guide.count("### "), EXPECTED_ITEM_COUNT)
        # the mapped* / Croissant / Sub-category columns must not leak into the guide
        for noise in ("mappedEML", "mappedDataCite", "mappedSOSO", "mappedCroissant", "Croissant scope"):
            self.assertNotIn(noise, guide, f"guide should omit {noise}")

    def test_session_passthrough(self):
        d = scaffold.build_document(self.rows, self.colmap, session={"evaluation_date": "2026-01-01"})
        self.assertEqual(d["session"], {"evaluation_date": "2026-01-01"})


class MergeTest(unittest.TestCase):
    def setUp(self):
        self.scaffold = {
            "session": {},
            "responses": [
                {"item": "A", "requirement_definition": "ra", "status": "", "evidence": "",
                 "notes": "", "recommendation": "", "fair_category": "Findable",
                 "ai_fair_criteria": "Structural"},
                {"item": "B", "requirement_definition": "rb", "status": "", "evidence": "",
                 "notes": "", "recommendation": "", "fair_category": "Reusable",
                 "ai_fair_criteria": "Provenance"},
            ],
            "summary": {"strengths": [], "gaps": [], "overall_assessment": "", "fair4ai_scores": {}},
        }

    def test_partial_batch_and_status_normalization(self):
        d = copy.deepcopy(self.scaffold)
        n, total = merger.merge(d, [{"item": "A", "status": "Does Not Meet", "evidence": "x"}])
        self.assertEqual((n, total), (1, 1))
        self.assertEqual(d["responses"][0]["status"], "does not meet")
        self.assertEqual(d["responses"][1]["status"], "", "unrated item stays pending")
        self.assertEqual(set(d["responses"][0].keys()), set(RESPONSE_FIELDS), "no new keys")

    def test_dict_form_and_na(self):
        d = copy.deepcopy(self.scaffold)
        merger.merge(d, {"A": {"status": "meets"}, "B": {"status": "n/a"}})
        self.assertEqual(d["responses"][0]["status"], "meets")
        self.assertEqual(d["responses"][1]["status"], "N/A")

    def test_unknown_item_rejected_without_mutation(self):
        d = copy.deepcopy(self.scaffold)
        with self.assertRaises(ValueError):
            merger.merge(d, [{"item": "ZZZ", "status": "meets"}])
        self.assertEqual(d, self.scaffold)

    def test_invalid_status_rejects_whole_batch(self):
        d = copy.deepcopy(self.scaffold)
        with self.assertRaises(ValueError):
            merger.merge(d, [{"item": "A", "status": "meets"}, {"item": "B", "status": "sorta"}])
        self.assertEqual(d, self.scaffold, "no partial mutation when any entry is invalid")

    def test_missing_status_rejected(self):
        d = copy.deepcopy(self.scaffold)
        with self.assertRaises(ValueError):
            merger.merge(d, [{"item": "A", "evidence": "x"}])

    def test_idempotent(self):
        d1 = copy.deepcopy(self.scaffold)
        merger.merge(d1, [{"item": "A", "status": "meets", "evidence": "x"}])
        d2 = copy.deepcopy(d1)
        merger.merge(d2, [{"item": "A", "status": "meets", "evidence": "x"}])
        self.assertEqual(d1, d2)


class ReconstructionTest(unittest.TestCase):
    """scaffold + merge(ratings from each committed example) == that example."""

    def _examples(self):
        return sorted(EXAMPLE_OUTPUTS.glob("FAIR4AI_eval_*.json"))

    def test_reconstructs_each_committed_example(self):
        rows, colmap = scaffold.load_rows(str(CHECKLIST))
        for path in self._examples():
            with self.subTest(file=path.name):
                with open(path, encoding="utf-8") as f:
                    example = json.load(f)
                # ratings extracted from the example (item + the four rating fields only)
                ratings = [
                    {k: r[k] for k in ["item"] + RATING_FIELDS}
                    for r in example["responses"]
                ]
                # rebuild from scratch: scaffold + the example's own session, then merge ratings
                doc = scaffold.build_document(rows, colmap, session=example["session"])
                merger.apply_summary(doc, example["summary"])
                n, total = merger.merge(doc, ratings)
                self.assertEqual(total, EXPECTED_ITEM_COUNT, "all items should be rated")

                # responses must match the committed example exactly (keyed by item)
                rebuilt = {r["item"]: r for r in doc["responses"]}
                original = {r["item"]: r for r in example["responses"]}
                self.assertEqual(set(rebuilt), set(original))
                for item, orig in original.items():
                    self.assertEqual(rebuilt[item], orig, f"mismatch on item {item!r}")

                # and the scorer reproduces the committed scores with no warnings
                recomputed, warnings = scorer.score_document(doc)
                self.assertEqual(warnings, [], f"{path.name}: {warnings}")
                self.assertEqual(recomputed, example["summary"]["fair4ai_scores"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
