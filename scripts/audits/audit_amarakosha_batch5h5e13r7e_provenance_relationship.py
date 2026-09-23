
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from pypdf import PdfReader


REPO_ROOT = Path("/content/SanskritAI")

PDF_DIR = (
    REPO_ROOT
    / "data"
    / "raw"
    / "amarakosha"
    / "pdf"
)

AMARAKOSHA_TXT = REPO_ROOT / "amarakosha.txt"

EXPECTED_PDFS = {
    "amarfin1.pdf": {
        "kanda": 1,
        "url": (
            "https://sanskritdocuments.org/"
            "doc_z_misc_major_works/amarfin1.html"
        ),
    },
    "amarfin2.pdf": {
        "kanda": 2,
        "url": (
            "https://sanskritdocuments.org/"
            "doc_z_misc_major_works/amarfin2.html"
        ),
    },
    "amarfin3.pdf": {
        "kanda": 3,
        "url": (
            "https://sanskritdocuments.org/"
            "doc_z_misc_major_works/amarfin3.html"
        ),
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def normalize(text: str) -> str:
    text = text.replace("\x00", " ")
    return " ".join(text.split())


def extract_pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))

    parts: list[str] = []

    for page in reader.pages:
        parts.append(page.extract_text() or "")

    return "\n".join(parts)


def find_first(text: str, patterns: list[str]) -> str | None:
    lowered = text.lower()

    for pattern in patterns:
        match = re.search(
            pattern,
            lowered,
            flags=re.IGNORECASE,
        )

        if match:
            return match.group(0)

    return None


print("=" * 72)
print("13R-7E — Amarakośa provenance relationship audit")
print("=" * 72)

print(f"Repository root : {REPO_ROOT}")
print(f"PDF directory   : {PDF_DIR}")
print(f"TXT artifact    : {AMARAKOSHA_TXT}")


# ---------------------------------------------------------------------
# Preconditions
# ---------------------------------------------------------------------

if not PDF_DIR.exists():
    raise SystemExit(
        f"FAIL — PDF directory missing: {PDF_DIR}"
    )

if not AMARAKOSHA_TXT.exists():
    raise SystemExit(
        f"FAIL — Amarakośa TXT artifact missing: {AMARAKOSHA_TXT}"
    )


# ---------------------------------------------------------------------
# TXT provenance
# ---------------------------------------------------------------------

txt_bytes = AMARAKOSHA_TXT.read_bytes()

try:
    txt_text = txt_bytes.decode("utf-8")
except UnicodeDecodeError as exc:
    raise SystemExit(
        f"FAIL — amarakosha.txt UTF-8 decode failed: {exc}"
    )

txt_sha256 = hashlib.sha256(txt_bytes).hexdigest()

print()
print("-" * 72)
print("Canonical TXT artifact")
print("-" * 72)

print(f"exists : PASS")
print(f"size   : {len(txt_bytes):,}")
print(f"sha256 : {txt_sha256}")
print(f"utf8   : PASS")


txt_metadata = {}

for line in txt_text.splitlines():

    if not line.startswith(";"):
        continue

    match = re.match(
        r";([^{}]+)\{(.*)\}",
        line,
    )

    if match:
        key = match.group(1).strip()
        value = match.group(2).strip()
        txt_metadata[key] = value


print()
print("TXT provenance metadata:")

for key in (
    "title",
    "author",
    "bookFullName",
    "bookSeriesDetails",
    "publisher",
    "credits",
):

    if key in txt_metadata:
        print(f"  {key} = {txt_metadata[key]}")


scl_evidence = any(
    marker in txt_text.lower()
    for marker in (
        "sanskrit.uohyd.ac.in",
        "university of hyderabad",
        "prof. amba kulkarni",
        "shivja s. nair",
    )
)

print()
print(
    "University of Hyderabad / SCL provenance evidence : "
    f"{'PASS' if scl_evidence else 'NOT ESTABLISHED'}"
)


# ---------------------------------------------------------------------
# PDF provenance
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("Sanskrit Documents PDF provenance")
print("-" * 72)


