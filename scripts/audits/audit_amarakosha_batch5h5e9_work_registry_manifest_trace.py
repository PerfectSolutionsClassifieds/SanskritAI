from __future__ import annotations

from pathlib import Path
import ast
import json
import re

REPO_ROOT = Path("/content/SanskritAI")

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "_audit",
    "tests",
}

EXCLUDED_PYTHON_PATTERNS = (
    re.compile(r".*\d+\.py$"),
    re.compile(r".*_G\d+\.py$"),
)

AMARAKOSHA_TERMS = (
    "amarakosha",
    "amarakośa",
    "अमरकोश",
    "अमरकोष",
)

TARGET_FILES = (
    REPO_ROOT / "resources" / "work_registry.json",
    REPO_ROOT / "core" / "resources" / "resource_id.py",
    REPO_ROOT / "acquisition" / "metadata" / "models" / "work_definition.py",
    REPO_ROOT / "acquisition" / "factories" / "corpus_source_factory.py",
    REPO_ROOT / "acquisition" / "models" / "corpus_source.py",
    REPO_ROOT / "acquisition" / "models" / "acquisition_manifest.py",
    REPO_ROOT / "acquisition" / "sources" / "monier_williams_manifest.py",
)

CONSTRUCTION_NAMES = {
    "WorkDefinition",
    "ResourceId",
    "CorpusSource",
    "AcquisitionManifest",
}

def is_excluded(path: Path) -> bool:
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return True

    if path.suffix == ".py":
        for pattern in EXCLUDED_PYTHON_PATTERNS:
            if pattern.match(path.name):
                return True

    return False


def read_text(path: Path, limit: int = 400_000) -> str:
    try:
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )[:limit]
    except Exception:
        return ""


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def parse_python(path: Path):
    text = read_text(path)

    if not text:
        return None

    try:
        return ast.parse(text)
    except SyntaxError:
        return None


def call_names(path: Path) -> list[str]:
    tree = parse_python(path)

    if tree is None:
        return []

    result = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        function = node.func

        if isinstance(function, ast.Name):
            result.append(function.id)

        elif isinstance(function, ast.Attribute):
            result.append(function.attr)

    return result


def relevant_lines(path: Path) -> list[str]:
    text = read_text(path)

    if not text:
        return []

    terms = (
        "WorkDefinition",
        "ResourceId",
        "CorpusSource",
        "AcquisitionManifest",
        "from_dict",
        "from_metadata",
        "from_url",
        "from_file",
        "manifest",
        "resource",
        "work_identifier",
        "source_identifier",
        "download_url",
        "amarakosha",
        "amarakośa",
    )

    result = []

    for number, line in enumerate(
        text.splitlines(),
        start=1,
    ):
        lower = line.lower()

        if any(term.lower() in lower for term in terms):
            result.append(
                f"{number:>5}: {line.rstrip()}"
            )

    return result


print("=" * 120)
print(
    "BATCH 5H-5E-9 — "
    "AMARAKOSHA WORK REGISTRY → ACQUISITION MANIFEST TRACE"
)
print("=" * 120)


# ------------------------------------------------------------------
# 1. TARGET INVENTORY
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("1. TARGET FILE INVENTORY")
print("-" * 120)

for path in TARGET_FILES:
    print()
    print(f"FILE: {rel(path)}")

    if not path.exists():
        print("STATUS: MISSING")
        continue

    print("STATUS: EXISTS")

    if path.suffix == ".py":
        print(
            "CALLS:",
            sorted(set(call_names(path)) & CONSTRUCTION_NAMES),
        )


# ------------------------------------------------------------------
# 2. WORK REGISTRY
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("2. AMARAKOSHA WORK REGISTRY ENTRY")
print("-" * 120)

registry_path = (
    REPO_ROOT
    / "resources"
    / "work_registry.json"
)

if registry_path.exists():
    try:
        data = json.loads(
            read_text(registry_path)
        )

        works = data.get("works", [])

        matches = [
            work
            for work in works
            if str(work.get("identifier", "")).lower()
            == "amarakosha"
        ]

        if matches:
            work = matches[0]

            print("IDENTIFIER :", work.get("identifier"))
            print("TITLE      :", work.get("title"))
            print("CORPUS TYPE:", work.get("corpus_type"))
            print("LANGUAGE   :", work.get("language"))
            print("SCRIPT     :", work.get("script"))
            print("REPOSITORY :", work.get("repository"))
            print("ALIASES    :", work.get("aliases"))
            print("METADATA   :", work.get("metadata"))

        else:
            print("Amarakośa registry entry: NOT FOUND")

    except Exception as exc:
        print("REGISTRY ERROR:", repr(exc))


# ------------------------------------------------------------------
# 3. WorkDefinition.from_dict
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("3. WorkDefinition CONSTRUCTION")
print("-" * 120)

work_definition_path = (
    REPO_ROOT
    / "acquisition"
    / "metadata"
    / "models"
    / "work_definition.py"
)

