"""Allow: cd .agents/utils && python3 -m transcribe --work-dir <skill> <audio>"""

import sys
from pathlib import Path

_UTILS_ROOT = Path(__file__).resolve().parent.parent
if str(_UTILS_ROOT) not in sys.path:
    sys.path.insert(0, str(_UTILS_ROOT))

from transcribe.cli import main

if __name__ == "__main__":
    main()
