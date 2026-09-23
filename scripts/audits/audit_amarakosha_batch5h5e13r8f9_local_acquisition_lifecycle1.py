from __future__ import annotations

"""
SanskritAI
==========

13R-8F-9 — Local Acquisition Lifecycle & Destination-Safety Audit

Purpose
-------
Audit the generic local acquisition lifecycle after 13R-8F-8.

This audit is READ-ONLY.

It does NOT modify production files.

Primary questions
-----------------
1. Does LocalFileImporter resolve CorpusSource.local_path canonically?
2. Does destination calculation remain safe?
3. Can a local source resolve to the same physical destination?
4. Does BaseDownloader provide the expected lifecycle helpers?
5. Does DefaultSourceAcquirer delegate local sources correctly?
6. Does AcquisitionResult finalize correctly?
7. Does the production Amarakośa manifest represent a safe acquisition target?
8. Are checksum/status fields being incorrectly conflated with local copying?

Architecture
------------
CorpusSource.local_path
        |
        v
LocalFileImporter._resolve_source_path()
        |
        v
LocalFileImporter
        |
        v
AcquisitionResult

DefaultSourceAcquirer
        |
        +---- local source ----> LocalFileImporter
        |
        +---- remote source ---> existing remote path

This audit intentionally does NOT repair any of the above.
"""

# from __future__ import annotations

import ast
import hashlib
import inspect
import sys
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory


REPO_ROOT = Path("/content/SanskritAI").resolve()
WORKSPACE_ROOT = REPO_ROOT.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))


LOCAL_IMPORTER = (
    REPO_ROOT
    / "acquisition"
    / "downloaders"
    / "local_file_importer.py"
)

BASE_DOWNLOADER = (
    REPO_ROOT
    / "acquisition"
    / "downloaders"
    / "base_downloader.py"
)

DEFAULT_SOURCE_ACQUIRER = (
    REPO_ROOT
    / "acquisition"
    / "acquirers"
    / "default_source_acquirer.py"
)

ACQUISITION_RESULT = (
    REPO_ROOT
    / "acquisition"
    / "models"
    / "acquisition_result.py"
)

ACQUISITION_MANIFEST = (
    REPO_ROOT
    / "acquisition"
    / "models"
    / "acquisition_manifest.py"
)

AMARAKOSHA_SOURCE = (
    REPO_ROOT
    / "acquisition"
    / "sources"
    / "amarakosha.py"
)

AMARAKOSHA_MANIFEST = (
    REPO_ROOT
    / "acquisition"
    / "sources"
    / "amarakosha_manifest.py"
)

AMARAKOSHA_ARTIFACT = REPO_ROOT / "amarakosha.txt"