pdf_results = []

for filename, expected in EXPECTED_PDFS.items():

    path = PDF_DIR / filename

    print()
    print(f"{filename}")
    print(f"  expected kanda = {expected['kanda']}")
    print(f"  expected URL   = {expected['url']}")

    if not path.exists():
        print("  artifact       = FAIL — missing")
        continue

    print("  artifact       = PASS")
    print(f"  size           = {path.stat().st_size:,}")
    print(f"  sha256         = {sha256(path)}")

    try:
        reader = PdfReader(str(path))
    except Exception as exc:
        print(
            f"  PDF reader     = FAIL — "
            f"{type(exc).__name__}: {exc}"
        )
        continue

    print("  PDF reader     = PASS")
    print(f"  page count     = {len(reader.pages)}")

    text = extract_pdf_text(path)
    normalized = normalize(text)

    lower = normalized.lower()

    has_amarakosha = (
        "amarakosha" in lower
        or "nAmaliNgA.anushAsan".lower() in lower
        or "नामलिङ्ग" in normalized
    )

    has_sanskrit_documents = (
        "sanskritdocuments.org" in lower
    )

    filename_match = (
        path.stem.lower()
        in lower
    )

    kanda_patterns = [
        f"chapter {expected['kanda']}",
        f"kANDa {expected['kanda']}",
        f"kāṇḍa {expected['kanda']}",
        f"काण्ड {expected['kanda']}",
    ]

    has_kanda = any(
        pattern.lower() in lower
        for pattern in kanda_patterns
    )

    print(
        "  Amarakośa text evidence = "
        f"{'PASS' if has_amarakosha else 'NOT ESTABLISHED'}"
    )

    print(
        "  Sanskrit Documents evidence = "
        f"{'PASS' if has_sanskrit_documents else 'NOT ESTABLISHED'}"
    )

    print(
        "  filename evidence = "
        f"{'PASS' if filename_match else 'NOT ESTABLISHED'}"
    )

    print(
        f"  kanda {expected['kanda']} evidence = "
        f"{'PASS' if has_kanda else 'NOT ESTABLISHED'}"
    )

    pdf_results.append(
        {
            "filename": filename,
            "kanda": expected["kanda"],
            "sha256": sha256(path),
            "pages": len(reader.pages),
            "amarakosha": has_amarakosha,
            "sanskrit_documents": has_sanskrit_documents,
            "filename_match": filename_match,
            "kanda_match": has_kanda,
        }
    )


# ---------------------------------------------------------------------
# Relationship decision
# ---------------------------------------------------------------------

print()
print("=" * 72)
print("13R-7E — relationship decision")
print("=" * 72)

all_pdfs_verified = (
    len(pdf_results) == len(EXPECTED_PDFS)
)

all_pdf_identity_verified = (
    all(
        result["amarakosha"]
        and result["sanskrit_documents"]
        and result["filename_match"]
        and result["kanda_match"]
        for result in pdf_results
    )
    if pdf_results
    else False
)

print()
print(
    "Sanskrit Documents PDF collection identity : "
    f"{'PASS' if all_pdf_identity_verified else 'NOT ESTABLISHED'}"
)

print(
    "Canonical TXT SCL provenance : "
    f"{'PASS' if scl_evidence else 'NOT ESTABLISHED'}"
)


print()
print("Relationship classification:")

if all_pdfs_verified and all_pdf_identity_verified and scl_evidence:

    print(
        "  PDF collection = VERIFIED EXTERNAL REPRESENTATION"
    )

    print(
        "  amarakosha.txt = VERIFIED SCL-DERIVED CANONICAL ARTIFACT"
    )

    print(
        "  PDF -> TXT direct derivation = NOT ESTABLISHED"
    )

    print()
    print(
        "RESULT: PASS — two provenance-bearing Amarakośa "
        "representations identified; their direct derivation "
        "relationship remains intentionally unasserted."
    )

else:

    print(
        "RESULT: BLOCKED — provenance relationship cannot yet "
        "be established conservatively."
    )

print("=" * 72)