if work_definition_path.exists():

    calls = call_names(work_definition_path)

    print(
        "CONSTRUCTOR / FACTORY CALLS:",
        sorted(set(calls) & CONSTRUCTION_NAMES),
    )

    lines = relevant_lines(work_definition_path)

    for line in lines:
        print(line)


# ------------------------------------------------------------------
# 4. ResourceId
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("4. ResourceId AMARAKOSHA CONTRACT")
print("-" * 120)

resource_id_path = (
    REPO_ROOT
    / "core"
    / "resources"
    / "resource_id.py"
)

if resource_id_path.exists():

    lines = relevant_lines(resource_id_path)

    for line in lines:
        print(line)


# ------------------------------------------------------------------
# 5. Search production code for WorkDefinition.from_dict
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("5. PRODUCTION WorkDefinition / from_dict USAGE")
print("-" * 120)

work_definition_sites = []

for path in REPO_ROOT.rglob("*.py"):

    if is_excluded(path):
        continue

    text = read_text(path)

    if not text:
        continue

    lower = text.lower()

    if (
        "workdefinition" in lower
        or "work_definition" in lower
    ) and "from_dict" in lower:

        work_definition_sites.append(
            rel(path)
        )

if work_definition_sites:
    for name in sorted(set(work_definition_sites)):
        print(name)
else:
    print(
        "No production WorkDefinition.from_dict "
        "usage found."
    )


# ------------------------------------------------------------------
# 6. Production CorpusSourceFactory usage
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("6. PRODUCTION CorpusSourceFactory USAGE")
print("-" * 120)

factory_sites = []

for path in REPO_ROOT.rglob("*.py"):

    if is_excluded(path):
        continue

    text = read_text(path)

    if not text:
        continue

    lower = text.lower()

    if (
        "corpussourcefactory" in lower
        or "corpus_source_factory" in lower
    ):
        factory_sites.append(
            rel(path)
        )

if factory_sites:
    for name in sorted(set(factory_sites)):
        print(name)
else:
    print(
        "No production CorpusSourceFactory "
        "usage found."
    )


# ------------------------------------------------------------------
# 7. Production AcquisitionManifest usage
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("7. PRODUCTION AcquisitionManifest USAGE")
print("-" * 120)

manifest_sites = []

for path in REPO_ROOT.rglob("*.py"):

    if is_excluded(path):
        continue

    text = read_text(path)

    if not text:
        continue

    lower = text.lower()

    if (
        "acquisitionmanifest" in lower
        or "acquisition_manifest" in lower
    ):
        manifest_sites.append(
            rel(path)
        )

if manifest_sites:
    for name in sorted(set(manifest_sites)):
        print(name)
else:
    print(
        "No production AcquisitionManifest "
        "usage found."
    )


# ------------------------------------------------------------------
# 8. Amarakośa + acquisition construction evidence
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("8. AMARAKOSHA + ACQUISITION CONSTRUCTION EVIDENCE")
print("-" * 120)

trace_sites = []

for path in REPO_ROOT.rglob("*.py"):

    if is_excluded(path):
        continue

    text = read_text(path)

    if not text:
        continue

    lower = text.lower()

    has_amarakosha = any(
        term.lower() in lower
        for term in AMARAKOSHA_TERMS
    )

    has_work = (
        "workdefinition" in lower
        or "work_definition" in lower
    )

    has_resource = (
        "resourceid" in lower
        or "resource_id" in lower
    )

    has_source = (
        "corpussource" in lower
        or "corpus_source" in lower
    )

    has_manifest = (
        "acquisitionmanifest" in lower
        or "acquisition_manifest" in lower
    )

    if (
        has_amarakosha
        and (
            has_work
            or has_resource
            or has_source
            or has_manifest
        )
    ):
        trace_sites.append(
            rel(path)
        )

if trace_sites:
    for name in sorted(set(trace_sites)):
        print(name)
else:
    print(
        "No production Amarakośa work/resource/"
        "acquisition construction trace found."
    )


# ------------------------------------------------------------------
# 9. Decision
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("9. ARCHITECTURAL DECISION")
print("-" * 120)

print(
    "WorkDefinition model             : PRESERVE"
)
print(
    "ResourceId model                 : PRESERVE"
)
print(
    "resources/work_registry.json     : PRESERVE"
)
print(
    "CorpusSourceFactory              : PRESERVE"
)
print(
    "AcquisitionManifest              : PRESERVE"
)
print(
    "MW manifest architecture         : REFERENCE ONLY"
)
print(
    "New Amarakośa source class       : NOT JUSTIFIED"
)
print(
    "New Amarakośa provider           : NOT JUSTIFIED"
)
print(
    "AmarakoshaParser grammar         : DEFER"
)


# ------------------------------------------------------------------
# 10. Final gate
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("10. FINAL GATE")
print("-" * 120)

if trace_sites:
    print(
        "AMARAKOSHA WORK → ACQUISITION EVIDENCE : FOUND"
    )
else:
    print(
        "AMARAKOSHA WORK → ACQUISITION EVIDENCE : NOT FOUND"
    )

print(
    "BATCH 5H-5E-9 STATUS: AUDIT COMPLETE"
)

print("=" * 120)
