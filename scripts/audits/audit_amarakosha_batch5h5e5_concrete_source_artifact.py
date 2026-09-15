from __future__ import annotations

from pathlib import Path
import re


REPO_ROOT = Path("/content/SanskritAI")

EXCLUDED_DIR_NAMES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "tests",
}

EXCLUDED_FILE_PATTERNS = (
    re.compile(r".*\d+\.py$"),
    re.compile(r".*_G\d+\.py$"),
)

DOC_SUFFIXES = {
    ".md",
    ".rst",
}

TEXT_SUFFIXES = {
    ".txt",
    ".text",
    ".xml",
    ".tei",
    ".html",
    ".htm",
    ".json",
    ".yaml",
    ".yml",
    ".csv",
    ".toml",
}

SOURCE_TERMS = (
    "amarakosha",
    "amarakośa",
    "amara kosha",
    "amara-kośa",
    "अमरकोश",
    "अमरकोष",
)

ACQUISITION_TERMS = (
    "source_url",
    "url",
    "manifest",
    "provider",
    "acquisition",
    "acquire",
    "download",
    "repository",
    "catalog",
    "resource",
    "raw",
    "input",
)

FORMAT_TERMS = (
    "txt",
    "text",
    "plaintext",
    "unicode",
    "devanagari",
    "iast",
    "sanskrit",
    "xml",
    "tei",
    "html",
    "json",
    "csv",
)

RAW_DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]{20,}")

URL_RE = re.compile(
    r"https?://[^\s\"'<>]+|ftp://[^\s\"'<>]+"
)


def is_excluded_file(path: Path) -> bool:
    if any(part in EXCLUDED_DIR_NAMES for part in path.parts):
        return True

    name = path.name

    for pattern in EXCLUDED_FILE_PATTERNS:
        if pattern.match(name):
            return True

    if name.startswith("audit_"):
        return True

    return False


def safe_read(path: Path, limit: int = 200_000) -> str:
    try:
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )[:limit]
    except Exception:
        return ""


