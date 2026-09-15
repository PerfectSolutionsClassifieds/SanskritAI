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
    REPO_ROOT / "acquisition" / "models" / "corpus_source.py",
    REPO_ROOT / "acquisition" / "models" / "acquisition_manifest.py",
    REPO_ROOT / "acquisition" / "acquisition_manager.py",
    REPO_ROOT / "acquisition" / "acquirers" / "source_acquirer.py",
    REPO_ROOT / "acquisition" / "acquirers" / "default_source_acquirer.py",
    REPO_ROOT / "acquisition" / "factories" / "corpus_source_factory.py",
    REPO_ROOT / "acquisition" / "providers" / "acquisition_request.py",
    REPO_ROOT / "acquisition" / "providers" / "acquisition_response.py",
    REPO_ROOT / "acquisition" / "providers" / "provider_registry.py",
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


def imports(path: Path) -> list[str]:
    tree = parse_python(path)

    if tree is None:
        return []

    result = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                result.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""

            for alias in node.names:
                result.append(
                    f"{module}.{alias.name}"
                )

    return result


def call_names(path: Path) -> list[str]:
    tree = parse_python(path)

    if tree is None:
        return []

    result = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            function = node.func

            if isinstance(function, ast.Name):
                result.append(function.id)

            elif isinstance(function, ast.Attribute):
                result.append(function.attr)

    return result


def source_lines(path: Path) -> list[str]:
    text = read_text(path)

    if not text:
        return []

    terms = (
        "source",
        "url",
        "urls",
        "provider",
        "manifest",
        "resource",
        "artifact",
        "download",
        "acquire",
        "input",
        "path",
        "identifier",
        "name",
        "version",
    )

    results = []

    for line_no, line in enumerate(
        text.splitlines(),
        start=1,
    ):
        lower = line.lower()

        if any(term in lower for term in terms):
            results.append(
                f"{line_no:>5}: {line.rstrip()}"
            )

    return results


def executable_urls(path: Path) -> list[str]:
    text = read_text(path)

    if not text:
        return []

    # Only inspect actual string literals.
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []

    urls = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant):
            value = node.value

            if not isinstance(value, str):
                continue

            for match in re.findall(
                r"https?://[^\s\"'<>]+|ftp://[^\s\"'<>]+",
                value,
            ):
                urls.append(match)

    return sorted(set(urls))


print("=" * 120)
print(
    "BATCH 5H-5E-7 — AMARAKOSHA ACQUISITION CONTRACT + TRACE AUDIT"
)
print("=" * 120)


print("\n" + "-" * 120)
print("1. TARGET ACQUISITION COMPONENTS")
print("-" * 120)

for path in TARGET_FILES:
    print()
    print(f"FILE: {rel(path)}")

    if not path.exists():
        print("STATUS: MISSING")
        continue

    print("STATUS: EXISTS")

    defs = definitions(path)

    if defs:
        print(f"DEFINITIONS: {defs}")

    else:
        print("DEFINITIONS: NONE")


print("\n" + "-" * 120)
print("2. ACQUISITION COMPONENT IMPORT GRAPH")
print("-" * 120)

for path in TARGET_FILES:
    if not path.exists():
        continue

    imports_found = imports(path)

    print()
    print(f"FILE: {rel(path)}")

    relevant = [
        item
        for item in imports_found
        if (
            item.startswith("SanskritAI.acquisition")
            or item.startswith("SanskritAI.core")
            or item.startswith("SanskritAI.models")
            or item.startswith("SanskritAI.lexical")
        )
    ]

    if relevant:
        for item in relevant:
            print(f"IMPORT: {item}")
    else:
        print("RELEVANT IMPORTS: NONE")


print("\n" + "-" * 120)
print("3. ACQUISITION CONSTRUCTION / CALL SURFACE")
print("-" * 120)

for path in TARGET_FILES:
    if not path.exists():
        continue

    calls = call_names(path)

    interesting = [
        name
        for name in calls
        if name in {
            "CorpusSource",
            "AcquisitionManifest",
            "AcquisitionRequest",
            "AcquisitionResponse",
            "SourceAcquirer",
            "DefaultSourceAcquirer",
            "AcquisitionManager",
            "ProviderRegistry",
            "CorpusSourceFactory",
        }
    ]

    print()
    print(f"FILE: {rel(path)}")

    if interesting:
        print(
            "TARGET CALLS: "
            + ", ".join(sorted(set(interesting)))
        )
    else:
        print("TARGET CALLS: NONE")


print("\n" + "-" * 120)
print("4. ACQUISITION MODEL SEMANTIC SURFACE")
print("-" * 120)

for path in (
    REPO_ROOT / "acquisition" / "models" / "corpus_source.py",
    REPO_ROOT / "acquisition" / "models" / "acquisition_manifest.py",
):
    if not path.exists():
        continue

    print()
    print(f"FILE: {rel(path)}")

    lines = source_lines(path)

    if lines:
        for line in lines:
            print(line)
    else:
        print("No acquisition-related semantic lines found.")


print("\n" + "-" * 120)
print("5. FACTORY SEMANTIC SURFACE")
print("-" * 120)

factory = (
    REPO_ROOT
    / "acquisition"
    / "factories"
    / "corpus_source_factory.py"
)

if factory.exists():
    print(f"FILE: {rel(factory)}")

    lines = source_lines(factory)

    if lines:
        for line in lines:
            print(line)
    else:
        print("No relevant factory lines found.")
else:
    print("CorpusSourceFactory file missing.")


print("\n" + "-" * 120)
print("6. ACQUISITION MANAGER SEMANTIC SURFACE")
print("-" * 120)

manager = (
    REPO_ROOT
    / "acquisition"
    / "acquisition_manager.py"
)

