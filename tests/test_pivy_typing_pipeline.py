"""Tests for the explicit stub-generation pipeline boundaries."""

import unittest

from tools.generate_pivy_stubs import (
    is_excluded_cpp_signature,
    parse_swig_signature,
)
from tools.pivy_stub_typing_policy import EXCLUDED_CPP_SIGNATURES
from tools.pivy_typing.pipeline import Stage, run_pipeline


class StubPipelineTests(unittest.TestCase):
    def test_stages_run_in_declared_order(self):
        result = run_pipeline(
            "start",
            (
                Stage("first", lambda text: text + ":first"),
                Stage("second", lambda text: text + ":second"),
            ),
        )

        self.assertEqual(result.text, "start:first:second")
        self.assertEqual(result.completed_stages, ("first", "second"))


class ExcludedSignatureTests(unittest.TestCase):
    def test_only_deprecated_bsp_overloads_are_excluded(self):
        deprecated_points = parse_swig_signature(
            "findPoints(SbBSPTree self, SbSphere sphere, "
            "SbList< int > & array)",
            "findPoints",
        )
        supported_points = parse_swig_signature(
            "findPoints(SbBSPTree self, SbSphere sphere, SbIntList array)",
            "findPoints",
        )
        deprecated_closest = parse_swig_signature(
            "findClosest(SbBSPTree self, SbSphere sphere, "
            "SbList< int > & array) -> int",
            "findClosest",
        )

        self.assertIsNotNone(deprecated_points)
        self.assertIsNotNone(supported_points)
        self.assertIsNotNone(deprecated_closest)
        self.assertTrue(
            is_excluded_cpp_signature("SbBSPTree", "findPoints", deprecated_points)
        )
        self.assertFalse(
            is_excluded_cpp_signature("SbBSPTree", "findPoints", supported_points)
        )
        self.assertTrue(
            is_excluded_cpp_signature("SbBSPTree", "findClosest", deprecated_closest)
        )

    def test_exclusions_have_reviewable_reasons(self):
        self.assertEqual(
            set(EXCLUDED_CPP_SIGNATURES),
            {
                ("SbBSPTree", "findPoints"),
                ("SbBSPTree", "findClosest"),
            },
        )
        self.assertTrue(all(rule.reason for rule in EXCLUDED_CPP_SIGNATURES.values()))


if __name__ == "__main__":
    unittest.main()
