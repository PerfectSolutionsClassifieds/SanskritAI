from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path("/content/SanskritAI")
REPO_PARENT = REPO_ROOT.parent

if str(REPO_PARENT) not in sys.path:
    sys.path.insert(0, str(REPO_PARENT))


TARGET = (
    REPO_ROOT
    / "acquisition"
    / "detectors"
    / "source_format_detector.py"
)

BACKUP = TARGET.with_suffix(
    ".py.5h5e10r4.corrective.bak"
)


print("=" * 120)
print(
    "BATCH 5H-5E-10R-4A — "
    "CORRECTED MINIMAL SOURCEFORMAT DETECTOR REPAIR"
)
print("=" * 120)


# ------------------------------------------------------------------
# 1. Target
# ------------------------------------------------------------------

print()
print("-" * 120)
print("1. TARGET")
print("-" * 120)

print(f"Target : {TARGET}")
print(f"Exists : {TARGET.exists()}")

if not TARGET.exists():
    raise FileNotFoundError(TARGET)


# ------------------------------------------------------------------
# 2. Read current source
# ------------------------------------------------------------------

source = TARGET.read_text(encoding="utf-8")


# ------------------------------------------------------------------
# 3. Current TEI-related references
# ------------------------------------------------------------------

print()
print("-" * 120)
print("2. CURRENT TEI REFERENCES")
print("-" * 120)

for line_no, line in enumerate(source.splitlines(), start=1):
    if "TEI" in line.upper():
        print(f"{line_no:4d}: {line}")


# ------------------------------------------------------------------
# 4. Exact-state diagnosis
# ------------------------------------------------------------------

print()
print("-" * 120)
print("3. EXACT-STATE DIAGNOSIS")
print("-" * 120)

bad_double = source.count("SourceFormat.TEI_XML_XML")

# IMPORTANT:
# Use regex negative lookahead so SourceFormat.TEI_XML is NOT
# accidentally classified as SourceFormat.TEI.
stale_exact_matches = re.findall(
    r"SourceFormat\.TEI(?!_XML)",
    source,
)

print(
    "SourceFormat.TEI_XML_XML occurrences : "
    f"{bad_double}"
)

print(
    "Exact stale SourceFormat.TEI occurrences : "
    f"{len(stale_exact_matches)}"
)

print()
print("Safety check:")
print(
    "  SourceFormat.TEI_XML is NOT treated as "
    "SourceFormat.TEI."
)


# ------------------------------------------------------------------
# 5. Backup current production file
# ------------------------------------------------------------------

print()
print("-" * 120)
print("4. BACKUP CURRENT PRODUCTION FILE")
print("-" * 120)

shutil.copy2(TARGET, BACKUP)

print(f"Backup : {BACKUP}")
print(f"Exists : {BACKUP.exists()}")


# ------------------------------------------------------------------
# 6. Minimal exact repair
# ------------------------------------------------------------------

print()
print("-" * 120)
print("5. MINIMAL EXACT REPAIR")
print("-" * 120)

repaired = source

if bad_double:
    print(
        "Repairing invalid token:"
    )
    print(
        "  SourceFormat.TEI_XML_XML"
    )
    print(
        "  -> SourceFormat.TEI_XML"
    )

    repaired = repaired.replace(
        "SourceFormat.TEI_XML_XML",
        "SourceFormat.TEI_XML",
    )


# Recalculate exact stale references AFTER the double-token repair.
stale_exact_matches_after_double_fix = re.findall(
    r"SourceFormat\.TEI(?!_XML)",
    repaired,
)

if stale_exact_matches_after_double_fix:
    print()
    print(
        "Repairing exact stale token:"
    )
    print(
        "  SourceFormat.TEI"
    )
    print(
        "  -> SourceFormat.TEI_XML"
    )

    repaired = re.sub(
        r"SourceFormat\.TEI(?!_XML)",
        "SourceFormat.TEI_XML",
        repaired,
    )


# ------------------------------------------------------------------
# 7. Write only if necessary
# ------------------------------------------------------------------

if repaired != source:
    TARGET.write_text(
        repaired,
        encoding="utf-8",
    )
    print()
    print("Production file rewritten : YES")
else:
    print()
    print("Production file rewritten : NO")
    print("Already in canonical TEI state.")


# ------------------------------------------------------------------
# 8. Post-repair lexical validation
# ------------------------------------------------------------------

