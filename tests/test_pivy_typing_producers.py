"""Tests for backend-independent producer comparison."""

from pathlib import Path
import tempfile
import unittest

from tools.compare_pivy_typing_producers import (
    classify_difference,
    compare_producers,
)


class ProducerComparisonTests(unittest.TestCase):
    def test_difference_categories_are_manifest_oriented(self):
        self.assertEqual(
            classify_difference("$.boundaries[0].category: changed"),
            "intentional-boundary",
        )
        self.assertEqual(
            classify_difference("$.callback_contracts.Foo.bar: changed"),
            "binding-metadata",
        )
        self.assertEqual(
            classify_difference("$.classes.Foo.methods.bar: changed"),
            "python-api",
        )

    def test_current_generated_producer_matches_reference(self):
        project_root = Path(__file__).resolve().parent.parent
        reference = project_root / "pivy" / "coin.pyi"
        candidate = project_root / "build" / "pivy" / "coin.pyi"

        result = compare_producers(reference, candidate)

        self.assertTrue(result["equivalent"])
        self.assertEqual(result["differences"], [])

    def test_semantic_difference_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "reference.pyi"
            candidate = Path(directory) / "candidate.pyi"
            reference.write_text("class Example:\n    value: int\n", encoding="utf-8")
            candidate.write_text("class Example:\n    value: str\n", encoding="utf-8")

            result = compare_producers(reference, candidate)

        self.assertFalse(result["equivalent"])
        self.assertEqual(
            result["categories"], {"manifest": 1, "python-api": 1}
        )


if __name__ == "__main__":
    unittest.main()