def banner(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def syntax_check(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    ast.parse(source, filename=str(path))
    print(f"{path}: Python syntax PASS")


def get_class(tree: ast.AST, name: str):
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    return None


def get_method(class_node: ast.ClassDef, name: str):
    for node in class_node.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == name:
                return node
    return None


def method_source(path: Path, class_name: str, method_name: str) -> str:
    tree = ast.parse(
        path.read_text(encoding="utf-8"),
        filename=str(path),
    )

    cls = get_class(tree, class_name)
    if cls is None:
        raise RuntimeError(
            f"Class {class_name!r} not found in {path}"
        )

    method = get_method(cls, method_name)
    if method is None:
        raise RuntimeError(
            f"Method {method_name!r} not found in {class_name}"
        )

    lines = path.read_text(encoding="utf-8").splitlines()
    return "\n".join(
        lines[method.lineno - 1 : method.end_lineno]
    )


def has_call(source: str, name: str) -> bool:
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func

            if isinstance(func, ast.Name):
                if func.id == name:
                    return True

            if isinstance(func, ast.Attribute):
                if func.attr == name:
                    return True

    return False


def contains_attribute_access(
    source: str,
    attribute: str,
) -> bool:
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            if node.attr == attribute:
                return True

    return False


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def physical_same_path(a: Path, b: Path) -> bool:
    try:
        return a.resolve(strict=False) == b.resolve(strict=False)
    except Exception:
        return a.absolute() == b.absolute()


banner(
    "13R-8F-9 — Local Acquisition Lifecycle & Destination-Safety Audit"
)

print(f"Repository root : {REPO_ROOT}")
print(f"Workspace root  : {WORKSPACE_ROOT}")


# ----------------------------------------------------------------------
# 1. Syntax
# ----------------------------------------------------------------------

banner("1. Production Python syntax")

for path in (
    LOCAL_IMPORTER,
    BASE_DOWNLOADER,
    DEFAULT_SOURCE_ACQUIRER,
    ACQUISITION_RESULT,
    ACQUISITION_MANIFEST,
    AMARAKOSHA_SOURCE,
    AMARAKOSHA_MANIFEST,
):
    if path.exists():
        syntax_check(path)
    else:
        print(f"WARNING: missing production file: {path}")


# ----------------------------------------------------------------------
# 2. LocalFileImporter contract
# ----------------------------------------------------------------------

banner("2. LocalFileImporter structural contract")

local_source = method_source(
    LOCAL_IMPORTER,
    "LocalFileImporter",
    "_resolve_source_path",
)

supports_source = method_source(
    LOCAL_IMPORTER,
    "LocalFileImporter",
    "supports",
)

download_source = method_source(
    LOCAL_IMPORTER,
    "LocalFileImporter",
    "download",
)

assert (
    contains_attribute_access(
        local_source,
        "local_path",
    )
    or '"local_path"' in local_source
), "Resolver does not reference canonical local_path"

assert '"source_path"' in local_source, (
    "Resolver does not contain metadata compatibility fallback"
)

assert has_call(
    supports_source,
    "_resolve_source_path",
), "supports() does not delegate to _resolve_source_path()"

assert has_call(
    download_source,
    "_resolve_source_path",
), "download() does not delegate to _resolve_source_path()"

print("Canonical resolver: PASS")
print("supports() delegation: PASS")
print("download() delegation: PASS")


# ----------------------------------------------------------------------
# 3. BaseDownloader lifecycle helpers
# ----------------------------------------------------------------------

banner("3. BaseDownloader lifecycle contract")

base_source = BASE_DOWNLOADER.read_text(encoding="utf-8")

for helper in (
    "destination_file",
    "validate_destination",
    "remove_existing",
    "finalize_result",
):
    if f"def {helper}" in base_source:
        print(f"{helper}(): PRESENT")
    else:
        print(f"WARNING: {helper}(): NOT FOUND")


# ----------------------------------------------------------------------
# 4. LocalFileImporter helper usage
# ----------------------------------------------------------------------

banner("4. LocalFileImporter helper usage")

for method_name, source in (
    ("download", download_source),
):
    for helper in (
        "validate_destination",
        "finalize_result",
        "destination_file",
        "remove_existing",
    ):
        print(
            f"{method_name} -> {helper}(): "
            f"{'PASS' if has_call(source, helper) else 'NOT DIRECTLY USED'}"
        )


# ----------------------------------------------------------------------
# 5. AcquisitionResult lifecycle
# ----------------------------------------------------------------------

banner("5. AcquisitionResult lifecycle contract")

result_source = ACQUISITION_RESULT.read_text(
    encoding="utf-8"
)

for method_name in (
    "finalize",
    "mark_success",
    "add_error",
    "add_downloaded_file",
):
    if f"def {method_name}" in result_source:
        print(f"{method_name}(): PRESENT")
    else:
        print(f"WARNING: {method_name}(): NOT FOUND")


# ----------------------------------------------------------------------
# 6. DefaultSourceAcquirer local dispatch
# ----------------------------------------------------------------------

banner("6. DefaultSourceAcquirer local dispatch")

acquirer_source = DEFAULT_SOURCE_ACQUIRER.read_text(
    encoding="utf-8"
)

if "LocalFileImporter" in acquirer_source:
    print("LocalFileImporter reference: PRESENT")
else:
    print("BLOCKER: LocalFileImporter reference missing")

if "supports(" in acquirer_source:
    print("Importer capability dispatch evidence: PRESENT")
else:
    print(
        "WARNING: no obvious supports() dispatch evidence"
    )


# ----------------------------------------------------------------------
# 7. Amarakośa artifact integrity
# ----------------------------------------------------------------------

banner("7. Amarakośa canonical artifact integrity")

if not AMARAKOSHA_ARTIFACT.is_file():
    raise RuntimeError(
        f"Missing canonical artifact: {AMARAKOSHA_ARTIFACT}"
    )

artifact_size = AMARAKOSHA_ARTIFACT.stat().st_size
artifact_hash = hash_file(AMARAKOSHA_ARTIFACT)

print(f"Artifact : {AMARAKOSHA_ARTIFACT}")
print(f"Size     : {artifact_size}")
print(f"SHA256   : {artifact_hash}")


# ----------------------------------------------------------------------
# 8. Production manifest inspection
# ----------------------------------------------------------------------

banner("8. Production Amarakośa manifest")

from SanskritAI.acquisition.sources.amarakosha import (
    create_amarakosha_source,
)

from SanskritAI.acquisition.sources.amarakosha_manifest import (
    create_amarakosha_manifest,
)

source = create_amarakosha_source()
manifest = create_amarakosha_manifest()

print(f"source_id       : {source.source_id}")
print(f"source_type     : {source.source_type}")
print(f"source_format   : {source.source_format}")
print(f"source.local_path: {source.local_path}")
print(f"manifest_id     : {manifest.manifest_id}")
print(f"destination     : {manifest.destination_directory}")
print(f"expected_filename: {manifest.expected_filename}")
print(f"expected_size   : {manifest.expected_size}")
print(f"checksum        : {manifest.checksum}")
print(f"overwrite       : {manifest.overwrite_existing}")
print(f"urls            : {manifest.urls}")
print(f"mirrors         : {manifest.mirrors}")


# ----------------------------------------------------------------------
# 9. Source / destination safety
# ----------------------------------------------------------------------

banner("9. Source / destination safety")

source_path = Path(source.local_path)

if manifest.destination_directory is None:
    print(
        "BLOCKER: production manifest has no destination directory"
    )
else:
    destination_directory = Path(
        manifest.destination_directory
    )

    expected_filename = (
        manifest.expected_filename
        or source_path.name
    )

    destination_path = (
        destination_directory
        / expected_filename
    )

    print(f"source path      : {source_path}")
    print(f"destination path : {destination_path}")

    same_path = physical_same_path(
        source_path,
        destination_path,
    )

    print(
        "source == destination: "
        f"{'WARNING / BLOCKER CANDIDATE' if same_path else 'PASS'}"
    )

    if same_path:
        print()
        print(
            "IMPORTANT:"
        )
        print(
            "The production manifest resolves the local source "
            "and acquisition destination to the same physical file."
        )
        print(
            "This must be resolved at the manifest/lifecycle level "
            "before production acquisition is executed."
        )


# ----------------------------------------------------------------------
# 10. Read-only isolated runtime test
# ----------------------------------------------------------------------

banner("10. Isolated LocalFileImporter runtime")

from SanskritAI.acquisition.downloaders.local_file_importer import (
    LocalFileImporter,
)

with TemporaryDirectory() as temp_dir:
    destination = Path(temp_dir) / "destination"
    destination.mkdir()

    # Prevent production-manifest mutation.
    isolated_manifest = replace(
        manifest,
        destination_directory=destination,
        metadata=dict(manifest.metadata),
    )

    importer = LocalFileImporter()

    supports = importer.supports(
        isolated_manifest
    )

    print(
        f"LocalFileImporter.supports(): "
        f"{supports}"
    )

    if not supports:
        raise RuntimeError(
            "LocalFileImporter unexpectedly rejected "
            "canonical local source"
        )

    result = importer.download(
        isolated_manifest
    )

    print(
        f"AcquisitionResult.success : "
        f"{result.success}"
    )

    print(
        f"AcquisitionResult.message : "
        f"{result.message}"
    )

    print(
        f"bytes_downloaded         : "
        f"{result.bytes_downloaded}"
    )

    print(
        f"downloaded_files         : "
        f"{result.downloaded_files}"
    )

    print(
        f"errors                   : "
        f"{result.errors}"
    )

    print(
        f"warnings                 : "
        f"{result.warnings}"
    )

    if not result.success:
        raise RuntimeError(
            "Isolated LocalFileImporter runtime failed"
        )

    if not result.downloaded_files:
        raise RuntimeError(
            "Successful local acquisition produced no "
            "downloaded_files"
        )

    copied = result.downloaded_files[0]

    copied_size = copied.stat().st_size
    copied_hash = hash_file(copied)

    print(f"copied size             : {copied_size}")
    print(f"copied SHA256           : {copied_hash}")

    assert copied_size == artifact_size
    assert copied_hash == artifact_hash

    print(
        "Copied artifact size/hash: PASS"
    )


# ----------------------------------------------------------------------
# 11. Production immutability
# ----------------------------------------------------------------------

banner("11. Production artifact immutability")

post_size = AMARAKOSHA_ARTIFACT.stat().st_size
post_hash = hash_file(AMARAKOSHA_ARTIFACT)

assert post_size == artifact_size
assert post_hash == artifact_hash

print(
    "amarakosha.txt unchanged during audit: PASS"
)


# ----------------------------------------------------------------------
# Final classification
# ----------------------------------------------------------------------

banner("13R-8F-9 RESULT")

if manifest.destination_directory is not None:
    destination_path = (
        Path(manifest.destination_directory)
        / (
            manifest.expected_filename
            or source_path.name
        )
    )

    if physical_same_path(
        source_path,
        destination_path,
    ):
        print(
            "AUDIT COMPLETE — lifecycle code is structurally "
            "healthy, but production Amarakośa acquisition "
            "destination is source-identical."
        )
        print()
        print(
            "NEXT DECISION REQUIRED:"
        )
        print(
            "Determine whether the production manifest is intended "
            "to be an acquisition registration manifest only, or "
            "whether acquire() is expected to physically copy the "
            "artifact."
        )
        print()
        print(
            "Do NOT repair LocalFileImporter yet."
        )
    else:
        print(
            "13R-8F-9 COMPLETE — no source/destination collision."
        )
else:
    print(
        "13R-8F-9 COMPLETE — manifest destination requires review."
    )
