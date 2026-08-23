from pathlib import Path
from unittest import TestCase

from tools.check_pivy_typing_compatibility import check_snapshot


class TypingCompatibilityTests(TestCase):
    def test_checked_in_snapshot_matches_stubs(self):
        self.assertEqual(check_snapshot(), [])

    def test_snapshot_reports_missing_module_stub(self):
        project_root = Path(__file__).resolve().parent.parent
        snapshot = project_root / "tests" / "pivy_typing_compatibility.json"
        errors = check_snapshot(snapshot, project_root / "does-not-exist")

        self.assertTrue(any("missing stub" in error for error in errors))
