import unittest
from pathlib import Path

from tools.report_pivy_typing_domains import build_report, domain_for


class TypingDomainReportTests(unittest.TestCase):
    def test_domains_are_deterministic_and_cover_the_surface(self):
        report = build_report()
        self.assertEqual(
            tuple(report["domains"]),
            (
                "values",
                "fields",
                "scenegraph",
                "actions",
                "callbacks",
                "sensors",
                "soqt",
                "sogui",
                "other",
            ),
        )
        self.assertEqual(
            report["totals"]["annotation_sites"],
            sum(
                domain["annotation_sites"]
                for domain in report["domains"].values()
            ),
        )
        self.assertGreater(report["domains"]["fields"]["classes"], 0)
        self.assertGreater(report["domains"]["soqt"]["classes"], 0)

    def test_domain_ownership_is_stable(self):
        self.assertEqual(domain_for(Path("pivy/coin.pyi"), "SbVec3f"), "values")
        self.assertEqual(domain_for(Path("pivy/coin.pyi"), "SoMFVec3f"), "fields")
        self.assertEqual(
            domain_for(Path("pivy/coin.pyi"), "SoCallbackAction"),
            "actions",
        )
        self.assertEqual(
            domain_for(Path("pivy/gui/soqt.pyi"), "SoQtViewer"),
            "soqt",
        )


if __name__ == "__main__":
    unittest.main()
