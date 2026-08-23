"""Tests for Coin/Pivy remediation ownership reporting."""

from pathlib import Path
import unittest

from tools.pivy_typing.coin_api_roadmap import COIN_API_CANDIDATE_REVIEWS
from tools.report_pivy_binding_friendliness import build_report


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class BindingFriendlinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = build_report(PROJECT_ROOT / "pivy" / "coin.pyi")

    def test_all_boundaries_and_special_contracts_are_classified(self):
        self.assertEqual(self.report["summary"]["boundaries"], 436)
        self.assertEqual(self.report["summary"]["special_contracts"], 405)
        self.assertTrue(
            all("remediation" in item for item in self.report["boundaries"])
        )
        self.assertTrue(
            all("remediation" in item for item in self.report["special_contracts"])
        )

    def test_reviewed_audits_and_provisional_queue_are_distinguished(self):
        boundaries = {
            (item["class"], item["method"], item["name"]): item
            for item in self.report["boundaries"]
        }
        self.assertEqual(
            boundaries[("SoMFFloat", "startEditing", "return")]["remediation"]["code"],
            "B",
        )
        self.assertEqual(
            boundaries[("SoGlyph", "getBitmap", "return")]["remediation"]["code"],
            "C",
        )
        self.assertEqual(
            boundaries[("SoAction", "getPathCode", "indices")]["remediation"]["code"],
            "D",
        )
        self.assertGreater(
            self.report["summary"]["boundary_confidence"]["provisional"],
            0,
        )

    def test_coin_candidates_prioritize_multi_boundary_symbols(self):
        candidates = self.report["coin_api_candidates"]
        self.assertTrue(candidates)
        self.assertEqual(candidates[0]["class"], "SoMultiTextureImageElement")
        self.assertEqual(candidates[0]["method"], "get")
        self.assertGreater(candidates[0]["score"], 1)

    def test_reviewed_coin_api_queue_has_source_backed_decisions(self):
        reviews = self.report["coin_api_reviews"]
        self.assertEqual(len(reviews), 20)
        self.assertEqual(len(reviews), len(COIN_API_CANDIDATE_REVIEWS))
        self.assertEqual(
            self.report["summary"]["reviewed_coin_api_owners"],
            {"A": 0, "B": 5, "C": 2, "D": 13},
        )
        self.assertTrue(
            all(
                item["confidence"] == "reviewed"
                and item["source_headers"]
                and item["native_signatures"]
                for item in reviews
            )
        )
        reviewed_keys = {(item["class"], item["method"]) for item in reviews}
        self.assertEqual(
            reviewed_keys,
            {(item.class_name, item.method_name) for item in COIN_API_CANDIDATE_REVIEWS},
        )

    def test_reviewed_queue_entries_override_provisional_defaults(self):
        boundaries = self.report["boundaries"]
        for review in self.report["coin_api_reviews"]:
            matching = [
                item
                for item in boundaries
                if item["class"] == review["class"]
                and item["method"] == review["method"]
            ]
            self.assertTrue(matching)
            self.assertTrue(
                all(
                    item["remediation"]["confidence"] == "reviewed"
                    and item["remediation"]["code"] == review["decision"]
                    for item in matching
                )
            )

    def test_special_contract_kinds_are_preserved(self):
        kinds = {item["kind"] for item in self.report["special_contracts"]}
        self.assertEqual(kinds, {"method", "callback"})
        self.assertEqual(
            sum(item["kind"] == "method" for item in self.report["special_contracts"]),
            327,
        )
        self.assertEqual(
            sum(item["kind"] == "callback" for item in self.report["special_contracts"]),
            78,
        )


if __name__ == "__main__":
    unittest.main()
