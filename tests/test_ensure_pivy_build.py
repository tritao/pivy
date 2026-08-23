import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from tools.ensure_pivy_build import build_command, configure_command, ensure_build


class EnsurePivyBuildTests(TestCase):
    def test_configure_command_matches_supported_build(self):
        command = configure_command(Path("/tmp/pivy"), "/tmp/prefix")

        self.assertEqual(command[:6], ["cmake", "-G", "Ninja", "-B", "/tmp/pivy/build", "-S"])
        self.assertIn("CMAKE_BUILD_TYPE=Release", command)
        self.assertIn("PIVY_USE_SOQT:BOOL=ON", command)
        self.assertIn("QT_HOST_PATH=/tmp/prefix", command)

    def test_incremental_build_skips_configure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "build").mkdir()
            (root / "build" / "build.ninja").touch()

            with patch("tools.ensure_pivy_build.subprocess.run") as run:
                ensure_build(root, install_prefix="/tmp/prefix")

        run.assert_called_once_with(build_command(root), cwd=root, check=True)

    def test_first_build_configures_then_builds(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            with patch("tools.ensure_pivy_build.subprocess.run") as run:
                ensure_build(root, install_prefix="/tmp/prefix", jobs=4)

        self.assertEqual(run.call_count, 2)
        self.assertEqual(
            run.call_args_list[0].args[0],
            configure_command(root, "/tmp/prefix"),
        )
        self.assertEqual(run.call_args_list[1].args[0], build_command(root, 4))
