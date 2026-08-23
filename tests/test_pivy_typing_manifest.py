"""Tests for the canonical semantic typing manifest."""

from pathlib import Path
import unittest

from tools.pivy_typing.manifest import (
    MANIFEST_SCHEMA_VERSION,
    manifest_diff,
    module_to_manifest,
    render_manifest,
)
from tools.pivy_typing.baseline import (
    COIN_MANIFEST_BASELINE,
    manifest_baseline_issues,
)
from tools.pivy_typing.model import parse_stub


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class TypingManifestTests(unittest.TestCase):
    def test_manifest_is_deterministic_and_excludes_source_locations(self):
        source = """
class Example:
    value: int

    def read(self, index: int = 0) -> str: ...
"""
        manifest = module_to_manifest(parse_stub(source, name="example"))
        rendered = render_manifest(manifest)

        self.assertEqual(manifest["schema_version"], MANIFEST_SCHEMA_VERSION)
        self.assertNotIn("line", rendered)
        self.assertEqual(rendered, render_manifest(manifest))
        self.assertIn('"return": "str"', rendered)
        self.assertNotIn('"self"', rendered)
        self.assertEqual(manifest["boundaries"], [])
        self.assertEqual(manifest["callback_contracts"], {})
        self.assertEqual(manifest["method_contracts"], [])

    def test_equivalent_annotation_spelling_has_no_semantic_diff(self):
        left = module_to_manifest(
            parse_stub(
                "class Example:\n    def read(self, value: list[int]) -> int: ...\n",
                name="example",
            )
        )
        right = module_to_manifest(
            parse_stub(
                "class Example:\n    def read(self, value: list [ int ]) -> int: ...\n",
                name="example",
            )
        )

        self.assertEqual(manifest_diff(left, right), ())

    def test_real_coin_manifest_contains_public_semantics(self):
        source = (PROJECT_ROOT / "pivy" / "coin.pyi").read_text(encoding="utf-8")
        manifest = module_to_manifest(parse_stub(source, name="pivy.coin"))

        self.assertGreater(len(manifest["classes"]), 800)
        self.assertEqual(manifest["classes"]["SoCube"]["bases"], ["SoShape"])
        self.assertEqual(
            manifest["classes"]["SoCube"]["attributes"]["width"],
            "SoSFFloat",
        )
        self.assertIn(
            "getValues",
            manifest["classes"]["SoMFDouble"]["methods"],
        )
        self.assertEqual(len(manifest["boundaries"]), 436)
        self.assertEqual(
            manifest["boundaries"][0]["source"],
            "tools/pivy_stub_typing_policy.py",
        )
        self.assertIn(
            "SoSelection.addSelectionCallback",
            manifest["callback_contracts"],
        )

    def test_real_coin_manifest_matches_reviewed_baseline(self):
        source = (PROJECT_ROOT / "pivy" / "coin.pyi").read_text(encoding="utf-8")
        manifest = module_to_manifest(parse_stub(source, name="pivy.coin"))

        self.assertEqual(manifest_baseline_issues(manifest), ())
        self.assertEqual(manifest["module"], COIN_MANIFEST_BASELINE["module"])


if __name__ == "__main__":
    unittest.main()