if manager.exists():
    print(f"FILE: {rel(manager)}")

    lines = source_lines(manager)

    if lines:
        for line in lines:
            print(line)
    else:
        print("No relevant manager lines found.")
else:
    print("AcquisitionManager file missing.")


print("\n" + "-" * 120)
print("7. SOURCE ACQUIRER SEMANTIC SURFACE")
print("-" * 120)

for path in (
    REPO_ROOT
    / "acquisition"
    / "acquirers"
    / "source_acquirer.py",

    REPO_ROOT
    / "acquisition"
    / "acquirers"
    / "default_source_acquirer.py",
):
    if not path.exists():
        continue

    print()
    print(f"FILE: {rel(path)}")

    lines = source_lines(path)

    if lines:
        for line in lines:
            print(line)
    else:
        print("No relevant acquirer lines found.")


print("\n" + "-" * 120)
print("8. PROVIDER REQUEST / RESPONSE SURFACE")
print("-" * 120)

for path in (
    REPO_ROOT
    / "acquisition"
    / "providers"
    / "acquisition_request.py",

    REPO_ROOT
    / "acquisition"
    / "providers"
    / "acquisition_response.py",

    REPO_ROOT
    / "acquisition"
    / "providers"
    / "provider_registry.py",
):
    if not path.exists():
        continue

    print()
    print(f"FILE: {rel(path)}")

    lines = source_lines(path)

    if lines:
        for line in lines:
            print(line)
    else:
        print("No relevant provider lines found.")


print("\n" + "-" * 120)
print("9. ACTUAL EXECUTABLE URL LITERALS")
print("-" * 120)

url_files = []

for path in REPO_ROOT.rglob("*.py"):
    if is_excluded(path):
        continue

    urls = executable_urls(path)

    if urls:
        url_files.append(
            (rel(path), urls)
        )

if not url_files:
    print(
        "No executable URL string literals found."
    )
else:
    for path_name, urls in url_files:
        print()
        print(f"FILE: {path_name}")

        for url in urls:
            print(f"URL: {url}")


print("\n" + "-" * 120)
print("10. AMARAKOSHA ACQUISITION REFERENCES IN ACTUAL CODE")
print("-" * 120)

amarakosha_code_hits = []

for path in REPO_ROOT.rglob("*.py"):
    if is_excluded(path):
        continue

    text = read_text(path)

    if not text:
        continue

    lower = text.lower()

    if (
        "amarakosha" in lower
        or "amarakośa" in lower
        or "अमरकोश" in text
        or "अमरकोष" in text
    ):
        # Ignore audit scripts for the production trace.
        if "scripts/audits/" in rel(path):
            continue

        amarakosha_code_hits.append(
            rel(path)
        )

if not amarakosha_code_hits:
    print(
        "No non-audit Python files reference Amarakośa."
    )
else:
    for path_name in sorted(amarakosha_code_hits):
        print(path_name)


print("\n" + "-" * 120)
print("11. AMARAKOSHA + ACQUISITION CONSTRUCTION EVIDENCE")
print("-" * 120)

construction_evidence = []

for path_name in amarakosha_code_hits:
    path = REPO_ROOT / path_name
    text = read_text(path)

    if not text:
        continue

    lower = text.lower()

    acquisition_terms = (
        "corpus_source",
        "acquisition_manifest",
        "acquisitionmanager",
        "sourceacquirer",
        "defaultsourceacquirer",
        "acquisitionrequest",
        "providerregistry",
        "download",
        "source_url",
        "source_urls",
    )

    matches = [
        term
        for term in acquisition_terms
        if term in lower
    ]

    if matches:
        construction_evidence.append(
            (
                path_name,
                sorted(set(matches)),
            )
        )

if not construction_evidence:
    print(
        "No production Amarakośa → acquisition "
        "construction evidence found."
    )
else:
    for path_name, matches in construction_evidence:
        print()
        print(f"FILE: {path_name}")
        print(
            "ACQUISITION REFERENCES: "
            + ", ".join(matches)
        )


print("\n" + "-" * 120)
print("12. ARCHITECTURAL DECISION GATE")
print("-" * 120)

print(
    "Existing CorpusSource                 : PRESERVE"
)
print(
    "Existing AcquisitionManifest          : PRESERVE"
)
print(
    "Existing AcquisitionManager           : PRESERVE"
)
print(
    "Existing SourceAcquirer               : PRESERVE"
)
print(
    "Existing provider architecture        : PRESERVE"
)
print(
    "Existing AmarakoshaParser             : PRESERVE"
)
print(
    "New Amarakośa source model            : NOT JUSTIFIED"
)
print(
    "New Amarakośa provider                : NOT JUSTIFIED"
)
print(
    "New parser grammar                    : DO NOT IMPLEMENT"
)


print("\n" + "-" * 120)
print("13. DECISION")
print("-" * 120)

if construction_evidence:
    print(
        "PRODUCTION AMARAKOSHA ACQUISITION "
        "BOUNDARY REFERENCES : FOUND"
    )
else:
    print(
        "PRODUCTION AMARAKOSHA ACQUISITION "
        "BOUNDARY REFERENCES : NOT FOUND"
    )

if url_files:
    print(
        "EXECUTABLE URL LITERALS : FOUND"
    )
else:
    print(
        "EXECUTABLE URL LITERALS : NOT FOUND"
    )

if construction_evidence and url_files:
    print(
        "\nNEXT: inspect the specific construction "
        "path before parser implementation."
    )
else:
    print(
        "\nNEXT: inspect concrete acquisition "
        "manifest/provider/resource evidence."
    )

print(
    "\nBATCH 5H-5E-7 STATUS: AUDIT COMPLETE"
)

print("=" * 120)
