
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

AMARAKOSHA_TXT = REPO_ROOT / "amarakosha.txt"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def normalize_sample(text: str, limit: int = 1200) -> str:
    text = text.replace("\x00", " ")
    text = " ".join(text.split())
    return text[:limit]


print("=" * 72)
print("13R-7D — Amarakośa PDF content + provenance audit")
print("=" * 72)

print(f"Repository root : {REPO_ROOT}")
print(f"PDF directory   : {PDF_DIR}")
print(f"TXT artifact    : {AMARAKOSHA_TXT}")

if not PDF_DIR.exists():
    raise SystemExit(
        f"FAIL — PDF directory does not exist: {PDF_DIR}"
    )

if not AMARAKOSHA_TXT.exists():
    raise SystemExit(
        f"FAIL — verified Amarakośa TXT artifact missing: "
        f"{AMARAKOSHA_TXT}"
    )


# ---------------------------------------------------------------------
# TXT baseline
# ---------------------------------------------------------------------

txt_bytes = AMARAKOSHA_TXT.read_bytes()
txt_sha256 = hashlib.sha256(txt_bytes).hexdigest()

try:
    txt_text = txt_bytes.decode("utf-8")
except UnicodeDecodeError as exc:
    raise SystemExit(
        f"FAIL — amarakosha.txt is not valid UTF-8: {exc}"
    )

txt_lines = txt_text.splitlines()

print()
print("Verified TXT baseline:")
print(f"  exists       = PASS")
print(f"  size         = {len(txt_bytes):,} bytes")
print(f"  sha256       = {txt_sha256}")
print(f"  utf8         = PASS")
print(f"  lines        = {len(txt_lines):,}")

print()
print("TXT metadata sample:")

for line in txt_lines[:12]:
    print(f"  {line}")


# ---------------------------------------------------------------------
# PDF reader
# ---------------------------------------------------------------------

try:
    from pypdf import PdfReader
except ImportError:
    raise SystemExit(
        "FAIL — pypdf is not installed. "
        "Install it before running this audit."
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


# ---------------------------------------------------------------------
# PDF inspection
# ---------------------------------------------------------------------

results = []

for path in pdf_files:

    print()
    print("-" * 72)
    print(f"PDF: {path.name}")
    print("-" * 72)

    file_size = path.stat().st_size
    file_hash = sha256(path)

    print(f"size   = {file_size:,} bytes")
    print(f"sha256 = {file_hash}")

    try:
        reader = PdfReader(str(path))
    except Exception as exc:
        print(f"PDF reader : FAIL")
        print(f"error      : {type(exc).__name__}: {exc}")

        results.append(
            {
                "path": path,
                "pages": None,
                "text_pages": 0,
                "empty_pages": 0,
                "total_text_chars": 0,
                "sha256": file_hash,
                "reader_ok": False,
            }
        )

        continue

    page_count = len(reader.pages)

    print(f"PDF reader : PASS")
    print(f"page count : {page_count}")

    total_text_chars = 0
    text_pages = 0
    empty_pages = 0

    first_samples = []

    for page_number, page in enumerate(reader.pages, start=1):

        try:
            text = page.extract_text() or ""
        except Exception as exc:
            print(
                f"  page {page_number}: "
                f"text extraction ERROR "
                f"{type(exc).__name__}: {exc}"
            )
            text = ""

        text_length = len(text.strip())

        total_text_chars += text_length

        if text_length:
            text_pages += 1

            if len(first_samples) < 3:
                first_samples.append(
                    (
                        page_number,
                        normalize_sample(text),
                    )
                )
        else:
            empty_pages += 1

    print(f"text-bearing pages : {text_pages}")
    print(f"empty/no-text pages: {empty_pages}")
    print(f"extracted chars     : {total_text_chars:,}")

    if text_pages == 0:
        classification = "SCAN_OR_IMAGE_PDF"
    elif text_pages == page_count:
        classification = "TEXT_PDF"
    else:
        classification = "MIXED_TEXT_AND_IMAGE"

    print(f"classification      : {classification}")

    print()
    print("text samples:")

    if first_samples:
        for page_number, sample in first_samples:
            print(f"  page {page_number}:")
            print(f"    {sample}")
    else:
        print("  <no extractable text>")

    results.append(
        {
            "path": path,
            "pages": page_count,
            "text_pages": text_pages,
            "empty_pages": empty_pages,
            "total_text_chars": total_text_chars,
            "sha256": file_hash,
            "reader_ok": True,
            "classification": classification,
        }
    )


# ---------------------------------------------------------------------
# Provenance comparison
# ---------------------------------------------------------------------

print()
print("=" * 72)
print("13R-7D — provenance comparison")
print("=" * 72)

print()
print("Important:")
print(
    "This audit does NOT assume that the PDFs are the parent source "
    "of amarakosha.txt."
)

print(
    "It only determines whether the PDFs contain extractable "
    "Amarakośa-like textual evidence that can be investigated further."
)

print()
print("Existing TXT provenance metadata:")

provenance_lines = [
    line
    for line in txt_lines
    if (
        "bookSeriesDetails" in line
        or "publisher" in line
        or "Digital data" in line
        or "sanskrit.uohyd.ac.in" in line
        or "amarakoza" in line.lower()
        or "amarakośa" in line.lower()
    )
]

for line in provenance_lines[:20]:
    print(f"  {line}")

print()
print("PDF collection summary:")

for result in results:
    print(
        f"  {result['path'].name}"
        f" | pages={result['pages']}"
        f" | text_pages={result['text_pages']}"
        f" | chars={result['total_text_chars']:,}"
        f" | classification={result.get('classification', 'UNREADABLE')}"
    )


# ---------------------------------------------------------------------
# Conservative decision
# ---------------------------------------------------------------------

readable = [
    result
    for result in results
    if result["reader_ok"]
]

text_bearing = [
    result
    for result in readable
    if result["text_pages"] > 0
]

print()
print("=" * 72)

if not readable:
    print(
        "RESULT: BLOCKED — none of the PDFs could be read successfully."
    )
elif not text_bearing:
    print(
        "RESULT: PASS — PDFs verified, but they appear to be "
        "scan/image PDFs. Further page-image/OCR audit required."
    )
else:
    print(
        "RESULT: PASS — PDF content is accessible for further "
        "Amarakośa/provenance investigation."
    )

print("=" * 72)
