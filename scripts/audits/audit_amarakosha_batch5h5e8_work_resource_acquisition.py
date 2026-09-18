from __future__ import annotations

from pathlib import Path
import ast
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


TARGET_FILES = (
    REPO_ROOT
    / "acquisition"
    / "metadata"
    / "models"
    / "work_definition.py",

    REPO_ROOT
    / "acquisition"
    / "metadata"
    / "extractors"
    / "corpus_type_extractor.py",

    REPO_ROOT
    / "acquisition"
    / "models"
    / "corpus_source.py",

    REPO_ROOT
    / "acquisition"
    / "models"
    / "acquisition_manifest.py",

    REPO_ROOT
    / "acquisition"
    / "factories"
    / "corpus_source_factory.py",

    REPO_ROOT
    / "acquisition"
    / "acquisition_manager.py",

    REPO_ROOT
    / "acquisition"
    / "acquirers"
    / "default_source_acquirer.py",
)


AMARAKOSHA_TERMS = (
    "amarakosha",
    "amarakośa",
    "amara kosha",
    "amara-kośa",
    "अमरकोश",
    "अमरकोष",
)


CONSTRUCTION_TERMS = (
    "CorpusSource",
    "AcquisitionManifest",
    "WorkDefinition",
    "from_metadata",
    "from_url",
    "from_file",
    "source_url",
    "source_urls",
    "download_url",
    "urls",
    "manifest",
    "provider",
    "resource",
    "artifact",
    "work_identifier",
)


def is_excluded(path: Path) -> bool:
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return True

    if path.suffix == ".py":
        for pattern in EXCLUDED_PYTHON_PATTERNS:
            if pattern.match(path.name):
                return True

    return False


def read_text(path: Path, limit: int = 300_000) -> str:
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


