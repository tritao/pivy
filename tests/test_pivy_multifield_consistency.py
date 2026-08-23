import unittest
from pathlib import Path

from tools.check_pivy_multifield_consistency import audit


class MultifieldConsistencyTests(unittest.TestCase):
    def test_generated_coin_stubs_cover_every_multifield_operation(self):
        errors, count = audit(Path("pivy/coin.pyi"))
        self.assertEqual(errors, [])
        self.assertGreaterEqual(count, 20)


if __name__ == "__main__":
    unittest.main(verbosity=2)
