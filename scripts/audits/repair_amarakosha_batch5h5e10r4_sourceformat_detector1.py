from __future__ import annotations

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

BACKUP = TARGET.with_suffix(".py.5h5e10r4.bak")


print("=" * 120)
print(
    "BATCH 5H-5E-10R-4 — "
    "MINIMAL SOURCEFORMAT DETECTOR REPAIR"
)
print("=" * 120)

print()
print("-" * 120)
print("1. TARGET")
print("-" * 120)

print(f"Target : {TARGET}")
print(f"Exists : {TARGET.exists()}")

if not TARGET.exists():
    raise FileNotFoundError(TARGET)


print()
print("-" * 120)
print("2. BACKUP")
print("-" * 120)

shutil.copy2(TARGET, BACKUP)

print(f"Backup : {BACKUP}")
print(f"Exists : {BACKUP.exists()}")


print()
print("-" * 120)
print("3. CURRENT TEI REFERENCES")
print("-" * 120)

source = TARGET.read_text(encoding="utf-8")

for line_no, line in enumerate(source.splitlines(), start=1):
    if "SourceFormat.TEI" in line:
        print(f"{line_no:4d}: {line}")


print()
print("-" * 120)
print("4. MINIMAL REPAIR")
print("-" * 120)

old_tei = "SourceFormat.TEI"
new_tei = "SourceFormat.TEI_XML"

occurrences = source.count(old_tei)

print(f"Occurrences before repair : {occurrences}")
print(f"Replacing                  : {old_tei}")
print(f"With                       : {new_tei}")

if occurrences != 2:
    raise RuntimeError(
        "Expected exactly 2 stale SourceFormat.TEI references. "
        f"Found {occurrences}."
    )

repaired = source.replace(old_tei, new_tei)

TARGET.write_text(repaired, encoding="utf-8")

print("Production file rewritten : YES")


print()
print("-" * 120)
print("5. POST-REPAIR VALIDATION")
print("-" * 120)

updated = TARGET.read_text(encoding="utf-8")

remaining = updated.count("SourceFormat.TEI")
canonical = updated.count("SourceFormat.TEI_XML")

print(
    f"Remaining SourceFormat.TEI occurrences     : {remaining}"
)
print(
    f"SourceFormat.TEI_XML occurrences            : {canonical}"
)

if remaining != 0:
    raise RuntimeError(
        "Stale SourceFormat.TEI references remain."
    )

if canonical != 2:
    raise RuntimeError(
        "Expected exactly 2 SourceFormat.TEI_XML references."
    )


print()
print("-" * 120)
print("6. FILE INTEGRITY")
print("-" * 120)

compile_source = compile(
    updated,
    str(TARGET),
    "exec",
)

print(f"Python compilation object : {compile_source!r}")
print("Syntax validation         : PASS")


print()
print("-" * 120)
print("7. REPAIR SUMMARY")
print("-" * 120)

print("Changed file:")
print(
    "  acquisition/detectors/source_format_detector.py"
)

print()
print("Changed semantics:")
print("  .tei     -> SourceFormat.TEI_XML")
print("  .tei.xml -> SourceFormat.TEI_XML")

print()
print("Not changed:")
print("  SourceFormat")
print("  CorpusSourceFactory")
print("  CorpusSource")
print("  WorkRegistry")
print("  WorkDefinition")
print("  Amarakośa")
print("  acquisition architecture")


print()
print("=" * 120)
print("BATCH 5H-5E-10R-4 STATUS: REPAIR COMPLETE")
print("=" * 120)
