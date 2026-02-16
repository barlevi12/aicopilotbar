"""Test suite initialization."""

import sys
from pathlib import Path

# Add parent directory to path for imports
giid_dir = Path(__file__).parent.parent
sys.path.insert(0, str(giid_dir))
sys.path.insert(0, str(giid_dir / 'src'))
