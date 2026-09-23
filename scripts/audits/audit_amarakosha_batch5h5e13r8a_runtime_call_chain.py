from __future__ import annotations

from pathlib import Path
import ast
import re
import sys


ROOT = Path("/content/SanskritAI")
ACQUISITION_ROOT = ROOT / "acquisition"

if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))


print("=" * 72)
print("13R-8A — Amarakośa exact acquisition runtime call-chain discovery")
print("=" * 72)
print(f"Repository root : {ROOT}")
print(f"Acquisition root: {ACQUISITION_ROOT}")


# ---------------------------------------------------------------------
# Production-file scope
# ---------------------------------------------------------------------

DUPLICATE_RE = re.compile(r".*_(?:G\d+|\d+)\.py$")


def is_production_python(path: Path) -> bool:
    if not path.is_file():
        return False

    if path.suffix != ".py":
        return False

    if "__pycache__" in path.parts:
        return False

    if "tests" in path.parts:
        return False

    if ".git" in path.parts:
        return False

    if DUPLICATE_RE.match(path.name):
        return False

    return True


files = sorted(
    path
    for path in ACQUISITION_ROOT.rglob("*.py")
    if is_production_python(path)
)

print()
print("-" * 72)
print("Production scope")
print("-" * 72)

print(f"Production acquisition Python files : {len(files)}")


# ---------------------------------------------------------------------
# Target runtime modules
# ---------------------------------------------------------------------

TARGET_FILES = [
    ACQUISITION_ROOT / "acquirers" / "default_source_acquirer.py",
    ACQUISITION_ROOT / "acquirers" / "source_acquirer.py",
    ACQUISITION_ROOT / "pipelines" / "acquisition_pipeline.py",
    ACQUISITION_ROOT / "services" / "acquisition_service.py",
    ACQUISITION_ROOT / "services" / "default_acquisition_service.py",
    ACQUISITION_ROOT / "downloaders" / "local_file_importer.py",
    ACQUISITION_ROOT / "downloaders" / "base_downloader.py",
    ACQUISITION_ROOT / "downloaders" / "http_downloader.py",
    ACQUISITION_ROOT / "models" / "acquisition_manifest.py",
    ACQUISITION_ROOT / "models" / "acquisition_result.py",
    ACQUISITION_ROOT / "models" / "corpus_source.py",
]


print()
print("-" * 72)
print("Target runtime modules")
print("-" * 72)

for path in TARGET_FILES:
    print(
        f"{path.relative_to(ROOT)} : "
        f"{'PASS' if path.exists() else 'MISSING'}"
    )


# ---------------------------------------------------------------------
# AST helpers
# ---------------------------------------------------------------------

def parse(path: Path):
    return ast.parse(
        path.read_text(encoding="utf-8"),
        filename=str(path),
    )


def qualified_call_name(node):
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        parent = qualified_call_name(node.value)
        if parent:
            return f"{parent}.{node.attr}"

    return None


def call_matches(node, names):
    if not isinstance(node, ast.Call):
        return False

    name = qualified_call_name(node.func)
    if not name:
        return False

    return name.split(".")[-1] in names


# ---------------------------------------------------------------------
# Inspect exact runtime modules
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("Exact runtime call sites")
print("-" * 72)


TARGET_CALLS = {
    "acquire",
    "execute",
    "run",
    "process",
    "download",
    "import_file",
    "import_source",
    "copy",
    "copy_file",
    "copy_local_file",
    "validate",
    "validate_checksum",
    "finalize_result",
    "supports",
}


for path in TARGET_FILES:
    if not path.exists():
        continue

    try:
        tree = parse(path)
    except Exception as exc:
        print()
        print(f"{path.relative_to(ROOT)}")
        print(f"  AST parse : FAIL — {exc}")
        continue

    hits = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = qualified_call_name(node.func)
            if name and name.split(".")[-1] in TARGET_CALLS:
                hits.append(
                    (
                        getattr(node, "lineno", "?"),
                        name,
                    )
                )

    if hits:
        print()
        print(path.relative_to(ROOT))
        for lineno, name in sorted(hits):
            print(f"  L{lineno}: {name}")


# ---------------------------------------------------------------------
# Class/method structure
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("Runtime class/method structure")
print("-" * 72)


for path in TARGET_FILES:
    if not path.exists():
        continue

    try:
        tree = parse(path)
    except Exception:
        continue

    classes = [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    ]

    if not classes:
        continue

    print()
    print(path.relative_to(ROOT))

    for cls in classes:
        print(f"  class {cls.name}")

        for node in cls.body:
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ):
                args = [
                    arg.arg
                    for arg in node.args.args
                ]

                print(
                    f"    {node.name}"
                    f"({', '.join(args)})"
                )


# ---------------------------------------------------------------------
# Concrete LocalFileImporter selection evidence
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("LocalFileImporter selection evidence")
print("-" * 72)


local_importer_refs = []

for path in files:
    try:
        tree = parse(path)
    except Exception:
        continue

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if node.id == "LocalFileImporter":
                local_importer_refs.append(
                    (
                        path.relative_to(ROOT),
                        getattr(node, "lineno", "?"),
                        "Name",
                    )
                )

        elif isinstance(node, ast.Attribute):
            if node.attr == "LocalFileImporter":
                local_importer_refs.append(
                    (
                        path.relative_to(ROOT),
                        getattr(node, "lineno", "?"),
                        "Attribute",
                    )
                )

for item in local_importer_refs:
    print(f"{item[0]}:{item[1]} [{item[2]}]")


# ---------------------------------------------------------------------
# DefaultSourceAcquirer dependency evidence
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("DefaultSourceAcquirer dependency evidence")
print("-" * 72)


for path in TARGET_FILES:
    if not path.exists():
        continue

    text = path.read_text(encoding="utf-8")

    interesting = []

    for keyword in (
        "LocalFileImporter",
        "HTTPDownloader",
        "BaseDownloader",
        "destination_directory",
        "source_path",
        "requires_download",
        "requires_checksum_validation",
        "AcquisitionResult",
        "ChecksumValidator",
        "FileValidator",
    ):
        if keyword in text:
            interesting.append(keyword)

    if interesting:
        print()
        print(path.relative_to(ROOT))
        for keyword in interesting:
            print(f"  {keyword}")


# ---------------------------------------------------------------------
# Amarakośa manifest → runtime compatibility
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("Amarakośa manifest compatibility")
print("-" * 72)


try:
    from SanskritAI.acquisition.sources.amarakosha_manifest import (
        create_amarakosha_manifest,
    )

    manifest = create_amarakosha_manifest()

    print("Manifest import : PASS")
    print(f"manifest_id     : {manifest.manifest_id}")
    print(f"source_id       : {manifest.source.source_id}")
    print(f"preferred_format: {manifest.preferred_format}")
    print(f"expected_file   : {manifest.expected_filename}")
    print(f"destination     : {manifest.destination_directory}")
    print(f"requires_download: {manifest.requires_download}")
    print(
        "requires_checksum_validation: "
        f"{manifest.requires_checksum_validation}"
    )

except Exception as exc:
    print(f"Manifest compatibility : FAIL — {exc}")


# ---------------------------------------------------------------------
# Decision
# ---------------------------------------------------------------------

print()
print("=" * 72)
print("13R-8A decision")
print("=" * 72)

print(
    "PASS — exact runtime call-chain discovery completed."
)

print()
print(
    "No Amarakośa-specific acquisition class should be created "
    "until the existing DefaultSourceAcquirer / pipeline / service "
    "selection path is confirmed."
)
