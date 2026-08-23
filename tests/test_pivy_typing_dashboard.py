"""Tests for the multi-module typing coverage dashboard."""

import unittest

from tools.report_pivy_typing_suite import (
    build_report,
    coverage_regressions,
)


class TypingDashboardTests(unittest.TestCase):
    def test_reviewed_module_budgets_are_clean(self):
        report = build_report()

        self.assertEqual(report["regressions"], [])
        self.assertEqual(coverage_regressions(report), ())
        self.assertEqual(
            set(report["modules"]),
            {"pivy/coin.pyi", "pivy/gui/soqt.pyi", "pivy/sogui.pyi"},
        )

    def test_dashboard_preserves_parameter_triage(self):
        report = build_report()
        coin = report["modules"]["pivy/coin.pyi"]

        self.assertEqual(
            coin["opaque_parameter_families"],
            {
                "geometry": 18,
                "image/buffer": 20,
                "action": 4,
                "array/output": 11,
                "callback/handle": 35,
                "other": 121,
            },
        )


if __name__ == "__main__":
    unittest.main()
