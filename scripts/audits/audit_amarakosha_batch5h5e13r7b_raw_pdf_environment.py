
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path("/content/SanskritAI")

RAW_AMARAKOSHA_DIR = (
    REPO_ROOT
    / "data"
    / "raw"
    / "amarakosha"
    / "pdf"
)


print("=" * 72)
print("13R-7B — Amarakośa original PDF environment audit")
print("=" * 72)

print(f"Repository root : {REPO_ROOT}")
print(f"Target PDF dir  : {RAW_AMARAKOSHA_DIR}")

if not REPO_ROOT.exists():
    raise SystemExit(
        f"FAIL — repository root does not exist: {REPO_ROOT}"
    )

RAW_AMARAKOSHA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

print()
print("Raw Amarakośa PDF directory : PASS")
print(f"  {RAW_AMARAKOSHA_DIR}")

pdf_files = sorted(
    p for p in RAW_AMARAKOSHA_DIR.iterdir()
    if p.is_file() and p.suffix.lower() == ".pdf"
)

print()
print(f"PDF files currently present : {len(pdf_files)}")

for path in pdf_files:
    print(
        f"  {path.name}"
        f" | {path.stat().st_size:,} bytes"
    )

print()
print("=" * 72)
print("RESULT: PASS — Amarakośa original-PDF audit directory established.")
print("=" * 72)
