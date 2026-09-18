from __future__ import annotations

import ast
import sys
from pathlib import Path


REPO_ROOT = Path("/content/SanskritAI")
REPO_PARENT = REPO_ROOT.parent

if str(REPO_PARENT) not in sys.path:
    sys.path.insert(0, str(REPO_PARENT))


DETECTOR_FILE = (
    REPO_ROOT
    / "acquisition"
    / "detectors"
    / "source_format_detector.py"
)

SOURCE_FORMAT_FILE = (
    REPO_ROOT
    / "acquisition"
    / "models"
    / "source_format.py"
)

FACTORY_FILE = (
    REPO_ROOT
    / "acquisition"
    / "factories"
    / "corpus_source_factory.py"
)


def section(title: str) -> None:
    print()
    print("-" * 120)
    print(title)
    print("-" * 120)


def production_python_files() -> list[Path]:
    files: list[Path] = []

    for path in (REPO_ROOT / "acquisition").rglob("*.py"):
        stem = path.stem

        # Project audit rule:
        # ignore historical / duplicate numeric files and _G<number>.py
        if any(stem.endswith(str(i)) for i in range(1, 10)):
            continue

        if "_G" in stem:
            suffix = stem.rsplit("_G", 1)[-1]
            if suffix.isdigit():
                continue

        files.append(path)

    return files


print("=" * 120)
print(
    "BATCH 5H-5E-10R-3 — "
    "SOURCEFORMAT DETECTOR → SOURCEFORMAT COMPATIBILITY AUDIT"
)
print("=" * 120)


# ------------------------------------------------------------------
# 1. Files
# ------------------------------------------------------------------

section("1. PRODUCTION FILES")

for path in (
    SOURCE_FORMAT_FILE,
    DETECTOR_FILE,
    FACTORY_FILE,
):
    print(f"{path.relative_to(REPO_ROOT)} : {path.exists()}")


# ------------------------------------------------------------------
# 2. Runtime SourceFormat
# ------------------------------------------------------------------

section("2. SOURCEFORMAT RUNTIME CONTRACT")

try:
    from SanskritAI.acquisition.models.source_format import SourceFormat

    print("SourceFormat import : PASS")

    for name, member in SourceFormat.__members__.items():
        print(f"  {name:20s} = {member.value!r}")

    print()
    print(f"SourceFormat.TEI exists     : {hasattr(SourceFormat, 'TEI')}")
    print(f"SourceFormat.TEI_XML exists : {hasattr(SourceFormat, 'TEI_XML')}")

except Exception as exc:
    SourceFormat = None
    print("SourceFormat import : FAIL")
    print(f"ERROR: {exc!r}")


# ------------------------------------------------------------------
# 3. Static detector inspection
# ------------------------------------------------------------------

section("3. SOURCEFORMAT DETECTOR STATIC CONTRACT")

if DETECTOR_FILE.exists():
    detector_source = DETECTOR_FILE.read_text(encoding="utf-8")

    print("Lines containing TEI:")
    for line_no, line in enumerate(
        detector_source.splitlines(),
        start=1,
    ):
        if "TEI" in line.upper():
            print(f"  {line_no:4d}: {line}")


# ------------------------------------------------------------------
# 4. AST inspection of detector
# ------------------------------------------------------------------

section("4. DETECTOR AST MAPPING")

tei_mappings: list[tuple[int, str, str]] = []

if DETECTOR_FILE.exists():
    source = DETECTOR_FILE.read_text(encoding="utf-8")

    try:
        tree = ast.parse(
            source,
            filename=str(DETECTOR_FILE),
        )

        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue

            for key, value in zip(node.keys, node.values):
                if not (
                    isinstance(key, ast.Constant)
                    and isinstance(key.value, str)
                ):
                    continue

                key_text = key.value.lower()

                if "tei" not in key_text:
                    continue

                value_text = ast.get_source_segment(
                    source,
                    value,
                ) or ""

                tei_mappings.append(
                    (
                        node.lineno,
                        key.value,
                        value_text,
                    )
                )

        if tei_mappings:
            for line_no, key, value in tei_mappings:
                print(
                    f"line {line_no:4d}: "
                    f"{key!r} -> {value}"
                )
        else:
            print("No TEI dictionary mappings found.")

    except Exception as exc:
        print(f"AST inspection failed: {exc!r}")


# ------------------------------------------------------------------
# 5. Detector runtime import
# ------------------------------------------------------------------

section("5. SOURCEFORMAT DETECTOR RUNTIME IMPORT")

try:
    from SanskritAI.acquisition.detectors.source_format_detector import (
        SourceFormatDetector,
    )

    print("SourceFormatDetector import : PASS")
    print(f"CLASS: {SourceFormatDetector}")

except Exception as exc:
    SourceFormatDetector = None
    print("SourceFormatDetector import : FAIL")
    print(f"ERROR: {exc!r}")


# ------------------------------------------------------------------
# 6. Detector runtime probe
# ------------------------------------------------------------------

section("6. DETECTOR RUNTIME PROBE")

