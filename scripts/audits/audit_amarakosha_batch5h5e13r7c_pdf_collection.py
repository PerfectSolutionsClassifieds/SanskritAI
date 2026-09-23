
from __future__ import annotations

import hashlib
from pathlib import Path


REPO_ROOT = Path("/content/SanskritAI")

PDF_DIR = (
    REPO_ROOT
    / "data"
    / "raw"
    / "amarakosha"
    / "pdf"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


print("=" * 72)
print("13R-7C — Amarakośa original PDF collection audit")
print("=" * 72)

print(f"Repository root : {REPO_ROOT}")
print(f"PDF directory   : {PDF_DIR}")

if not PDF_DIR.exists():
    raise SystemExit(
        f"FAIL — PDF directory does not exist: {PDF_DIR}"
    )

pdf_files = sorted(
    path
    for path in PDF_DIR.iterdir()
    if path.is_file()
    and path.suffix.lower() == ".pdf"
)

if not pdf_files:
    raise SystemExit(
        "FAIL — no Amarakośa PDF files found."
    )

print()
print(f"PDF count : {len(pdf_files)}")
print()

for index, path in enumerate(pdf_files, start=1):

    print(f"[{index}] {path.name}")
    print(f"    size   = {path.stat().st_size:,} bytes")
    print(f"    sha256 = {sha256(path)}")
    print()

print("=" * 72)
print("RESULT: PASS — original PDF collection discovered and hashed.")
print("=" * 72)