def definitions(path: Path) -> list[str]:
    tree = parse_python(path)

    if tree is None:
        return []

    result = []

    for node in ast.walk(tree):
        if isinstance(
            node,
            (
                ast.ClassDef,
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            result.append(node.name)

    return result


def constructor_calls(path: Path) -> list[str]:
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

    results = []

    for number, line in enumerate(
        text.splitlines(),
        start=1,
    ):
        lower = line.lower()

        if any(
            term.lower() in lower
            for term in CONSTRUCTION_TERMS
        ):
            results.append(
                f"{number:>5}: {line.rstrip()}"
            )

    return results


def amarakosha_lines(path: Path) -> list[str]:
    text = read_text(path)

    if not text:
        return []

    results = []

    for number, line in enumerate(
        text.splitlines(),
        start=1,
    ):
        lower = line.lower()

        if any(
            term.lower() in lower
            for term in AMARAKOSHA_TERMS
        ):
            results.append(
                f"{number:>5}: {line.rstrip()}"
            )

    return results


print("=" * 120)
print(
    "BATCH 5H-5E-8 — AMARAKOSHA WORK / RESOURCE → ACQUISITION TRACE"
)
print("=" * 120)


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
    print(f"DEFINITIONS: {definitions(path)}")


print("\n" + "-" * 120)
print("2. WORK DEFINITION CONTRACT")
print("-" * 120)

work_definition = (
    REPO_ROOT
    / "acquisition"
    / "metadata"
    / "models"
    / "work_definition.py"
)

if work_definition.exists():
    print(f"FILE: {rel(work_definition)}")

    lines = relevant_lines(work_definition)

    if lines:
        for line in lines:
            print(line)
    else:
        print(
            "No WorkDefinition/acquisition construction "
            "terms found."
        )


print("\n" + "-" * 120)
print("3. CORPUS TYPE / RESOURCE METADATA CONTRACT")
print("-" * 120)

extractor = (
    REPO_ROOT
    / "acquisition"
    / "metadata"
    / "extractors"
    / "corpus_type_extractor.py"
)

if extractor.exists():
    print(f"FILE: {rel(extractor)}")

    lines = relevant_lines(extractor)

    if lines:
        for line in lines:
            print(line)
    else:
        print(
            "No relevant metadata/extractor terms found."
        )


print("\n" + "-" * 120)
print("4. CORPUS SOURCE CONSTRUCTION PATH")
print("-" * 120)

factory = (
    REPO_ROOT
    / "acquisition"
    / "factories"
    / "corpus_source_factory.py"
)

if factory.exists():
    print(f"FILE: {rel(factory)}")

    calls = constructor_calls(factory)

    target_calls = [
        name
        for name in calls
        if name in {
            "CorpusSource",
            "SourceFormatDetector",
            "Path",
        }
    ]

    print(
        "CONSTRUCTION CALLS:",
        sorted(set(target_calls)),
    )

    lines = relevant_lines(factory)

    for line in lines:
        print(line)


print("\n" + "-" * 120)
print("5. ACQUISITION MANIFEST CONSTRUCTION PATH")
print("-" * 120)

manifest = (
    REPO_ROOT
    / "acquisition"
    / "models"
    / "acquisition_manifest.py"
)

if manifest.exists():
    print(f"FILE: {rel(manifest)}")

    calls = constructor_calls(manifest)

    target_calls = [
        name
        for name in calls
        if name in {
            "CorpusSource",
            "AcquisitionManifest",
            "Path",
        }
    ]

    print(
        "CONSTRUCTION CALLS:",
        sorted(set(target_calls)),
    )

    lines = relevant_lines(manifest)

    for line in lines:
        print(line)


print("\n" + "-" * 120)
print("6. ALL PRODUCTION CorpusSource CONSTRUCTION SITES")
print("-" * 120)

corpus_source_sites = []

for path in REPO_ROOT.rglob("*.py"):
    if is_excluded(path):
        continue

    text = read_text(path)

    if not text:
        continue

    tree = parse_python(path)

    if tree is None:
        continue

    found = False

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        function = node.func

        if isinstance(function, ast.Name):
            if function.id == "CorpusSource":
                found = True

        elif isinstance(function, ast.Attribute):
            if function.attr == "CorpusSource":
                found = True

    if found:
        corpus_source_sites.append(
            rel(path)
        )

if corpus_source_sites:
    for path_name in sorted(
        set(corpus_source_sites)
    ):
        print(path_name)
else:
    print(
        "No production CorpusSource constructor sites found."
    )


print("\n" + "-" * 120)
print("7. ALL PRODUCTION AcquisitionManifest CONSTRUCTION SITES")
print("-" * 120)

manifest_sites = []

for path in REPO_ROOT.rglob("*.py"):
    if is_excluded(path):
        continue

    text = read_text(path)

    if not text:
        continue

    tree = parse_python(path)

    if tree is None:
        continue

    found = False

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        function = node.func

        if isinstance(function, ast.Name):
            if function.id == "AcquisitionManifest":
                found = True

        elif isinstance(function, ast.Attribute):
            if function.attr == "AcquisitionManifest":
                found = True

    if found:
        manifest_sites.append(
            rel(path)
        )

if manifest_sites:
    for path_name in sorted(
        set(manifest_sites)
    ):
        print(path_name)
else:
    print(
        "No production AcquisitionManifest constructor sites found."
    )


print("\n" + "-" * 120)
print("8. AMARAKOSHA REFERENCES IN WORK / RESOURCE CODE")
print("-" * 120)

work_resource_files = (
    REPO_ROOT / "acquisition" / "metadata",
    REPO_ROOT / "acquisition" / "resources",
    REPO_ROOT / "core" / "resources",
    REPO_ROOT / "resources",
)

found = []

for root in work_resource_files:
    if not root.exists():
        continue

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if is_excluded(path):
            continue

        text = read_text(path)

        if not text:
            continue

        if any(
            term.lower() in text.lower()
            for term in AMARAKOSHA_TERMS
        ):
            found.append(rel(path))

if found:
    for path_name in sorted(set(found)):
        print()
        print(f"FILE: {path_name}")

        lines = amarakosha_lines(
            REPO_ROOT / path_name
        )

        for line in lines:
            print(line)

else:
    print(
        "No Amarakośa references found in "
        "work/resource metadata paths."
    )


print("\n" + "-" * 120)
print("9. AMARAKOSHA → CorpusSource / Manifest TRACE")
print("-" * 120)

trace_files = []

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

    has_acquisition = (
        "corpus_source" in lower
        or "acquisition_manifest" in lower
        or "source_url" in lower
        or "download_url" in lower
        or "acquisitionmanager" in lower
    )

    if has_amarakosha and has_acquisition:
        trace_files.append(rel(path))

if trace_files:
    for path_name in sorted(
        set(trace_files)
    ):
        print(path_name)
else:
    print(
        "No production Amarakośa → acquisition "
        "construction trace found."
    )


print("\n" + "-" * 120)
print("10. ARCHITECTURAL GATE")
print("-" * 120)

print(
    "Existing WorkDefinition                  : PRESERVE"
)
print(
    "Existing resource metadata               : PRESERVE"
)
print(
    "Existing CorpusSource                    : PRESERVE"
)
print(
    "Existing CorpusSourceFactory             : PRESERVE"
)
print(
    "Existing AcquisitionManifest             : PRESERVE"
)
print(
    "Existing AcquisitionManager              : PRESERVE"
)
print(
    "Existing SourceAcquirer                  : PRESERVE"
)
print(
    "Existing AmarakoshaParser                : PRESERVE"
)
print(
    "New Amarakośa source model               : NOT JUSTIFIED"
)
print(
    "New Amarakośa provider                   : NOT JUSTIFIED"
)
print(
    "Parser implementation                   : DEFER"
)


print("\n" + "-" * 120)
print("11. DECISION")
print("-" * 120)

if trace_files:
    print(
        "AMARAKOSHA → ACQUISITION TRACE : FOUND"
    )
else:
    print(
        "AMARAKOSHA → ACQUISITION TRACE : NOT FOUND"
    )

if corpus_source_sites:
    print(
        "CorpusSource construction path : FOUND"
    )
else:
    print(
        "CorpusSource construction path : NOT FOUND"
    )

if manifest_sites:
    print(
        "AcquisitionManifest construction path : FOUND"
    )
else:
    print(
        "AcquisitionManifest construction path : NOT FOUND"
    )

print(
    "\nBATCH 5H-5E-8 STATUS: AUDIT COMPLETE"
)

print("=" * 120)
