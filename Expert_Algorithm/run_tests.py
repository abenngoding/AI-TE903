"""Jalankan unit test asli tanpa instalasi paket tambahan."""

from pathlib import Path
import sys
import unittest


if __name__ == "__main__":
    directory = Path(__file__).resolve().parent
    sys.path.insert(0, str(directory / "src"))
    suite = unittest.defaultTestLoader.discover(str(directory / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
