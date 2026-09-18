from __future__ import annotations

import hashlib
import sys
from pathlib import Path


REPO_ROOT = Path("/content/SanskritAI")
ARTIFACT = REPO_ROOT / "amarakosha.txt"


def header(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


header("BATCH 5H-5E-13R-6B — VERIFIED AMARAKOSHA ARTIFACT")

# -------------------------------------------------------------------------
# 1. Repository bootstrap
# -------------------------------------------------------------------------

header("1. REPOSITORY BOOTSTRAP")

print("Repository :", REPO_ROOT)
print("Exists     :", REPO_ROOT.exists())

if not REPO_ROOT.exists():
    print("RESULT : FAIL — repository does not exist")
    raise SystemExit(1)

if str(REPO_ROOT.parent) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT.parent))

try:
    import SanskritAI

    print("SanskritAI import : PASS")
    print("SanskritAI.__file__ :", SanskritAI.__file__)
except Exception as exc:
    print("SanskritAI import : FAIL")
    print("error :", repr(exc))
    raise SystemExit(1)


# -------------------------------------------------------------------------
# 2. Concrete artifact
# -------------------------------------------------------------------------

header("2. CONCRETE ARTIFACT")

print("Artifact path :", ARTIFACT)
print("Exists        :", ARTIFACT.exists())
print("Is file       :", ARTIFACT.is_file())

if not ARTIFACT.exists() or not ARTIFACT.is_file():
    print("RESULT : FAIL — amarakośa.txt is not available")
    raise SystemExit(1)


# -------------------------------------------------------------------------
# 3. File metadata
# -------------------------------------------------------------------------

header("3. ARTIFACT METADATA")

stat = ARTIFACT.stat()

print("Filename       :", ARTIFACT.name)
print("Suffix         :", ARTIFACT.suffix)
print("Size           :", stat.st_size, "bytes")
print("Absolute path  :", ARTIFACT.resolve())


# -------------------------------------------------------------------------
# 4. UTF-8 validation
# -------------------------------------------------------------------------

header("4. UTF-8 VALIDATION")

try:
    text = ARTIFACT.read_text(encoding="utf-8")
    print("UTF-8 decoding : PASS")
    print("Character count:", len(text))
    print("Line count     :", len(text.splitlines()))
except UnicodeDecodeError as exc:
    print("UTF-8 decoding : FAIL")
    print("error :", repr(exc))
    raise SystemExit(1)


# -------------------------------------------------------------------------
# 5. Content preview
# -------------------------------------------------------------------------

header("5. CONTENT PREVIEW")

lines = text.splitlines()

print("First non-empty lines:")

shown = 0

for line_number, line in enumerate(lines, start=1):
    if not line.strip():
        continue

    print(f"{line_number}: {line[:300]}")
    shown += 1

    if shown >= 10:
        break


# -------------------------------------------------------------------------
# 6. SHA-256
# -------------------------------------------------------------------------

header("6. ARTIFACT CHECKSUM")

digest = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest()

print("SHA-256 :", digest)


# -------------------------------------------------------------------------
# 7. Git tracking
# -------------------------------------------------------------------------

header("7. GIT TRACKING")

import subprocess

result = subprocess.run(
    ["git", "ls-files", "--error-unmatch", str(ARTIFACT.relative_to(REPO_ROOT))],
    cwd=REPO_ROOT,
    text=True,
    capture_output=True,
)

tracked = result.returncode == 0

print("Git tracked :", tracked)

if tracked:
    print("Git path    :", result.stdout.strip())
else:
    print("Git path    : NOT TRACKED")


# -------------------------------------------------------------------------
# 8. Final contract
# -------------------------------------------------------------------------

header("8. 13R-6 ARTIFACT CONTRACT")

print("source_id     : amarakosha")
print("name          : Amarakośa")
print("source_type   : SourceType.LEXICON")
print("source_format : SourceFormat.TXT")
print("status        : SourceStatus.REGISTERED")
print("local_path    :", ARTIFACT)
print("download_urls : []")
print()
print("Remote provenance : NOT asserted")
print("Publisher         : NOT asserted")
print("Author             : NOT asserted")
print("Version            : NOT asserted")
print("Edition            : NOT asserted")


header("9. RESULT")

print("RESULT : PASS — concrete Amarakośa artifact verified.")
print()
print("13R-6 may now proceed to the canonical CorpusSource declaration.")
print("No production files were modified.")
