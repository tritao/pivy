import tempfile
import unittest
from pathlib import Path

import install_helpers


class InstallHelpersTests(unittest.TestCase):
    def test_write_if_changed_preserves_existing_content(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "header.h"
            path.write_text("content\n")

            self.assertFalse(install_helpers.write_if_changed(path, "content\n"))
            self.assertTrue(install_helpers.write_if_changed(path, "updated\n"))
            self.assertEqual(path.read_text(), "updated\n")

    def test_copy_and_swigify_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            interface_dir = root / "interface"
            include_dir = root / "include"
            (interface_dir / "Inventor").mkdir(parents=True)
            (include_dir / "Inventor").mkdir(parents=True)
            source = include_dir / "Inventor" / "Example.h"
            target = interface_dir / "Inventor" / "Example.h"
            source.write_text("#include <ExampleBase.h>\n")

            install_helpers.copy_and_swigify_header(
                str(interface_dir), str(include_dir), "Inventor/Example.i"
            )
            first = target.read_text()
            install_helpers.copy_and_swigify_header(
                str(interface_dir), str(include_dir), "Inventor/Example.i"
            )

            self.assertEqual(target.read_text(), first)
            self.assertEqual(first.count("%include Inventor/Example.i"), 1)


if __name__ == "__main__":
    unittest.main()