if SourceFormatDetector is not None:

    detector = None

    try:
        detector = SourceFormatDetector()
        print("SourceFormatDetector() : PASS")
    except Exception as exc:
        print("SourceFormatDetector() : FAIL")
        print(f"ERROR: {exc!r}")

    if detector is not None:

        candidates = [
            "sample.tei",
            "sample.tei.xml",
            "sample.xml",
            "sample.txt",
            "sample.pdf",
            "sample.html",
            "sample.unknown",
        ]

        print()
        print("Detection candidates:")

        for candidate in candidates:
            try:
                result = detector.detect(candidate)

                print(
                    f"  {candidate:24s} -> "
                    f"{result!r}"
                )

            except Exception as exc:
                print(
                    f"  {candidate:24s} -> "
                    f"ERROR: {exc!r}"
                )


# ------------------------------------------------------------------
# 7. Production SourceFormat.TEI references
# ------------------------------------------------------------------

section("7. PRODUCTION SourceFormat.TEI REFERENCES")

tei_references: list[tuple[str, int, str]] = []

for path in production_python_files():

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        continue

    for line_no, line in enumerate(lines, start=1):

        if "SourceFormat.TEI" in line:
            tei_references.append(
                (
                    str(path.relative_to(REPO_ROOT)),
                    line_no,
                    line.strip(),
                )
            )

if tei_references:
    for path, line_no, line in tei_references:
        print(
            f"{path}:{line_no}: {line}"
        )
else:
    print("No production SourceFormat.TEI references found.")


# ------------------------------------------------------------------
# 8. Production TEI_XML references
# ------------------------------------------------------------------

section("8. PRODUCTION SourceFormat.TEI_XML REFERENCES")

tei_xml_references: list[tuple[str, int, str]] = []

for path in production_python_files():

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        continue

    for line_no, line in enumerate(lines, start=1):

        if "SourceFormat.TEI_XML" in line:
            tei_xml_references.append(
                (
                    str(path.relative_to(REPO_ROOT)),
                    line_no,
                    line.strip(),
                )
            )

if tei_xml_references:
    for path, line_no, line in tei_xml_references:
        print(
            f"{path}:{line_no}: {line}"
        )
else:
    print("No production SourceFormat.TEI_XML references found.")


# ------------------------------------------------------------------
# 9. Detector callers
# ------------------------------------------------------------------

section("9. SOURCEFORMAT DETECTOR CALLERS")

detector_callers: list[tuple[str, int, str]] = []

for path in production_python_files():

    try:
        source = path.read_text(encoding="utf-8")
    except Exception:
        continue

    if path == DETECTOR_FILE:
        continue

    for line_no, line in enumerate(source.splitlines(), start=1):

        if (
            "SourceFormatDetector" in line
            or "source_format_detector" in line
        ):
            detector_callers.append(
                (
                    str(path.relative_to(REPO_ROOT)),
                    line_no,
                    line.strip(),
                )
            )

if detector_callers:
    for path, line_no, line in detector_callers:
        print(
            f"{path}:{line_no}: {line}"
        )
else:
    print("No production detector callers found.")


# ------------------------------------------------------------------
# 10. CorpusSourceFactory import after detector inspection
# ------------------------------------------------------------------

section("10. CORPUS SOURCE FACTORY IMPORT")

try:
    from SanskritAI.acquisition.factories.corpus_source_factory import (
        CorpusSourceFactory,
    )

    print("CorpusSourceFactory import : PASS")
    print(f"CLASS: {CorpusSourceFactory}")

except Exception as exc:
    CorpusSourceFactory = None

    print("CorpusSourceFactory import : FAIL")
    print(f"ERROR: {exc!r}")


# ------------------------------------------------------------------
# 11. Final decision
# ------------------------------------------------------------------

section("11. FINAL DECISION")

has_invalid_detector_mapping = any(
    "SourceFormat.TEI" in value
    for _, _, value in tei_mappings
)

if (
    SourceFormat is not None
    and hasattr(SourceFormat, "TEI_XML")
    and not hasattr(SourceFormat, "TEI")
    and has_invalid_detector_mapping
):

    print("Canonical TEI enum member     : TEI_XML")
    print("Invalid detector member       : TEI")
    print("Detector incompatibility      : CONFIRMED")
    print()
    print("Interpretation:")
    print("  .tei      → TEI_XML is the likely canonical mapping")
    print("  .tei.xml  → TEI_XML is the likely canonical mapping")
    print()
    print("Production repair candidate   : source_format_detector.py")
    print("Repair scope                  : minimal detector mapping only")
    print("Do NOT add SourceFormat.TEI.")
    print("Do NOT modify CorpusSourceFactory yet.")

elif (
    SourceFormat is not None
    and hasattr(SourceFormat, "TEI_XML")
    and SourceFormatDetector is not None
    and CorpusSourceFactory is not None
):

    print("Detector compatibility        : VERIFIED")
    print("CorpusSourceFactory import    : VERIFIED")
    print("No production repair required.")

else:

    print("Detector compatibility        : NOT FULLY VERIFIED")
    print("Production repair             : DO NOT MODIFY")
    print("Further dependency audit      : REQUIRED")


print()
print("=" * 120)
print("BATCH 5H-5E-10R-3 STATUS: AUDIT COMPLETE")
print("=" * 120)
