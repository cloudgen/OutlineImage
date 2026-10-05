#!/usr/bin/env python3
# Checkout entry for the outline conversion. The package owns the function.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from OutlineImage.outline import main


if __name__ == "__main__":
    sys.exit(main())
