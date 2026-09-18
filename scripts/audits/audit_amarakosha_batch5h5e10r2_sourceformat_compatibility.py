from __future__ import annotations

import ast
import sys
from pathlib import Path


REPO_ROOT = Path("/content/SanskritAI")
REPO_PARENT = REPO_ROOT.parent

if str(REPO_PARENT) not in sys.path:
    sys.path.insert(0, str(REPO_PARENT))


SOURCE_FORMAT_FILE = (
    REPO_ROOT
    / "acquisition"
    / "models"
    / "source_format.py"
)

CORPUS_SOURCE_FACTORY_FILE = (
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


def ast_attribute_references(path: Path, attribute: str) -> list[tuple[int, str]]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    matches: list[tuple[int, str]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            if node.attr == attribute:
                try:
                    text = ast.get_source_segment(source, node) or ""
                except Exception:
                    text = ""
                matches.append((node.lineno, text))

    return matches


print("=" * 120)
print("BATCH 5H-5E-10R-2 — SOURCEFORMAT / CORPUS SOURCE FACTORY COMPATIBILITY AUDIT")
print("=" * 120)


# ------------------------------------------------------------------
# 1. File existence
# ------------------------------------------------------------------

section("1. PRODUCTION FILES")

for path in (
    SOURCE_FORMAT_FILE,
    CORPUS_SOURCE_FACTORY_FILE,
):
    print(f"{path.relative_to(REPO_ROOT)} : {path.exists()}")


# ------------------------------------------------------------------
# 2. SourceFormat runtime contract
# ------------------------------------------------------------------

section("2. SOURCEFORMAT RUNTIME CONTRACT")

try:
    from SanskritAI.acquisition.models.source_format import SourceFormat

    print("SourceFormat import : PASS")
    print()
    print("Enum members:")

    for name, member in SourceFormat.__members__.items():
        print(f"  {name:20s} = {member.value!r}")

    print()
    print(f"Has TEI     : {hasattr(SourceFormat, 'TEI')}")
    print(f"Has TEI_XML : {hasattr(SourceFormat, 'TEI_XML')}")

except Exception as exc:
    SourceFormat = None
    print("SourceFormat import : FAIL")
    print(f"ERROR: {exc!r}")


# ------------------------------------------------------------------
# 3. Static inspection of SourceFormat
# ------------------------------------------------------------------

section("3. SOURCEFORMAT STATIC INSPECTION")

if SOURCE_FORMAT_FILE.exists():
    source = SOURCE_FORMAT_FILE.read_text(encoding="utf-8")

    print("Literal 'TEI' occurrences:")
    for line_no, line in enumerate(source.splitlines(), start=1):
        if "TEI" in line:
            print(f"  {line_no:4d}: {line}")

    try:
        tree = ast.parse(
            source,
            filename=str(SOURCE_FORMAT_FILE),
        )

        enum_assignments: list[tuple[int, str, str]] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if target.id in {"TEI", "TEI_XML"}:
                            value = ast.get_source_segment(source, node.value) or ""
                            enum_assignments.append(
                                (
                                    node.lineno,
                                    target.id,
                                    value,
                                )
                            )

        print()
        print("TEI-related enum assignments:")

        if enum_assignments:
            for line_no, name, value in enum_assignments:
                print(
                    f"  line {line_no}: "
                    f"{name} = {value}"
                )
        else:
            print("  NONE")

    except Exception as exc:
        print(f"AST inspection failed: {exc!r}")


# ------------------------------------------------------------------
# 4. Static inspection of CorpusSourceFactory
# ------------------------------------------------------------------

section("4. CORPUS SOURCE FACTORY STATIC INSPECTION")

if CORPUS_SOURCE_FACTORY_FILE.exists():
    source = CORPUS_SOURCE_FACTORY_FILE.read_text(encoding="utf-8")

    print("SourceFormat references:")

    try:
        references = ast_attribute_references(
            CORPUS_SOURCE_FACTORY_FILE,
            "TEI",
        )

        if references:
            for line_no, text in references:
                print(
                    f"  line {line_no:4d}: "
                    f"{text}"
                )
        else:
            print("  No .TEI references found.")

    except Exception as exc:
        print(f"AST inspection failed: {exc!r}")

    print()
    print("Literal lines containing 'SourceFormat.TEI':")

    found_literal = False

    for line_no, line in enumerate(source.splitlines(), start=1):
        if "SourceFormat.TEI" in line:
            found_literal = True
            print(f"  {line_no:4d}: {line}")

    if not found_literal:
        print("  NONE")


# ------------------------------------------------------------------
# 5. Other production references
# ------------------------------------------------------------------

section("5. PRODUCTION SourceFormat.TEI REFERENCES")

production_root = REPO_ROOT / "acquisition"

matches: list[tuple[str, int, str]] = []

for path in production_root.rglob("*.py"):
    # Ignore historical / duplicate files by project audit rule.
    if path.name.endswith(".py"):
        stem = path.stem

        if any(
            stem.endswith(str(i))
            for i in range(1, 10)
        ):
            continue

        if "_G" in stem:
            suffix = stem.rsplit("_G", 1)[-1]
            if suffix.isdigit():
                continue

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        continue

    for line_no, line in enumerate(lines, start=1):
        if "SourceFormat.TEI" in line:
            matches.append(
                (
                    str(path.relative_to(REPO_ROOT)),
                    line_no,
                    line.strip(),
                )
            )

if matches:
    for path, line_no, line in matches:
        print(
            f"{path}:{line_no}: {line}"
        )
else:
    print("No production SourceFormat.TEI references found.")


# ------------------------------------------------------------------
# 6. Production SourceFormat.TEI_XML references
# ------------------------------------------------------------------

section("6. PRODUCTION SourceFormat.TEI_XML REFERENCES")

matches_xml: list[tuple[str, int, str]] = []

for path in production_root.rglob("*.py"):
    stem = path.stem

    if any(stem.endswith(str(i)) for i in range(1, 10)):
        continue

    if "_G" in stem:
        suffix = stem.rsplit("_G", 1)[-1]
        if suffix.isdigit():
            continue

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        continue

    for line_no, line in enumerate(lines, start=1):
        if "SourceFormat.TEI_XML" in line:
            matches_xml.append(
                (
                    str(path.relative_to(REPO_ROOT)),
                    line_no,
                    line.strip(),
                )
            )

if matches_xml:
    for path, line_no, line in matches_xml:
        print(
            f"{path}:{line_no}: {line}"
        )
else:
    print("No production SourceFormat.TEI_XML references found.")


# ------------------------------------------------------------------
# 7. Final diagnosis
# ------------------------------------------------------------------

section("7. FINAL DIAGNOSIS")

if SourceFormat is None:
    print("SourceFormat contract : NOT VERIFIED")
    print("CorpusSourceFactory   : NOT VERIFIED")
    print("Decision              : DO NOT MODIFY PRODUCTION")
else:
    has_tei = hasattr(SourceFormat, "TEI")
    has_tei_xml = hasattr(SourceFormat, "TEI_XML")

    if not has_tei and has_tei_xml and matches:
        print("Canonical enum member : TEI_XML")
        print("Legacy/invalid member : TEI")
        print("Factory incompatibility: CONFIRMED")
        print("Decision               : PRODUCTION REPAIR MAY BE REQUIRED")
        print("Next                   : inspect exact offending factory lines")
    elif has_tei:
        print("SourceFormat.TEI exists.")
        print("The observed AttributeError requires further investigation.")
        print("Decision: DO NOT MODIFY PRODUCTION")
    elif not matches:
        print("No SourceFormat.TEI reference found by static audit.")
        print("Observed import failure requires deeper dependency tracing.")
        print("Decision: DO NOT MODIFY PRODUCTION")
    else:
        print("SourceFormat / factory relationship remains ambiguous.")
        print("Decision: DO NOT MODIFY PRODUCTION")


print()
print("=" * 120)
print("BATCH 5H-5E-10R-2 STATUS: AUDIT COMPLETE")
print("=" * 120)