def relative(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def source_score(path: Path, text: str) -> int:
    lower = text.lower()
    score = 0

    # Strongest evidence: substantial Devanagari source material.
    devanagari_matches = RAW_DEVANAGARI_RE.findall(text)

    if devanagari_matches:
        score += 10
        score += min(len(devanagari_matches), 10)

    # Source identity.
    for term in SOURCE_TERMS:
        if term.lower() in lower:
            score += 3

    # Sanskrit/source-format indicators.
    for term in FORMAT_TERMS:
        if term.lower() in lower:
            score += 1

    # Avoid treating ordinary documentation as a source artifact.
    if path.suffix.lower() in DOC_SUFFIXES:
        score -= 8

    if "docs" in path.parts:
        score -= 10

    if "scripts" in path.parts:
        score -= 10

    if "audit" in path.name.lower():
        score -= 20

    return score


def classify(path: Path, text: str) -> list[str]:
    lower = text.lower()
    findings: list[str] = []

    devanagari_count = len(
        re.findall(r"[\u0900-\u097F]", text)
    )

    if devanagari_count >= 50:
        findings.append(
            f"substantial Devanagari ({devanagari_count} chars)"
        )

    if any(term.lower() in lower for term in SOURCE_TERMS):
        findings.append("Amarakośa identity")

    if any(term.lower() in lower for term in ACQUISITION_TERMS):
        findings.append("acquisition/source terminology")

    if URL_RE.search(text):
        findings.append("URL")

    if path.suffix.lower() in TEXT_SUFFIXES:
        findings.append(f"format={path.suffix.lower()}")

    return findings


print("=" * 115)
print("BATCH 5H-5E-5 — CONCRETE AMARAKOSHA SOURCE ARTIFACT IDENTIFICATION")
print("=" * 115)

print("\n" + "-" * 115)
print("1. CANDIDATE FILE SCAN")
print("-" * 115)

candidates: list[tuple[int, Path, str, str]] = []

for path in REPO_ROOT.rglob("*"):
    if not path.is_file():
        continue

    if is_excluded_file(path):
        continue

    if path.suffix.lower() not in TEXT_SUFFIXES:
        continue

    text = safe_read(path)

    if not text:
        continue

    lower = text.lower()

    if not any(term.lower() in lower for term in SOURCE_TERMS):
        continue

    score = source_score(path, text)
    findings = classify(path, text)

    candidates.append(
        (
            score,
            path,
            relative(path),
            ", ".join(findings),
        )
    )

candidates.sort(
    key=lambda item: (-item[0], item[2])
)

print(f"Candidate files: {len(candidates)}")

for score, path, rel, findings in candidates:
    print()
    print(f"FILE   : {rel}")
    print(f"SCORE  : {score}")
    print(f"EVIDENCE: {findings}")

print("\n" + "-" * 115)
print("2. STRONG SOURCE-ARTIFACT CANDIDATES")
print("-" * 115)

strong_candidates = []

for score, path, rel, findings in candidates:
    text = safe_read(path)

    devanagari_count = len(
        re.findall(r"[\u0900-\u097F]", text)
    )

    if (
        devanagari_count >= 100
        and path.suffix.lower() not in DOC_SUFFIXES
        and "docs" not in path.parts
        and "scripts" not in path.parts
    ):
        strong_candidates.append(
            (score, path, rel, devanagari_count)
        )

print(f"Strong candidates: {len(strong_candidates)}")

for score, path, rel, devanagari_count in strong_candidates:
    print()
    print(f"FILE       : {rel}")
    print(f"SCORE      : {score}")
    print(f"DEVANAGARI : {devanagari_count} chars")
    print(f"SUFFIX     : {path.suffix.lower()}")

    text = safe_read(path, limit=8_000)

    print("PREVIEW:")
    print(text[:2_000].replace("\n", " ")[:2_000])

print("\n" + "-" * 115)
print("3. URL EVIDENCE OUTSIDE AUDIT/DOCUMENTATION FILES")
print("-" * 115)

url_evidence = []

for path in REPO_ROOT.rglob("*"):
    if not path.is_file():
        continue

    if is_excluded_file(path):
        continue

    if path.suffix.lower() not in TEXT_SUFFIXES:
        continue

    if "docs" in path.parts:
        continue

    if "scripts" in path.parts:
        continue

    text = safe_read(path)

    if not text:
        continue

    if not any(term.lower() in text.lower() for term in SOURCE_TERMS):
        continue

    urls = URL_RE.findall(text)

    if urls:
        url_evidence.append(
            (relative(path), sorted(set(urls)))
        )

if not url_evidence:
    print("No non-documentation executable/source URL evidence found.")
else:
    for rel, urls in url_evidence:
        print()
        print(f"FILE: {rel}")
        for url in urls:
            print(f"  URL: {url}")

print("\n" + "-" * 115)
print("4. SOURCE ARTIFACT DECISION")
print("-" * 115)

if len(strong_candidates) == 1:
    score, path, rel, devanagari_count = strong_candidates[0]

    print("UNIQUE STRONG SOURCE ARTIFACT : FOUND")
    print(f"Artifact                     : {rel}")
    print(f"Format                       : {path.suffix.lower()}")
    print(f"Devanagari evidence          : {devanagari_count} chars")
    print()
    print("NEXT:")
    print("Inspect this exact artifact.")
    print("Do not implement parser grammar until its actual structure is inspected.")

elif len(strong_candidates) > 1:
    print("MULTIPLE STRONG SOURCE ARTIFACTS : FOUND")
    print()
    print("NEXT:")
    print("Determine which artifact is authoritative.")
    print("Do not implement parser grammar yet.")

else:
    print("NO UNIQUE STRONG SOURCE ARTIFACT IDENTIFIED")
    print()
    print("NEXT:")
    print("Trace acquisition manifests/providers/repositories.")
    print("Do not implement parser grammar yet.")

print("\n" + "-" * 115)
print("5. ARCHITECTURAL GATE")
print("-" * 115)

print("Existing acquisition architecture : PRESERVE")
print("Existing AmarakoshaParser          : PRESERVE")
print("Existing SynsetRecord/VargaRecord : PRESERVE")
print("New source model                   : NOT JUSTIFIED")
print("New provider                       : NOT JUSTIFIED")
print("New parser grammar                 : DO NOT IMPLEMENT")
print("New record types                   : NOT JUSTIFIED")

print("\nBATCH 5H-5E-5 STATUS: AUDIT COMPLETE")
print("=" * 115)
