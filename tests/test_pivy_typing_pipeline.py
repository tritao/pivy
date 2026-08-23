"""Tests for the explicit stub-generation pipeline boundaries."""

import unittest

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


if __name__ == "__main__":
    unittest.main()
