"""Peluncur lokal untuk source asli Waldo0926/animal-expert-system.

Menambahkan folder src ke pencarian modul agar CLI bisa dijalankan langsung
tanpa menginstal paket atau mengatur PYTHONPATH.
"""

from pathlib import Path
import sys


def main() -> int:
    source_directory = Path(__file__).resolve().parent / "src"
    sys.path.insert(0, str(source_directory))
    from animal_expert_system.cli import main as run_cli

    return run_cli()


if __name__ == "__main__":
    raise SystemExit(main())
