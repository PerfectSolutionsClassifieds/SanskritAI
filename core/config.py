from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
DEFAULT_DICTIONARY = DATA_DIR / "dictionaries" / "basic.json"