print()
print("-" * 120)
print("6. POST-REPAIR LEXICAL VALIDATION")
print("-" * 120)

updated = TARGET.read_text(encoding="utf-8")

remaining_double = updated.count(
    "SourceFormat.TEI_XML_XML"
)

remaining_exact_stale = re.findall(
    r"SourceFormat\.TEI(?!_XML)",
    updated,
)

tei_xml_count = updated.count(
    "SourceFormat.TEI_XML"
)

print(
    "SourceFormat.TEI_XML_XML remaining : "
    f"{remaining_double}"
)

print(
    "Exact SourceFormat.TEI remaining    : "
    f"{len(remaining_exact_stale)}"
)

print(
    "SourceFormat.TEI_XML occurrences    : "
    f"{tei_xml_count}"
)

if remaining_double != 0:
    raise RuntimeError(
        "SourceFormat.TEI_XML_XML still remains."
    )

if remaining_exact_stale:
    raise RuntimeError(
        "Exact stale SourceFormat.TEI references remain."
    )


# ------------------------------------------------------------------
# 9. Python syntax validation
# ------------------------------------------------------------------

print()
print("-" * 120)
print("7. PYTHON SYNTAX VALIDATION")
print("-" * 120)

compile(
    updated,
    str(TARGET),
    "exec",
)

print("Production source compilation : PASS")


# ------------------------------------------------------------------
# 10. Runtime SourceFormat validation
# ------------------------------------------------------------------

print()
print("-" * 120)
print("8. RUNTIME SOURCEFORMAT VALIDATION")
print("-" * 120)

from SanskritAI.acquisition.models.source_format import SourceFormat

print("SourceFormat import : PASS")
print(
    f"SourceFormat.TEI_XML : "
    f"{SourceFormat.TEI_XML!r}"
)

print(
    f"Has SourceFormat.TEI : "
    f"{hasattr(SourceFormat, 'TEI')}"
)

if not hasattr(SourceFormat, "TEI_XML"):
    raise RuntimeError(
        "Canonical SourceFormat.TEI_XML is unavailable."
    )

if hasattr(SourceFormat, "TEI"):
    raise RuntimeError(
        "Unexpected SourceFormat.TEI exists."
    )


# ------------------------------------------------------------------
# 11. Runtime detector import
# ------------------------------------------------------------------

print()
print("-" * 120)
print("9. SOURCEFORMAT DETECTOR IMPORT")
print("-" * 120)

try:
    from SanskritAI.acquisition.detectors.source_format_detector import (
        SourceFormatDetector,
    )

    print("SourceFormatDetector import : PASS")
    print(
        f"Detector class : "
        f"{SourceFormatDetector}"
    )

except Exception as exc:
    print("SourceFormatDetector import : FAIL")
    print(f"ERROR: {exc!r}")
    print()
    print(
        "IMPORTANT: This is now a genuine downstream "
        "dependency error, not the TEI repair."
    )
    raise


# ------------------------------------------------------------------
# 12. TEI detection
# ------------------------------------------------------------------

print()
print("-" * 120)
print("10. TEI DETECTION")
print("-" * 120)

for filename in (
    "sample.tei",
    "sample.tei.xml",
):
    result = SourceFormatDetector.detect(filename)

    print(
        f"{filename:20s} -> {result!r}"
    )

    if result != SourceFormat.TEI_XML:
        raise RuntimeError(
            f"Unexpected TEI detection result "
            f"for {filename}: {result!r}"
        )


# ------------------------------------------------------------------
# 13. Final
# ------------------------------------------------------------------

print()
print("-" * 120)
print("11. FINAL DECISION")
print("-" * 120)

print("TEI canonical member          : TEI_XML")
print("Invalid TEI alias introduced  : NO")
print("TEI_XML_XML corruption fixed  : YES")
print("Exact stale TEI references    : NONE")
print("Production syntax             : PASS")
print("SourceFormat import           : PASS")
print("SourceFormatDetector import   : PASS")
print("TEI detection                 : PASS")
print()
print(
    "No SourceFormat or "
    "CorpusSourceFactory modification was made."
)
print(
    "Next step: complete acquisition runtime "
    "re-verification."
)


print()
print("=" * 120)
print(
    "BATCH 5H-5E-10R-4A STATUS: PASS"
)
print("=" * 120)
