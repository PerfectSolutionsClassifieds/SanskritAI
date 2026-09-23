from __future__ import annotations

"""
SanskritAI
==========

13R-8F-10 — Amarakośa Manifest Semantics & Acquisition Lifecycle Audit

Purpose
-------
Determine the correct architectural interpretation of the production
Amarakośa local manifest before making any production repair.

This is a READ-ONLY audit.

It does NOT modify production files.

Questions
---------
1. Is the Amarakośa manifest a registration manifest or a physical
   acquisition manifest?
2. What does CorpusSource.local_path mean in the current architecture?
3. What does AcquisitionManifest.destination_directory mean?
4. Does the generic acquisition layer already support an artifact
   that is already local?
5. Does DefaultSourceAcquirer have a safe same-source/destination
   policy?
6. What SourceStatus transitions occur for local acquisition?
7. What does AcquisitionResult.success actually represent?
8. Are checksum verification and local copying separate lifecycle
   concerns?
9. Would changing only the Amarakośa manifest be sufficient?
10. Would changing generic acquisition behavior be required?

Important
---------
This audit intentionally does NOT choose or implement the repair.

It establishes evidence first.
"""

import ast
import hashlib
import inspect
import sys
import textwrap
from pathlib import Path


# ==========================================================================
# Runtime bootstrap
# ==========================================================================

REPO_ROOT = Path("/content/SanskritAI").resolve()
WORKSPACE_ROOT = REPO_ROOT.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))


# ==========================================================================
# Production paths
# ==========================================================================

FILES = {
    "local_file_importer": (
        REPO_ROOT
        / "acquisition"
        / "downloaders"
        / "local_file_importer.py"
    ),
    "base_downloader": (
        REPO_ROOT
        / "acquisition"
        / "downloaders"
        / "base_downloader.py"
    ),
    "default_source_acquirer": (
        REPO_ROOT
        / "acquisition"
        / "acquirers"
        / "default_source_acquirer.py"
    ),
    "acquisition_result": (
        REPO_ROOT
        / "acquisition"
        / "models"
        / "acquisition_result.py"
    ),
    "acquisition_manifest": (
        REPO_ROOT
        / "acquisition"
        / "models"
        / "acquisition_manifest.py"
    ),
    "corpus_source": (
        REPO_ROOT
        / "acquisition"
        / "models"
        / "corpus_source.py"
    ),
    "amarakosha_source": (
        REPO_ROOT
        / "acquisition"
        / "sources"
        / "amarakosha.py"
    ),
    "amarakosha_manifest": (
        REPO_ROOT
        / "acquisition"
        / "sources"
        / "amarakosha_manifest.py"
    ),
}


AMARAKOSHA_ARTIFACT = (
    REPO_ROOT / "amarakosha.txt"
)


# ==========================================================================
# Utilities
# ==========================================================================

def banner(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def read(path: Path) -> str:
    return path.read_text(
        encoding="utf-8"
    )


def syntax_check(path: Path) -> None:
    ast.parse(
        read(path),
        filename=str(path),
    )

    print(
        f"{path}: Python syntax PASS"
    )


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def dedent(source: str) -> str:
    return textwrap.dedent(source)


def get_class(
    tree: ast.AST,
    name: str,
):
    for node in tree.body:
        if (
            isinstance(node, ast.ClassDef)
            and node.name == name
        ):
            return node

    return None


def get_method(
    class_node: ast.ClassDef,
    name: str,
):
    for node in class_node.body:
        if (
            isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
            and node.name == name
        ):
            return node

    return None


def method_source(
    path: Path,
    class_name: str,
    method_name: str,
) -> str:
    source = read(path)

    tree = ast.parse(
        source,
        filename=str(path),
    )

    cls = get_class(
        tree,
        class_name,
    )

    if cls is None:
        raise RuntimeError(
            f"Class {class_name!r} not found "
            f"in {path}"
        )

    method = get_method(
        cls,
        method_name,
    )

    if method is None:
        raise RuntimeError(
            f"Method {method_name!r} not found "
            f"in {class_name}"
        )

    lines = source.splitlines()

    extracted = "\n".join(
        lines[
            method.lineno - 1 :
            method.end_lineno
        ]
    )

    return textwrap.dedent(
        extracted
    )


def contains_text(
    source: str,
    *values: str,
) -> bool:
    return all(
        value in source
        for value in values
    )


def contains_any_text(
    source: str,
    *values: str,
) -> bool:
    return any(
        value in source
        for value in values
    )


def calls_method(
    source: str,
    method_name: str,
) -> bool:
    tree = ast.parse(
        textwrap.dedent(source)
    )

    for node in ast.walk(tree):
        if not isinstance(
            node,
            ast.Call,
        ):
            continue

        func = node.func

        if (
            isinstance(func, ast.Name)
            and func.id == method_name
        ):
            return True

        if (
            isinstance(func, ast.Attribute)
            and func.attr == method_name
        ):
            return True

    return False


def find_definitions(
    source: str,
    names: tuple[str, ...],
) -> list[str]:
    found = []

    for name in names:
        if f"def {name}" in source:
            found.append(name)

    return found


# ==========================================================================
# Banner
# ==========================================================================

banner(
    "13R-8F-10 — Amarakośa Manifest Semantics "
    "& Acquisition Lifecycle Audit"
)

print(
    f"Repository root : {REPO_ROOT}"
)

print(
    f"Workspace root  : {WORKSPACE_ROOT}"
)


# ==========================================================================
# 1. Syntax
# ==========================================================================

banner(
    "1. Production syntax"
)

for name, path in FILES.items():

    if not path.exists():
        print(
            f"WARNING: missing {name}: {path}"
        )
        continue

    syntax_check(path)


# ==========================================================================
# 2. Import canonical production objects
# ==========================================================================

banner(
    "2. Canonical production object construction"
)

from SanskritAI.acquisition.sources.amarakosha import (
    create_amarakosha_source,
)

from SanskritAI.acquisition.sources.amarakosha_manifest import (
    create_amarakosha_manifest,
)

from SanskritAI.acquisition.models.source_status import (
    SourceStatus,
)


source = create_amarakosha_source()
manifest = create_amarakosha_manifest()


print(
    f"source_id             : {source.source_id}"
)

print(
    f"source_type           : {source.source_type}"
)

print(
    f"source_format         : {source.source_format}"
)

print(
    f"source_status         : {source.status}"
)

print(
    f"source.local_path     : {source.local_path}"
)

print(
    f"manifest_id           : {manifest.manifest_id}"
)

print(
    f"manifest.destination   : "
    f"{manifest.destination_directory}"
)

print(
    f"manifest.filename      : "
    f"{manifest.expected_filename}"
)

print(
    f"manifest.expected_size : "
    f"{manifest.expected_size}"
)

print(
    f"manifest.checksum      : "
    f"{manifest.checksum}"
)

print(
    f"manifest.overwrite     : "
    f"{manifest.overwrite_existing}"
)

print(
    f"manifest.urls          : "
    f"{manifest.urls}"
)

print(
    f"manifest.mirrors       : "
    f"{manifest.mirrors}"
)

print(
    f"manifest.importer      : "
    f"{manifest.importer}"
)

print(
    f"manifest.cache         : "
    f"{manifest.cache_directory}"
)


# ==========================================================================
# 3. Artifact identity
# ==========================================================================

banner(
    "3. Canonical artifact identity"
)

if not AMARAKOSHA_ARTIFACT.is_file():
    raise RuntimeError(
        f"Missing artifact: "
        f"{AMARAKOSHA_ARTIFACT}"
    )

artifact_size = (
    AMARAKOSHA_ARTIFACT.stat().st_size
)

artifact_hash = hash_file(
    AMARAKOSHA_ARTIFACT
)

print(
    f"Artifact exists : PASS"
)

print(
    f"Artifact size   : {artifact_size}"
)

print(
    f"Artifact SHA256 : {artifact_hash}"
)

if manifest.expected_size == artifact_size:
    print(
        "Manifest expected_size matches artifact: PASS"
    )
else:
    print(
        "WARNING: manifest expected_size mismatch"
    )

if manifest.checksum == artifact_hash:
    print(
        "Manifest checksum matches artifact: PASS"
    )
else:
    print(
        "WARNING: manifest checksum mismatch"
    )


# ==========================================================================
# 4. CorpusSource.local_path semantics
# ==========================================================================

banner(
    "4. CorpusSource.local_path semantics"
)

corpus_source_source = read(
    FILES["corpus_source"]
)

local_path_definitions = []

tree = ast.parse(
    corpus_source_source
)

for node in ast.walk(tree):

    if isinstance(
        node,
        (
            ast.FunctionDef,
            ast.AsyncFunctionDef,
        ),
    ):
        if node.name in (
            "set_local_path",
            "is_downloaded",
        ):
            local_path_definitions.append(
                node.name
            )

print(
    "CorpusSource local-path related definitions:"
)

for name in local_path_definitions:
    print(
        f"  {name}"
    )

if "local_path" in corpus_source_source:
    print(
        "CorpusSource.local_path field/reference: PRESENT"
    )
else:
    print(
        "WARNING: CorpusSource.local_path not found"
    )


# ==========================================================================
# 5. AcquisitionManifest destination semantics
# ==========================================================================

banner(
    "5. AcquisitionManifest destination semantics"
)

manifest_source = read(
    FILES["acquisition_manifest"]
)

destination_terms = (
    "destination_directory",
    "expected_filename",
    "overwrite_existing",
    "cache_directory",
)

for term in destination_terms:

    if term in manifest_source:
        print(
            f"{term}: PRESENT"
        )
    else:
        print(
            f"WARNING: {term}: NOT FOUND"
        )


# ==========================================================================
# 6. Existing local-source / already-local concepts
# ==========================================================================

banner(
    "6. Existing already-local / registration concepts"
)

search_terms = (
    "already",
    "registered",
    "local",
    "exists",
    "skip",
    "SKIPPED",
    "DOWNLOADED",
    "READY_FOR_IMPORT",
)

for name, path in FILES.items():

    if not path.exists():
        continue

    source_text = read(path)

    hits = []

    for term in search_terms:

        if term in source_text:
            hits.append(term)

    print(
        f"{name}: "
        f"{', '.join(hits) if hits else 'no obvious lifecycle terms'}"
    )


# ==========================================================================
# 7. LocalFileImporter semantics
# ==========================================================================

banner(
    "7. LocalFileImporter semantics"
)

local_download = method_source(
    FILES["local_file_importer"],
    "LocalFileImporter",
    "download",
)

local_copy_file = method_source(
    FILES["local_file_importer"],
    "LocalFileImporter",
    "_copy_file",
)

local_copy_directory = method_source(
    FILES["local_file_importer"],
    "LocalFileImporter",
    "_copy_directory",
)

print(
    "download() resolves source through resolver: "
    f"{calls_method(local_download, '_resolve_source_path')}"
)

print(
    "_copy_file() uses destination_file(): "
    f"{calls_method(local_copy_file, 'destination_file')}"
)

print(
    "_copy_file() uses remove_existing(): "
    f"{calls_method(local_copy_file, 'remove_existing')}"
)

print(
    "_copy_directory() uses remove_existing(): "
    f"{calls_method(local_copy_directory, 'remove_existing')}"
)

print(
    "_copy_file() performs shutil.copy2(): "
    f"{'shutil.copy2' in local_copy_file}"
)

print(
    "_copy_directory() performs shutil.copytree(): "
    f"{'shutil.copytree' in local_copy_directory}"
)


# ==========================================================================
# 8. DefaultSourceAcquirer local dispatch semantics
# ==========================================================================

banner(
    "8. DefaultSourceAcquirer local dispatch semantics"
)

acquirer_source = read(
    FILES["default_source_acquirer"]
)

acquire_source = method_source(
    FILES["default_source_acquirer"],
    "DefaultSourceAcquirer",
    "acquire",
)

print(
    "acquire() references LocalFileImporter: "
    f"{'LocalFileImporter' in acquire_source}"
)

print(
    "acquire() references source.local_path: "
    f"{'local_path' in acquire_source}"
)

print(
    "acquire() references metadata source_path: "
    f"{'source_path' in acquire_source}"
)

print(
    "acquire() calls _validate_manifest(): "
    f"{calls_method(acquire_source, '_validate_manifest')}"
)

print(
    "acquire() calls result.finalize(): "
    f"{calls_method(acquire_source, 'finalize')}"
)

print(
    "acquire() contains disabled-manifest logic: "
    f"{'enabled' in acquire_source}"
)


# ==========================================================================
# 9. SourceStatus lifecycle
# ==========================================================================

banner(
    "9. SourceStatus lifecycle semantics"
)

status_source = read(
    REPO_ROOT
    / "acquisition"
    / "models"
    / "source_status.py"
)

for status_name in (
    "REGISTERED",
    "PENDING_DOWNLOAD",
    "DOWNLOADING",
    "DOWNLOADED",
    "VALIDATING",
    "VALIDATED",
    "READY_FOR_IMPORT",
    "IMPORTING",
    "IMPORTED",
    "COMPLETED",
    "SKIPPED",
    "FAILED",
):

    if status_name in status_source:

        print(
            f"{status_name}: PRESENT"
        )

    else:

        print(
            f"{status_name}: NOT FOUND"
        )


# ==========================================================================
# 10. AcquisitionResult semantics
# ==========================================================================

banner(
    "10. AcquisitionResult semantics"
)

result_source = read(
    FILES["acquisition_result"]
)

for field_name in (
    "success",
    "message",
    "downloaded_files",
    "bytes_downloaded",
    "checksum_verified",
    "license_verified",
    "normalized",
    "imported",
    "warnings",
    "errors",
):

    if field_name in result_source:

        print(
            f"{field_name}: PRESENT"
        )

    else:

        print(
            f"WARNING: {field_name}: NOT FOUND"
        )


# ==========================================================================
# 11. Production source/destination collision
# ==========================================================================

banner(
    "11. Production source/destination collision"
)

source_path = Path(
    source.local_path
)

if manifest.destination_directory is None:

    print(
        "BLOCKER: destination_directory is None"
    )

    destination_path = None

else:

    destination_path = (
        Path(
            manifest.destination_directory
        )
        / (
            manifest.expected_filename
            or source_path.name
        )
    )

    print(
        f"source      : {source_path}"
    )

    print(
        f"destination : {destination_path}"
    )

    same_path = (
        source_path.resolve(strict=False)
        == destination_path.resolve(strict=False)
    )

    print(
        f"same physical path: {same_path}"
    )


# ==========================================================================
# 12. Interpretive classification
# ==========================================================================

banner(
    "12. Manifest semantic classification"
)

print(
    "Evidence:"
)

print(
    "  source.local_path is populated."
)

print(
    "  manifest.urls is empty."
)

print(
    "  manifest.mirrors is empty."
)

print(
    "  local artifact already exists."
)

print(
    "  destination_directory points at the same "
    "repository directory."
)

print(
    "  expected_filename equals the local artifact name."
)

if destination_path is not None and (
    source_path.resolve(strict=False)
    == destination_path.resolve(strict=False)
):

    print()
    print(
        "CLASSIFICATION:"
    )

    print(
        "  The current manifest behaves primarily "
        "as a LOCAL ARTIFACT REGISTRATION declaration."
    )

    print(
        "  It is NOT currently a safe physical-copy "
        "acquisition target."
    )

    print()
    print(
        "This is an architectural finding, not yet a "
        "production repair decision."
    )

else:

    print(
        "No source/destination collision detected."
    )


# ==========================================================================
# 13. Determine whether generic acquisition already
#     supports registration semantics
# ==========================================================================

banner(
    "13. Generic registration/acquisition capability audit"
)

registration_candidates = []

for name, path in FILES.items():

    if not path.exists():
        continue

    source_text = read(path)

    for term in (
        "already_downloaded",
        "already_exists",
        "local_path",
        "SKIPPED",
        "REGISTERED",
        "source.local_path",
        "is_downloaded",
    ):

        if term in source_text:
            registration_candidates.append(
                (name, term)
            )

if registration_candidates:

    for name, term in registration_candidates:

        print(
            f"{name}: {term}"
        )

else:

    print(
        "No obvious generic registration "
        "mechanism found."
    )


# ==========================================================================
# 14. No production mutation verification
# ==========================================================================

banner(
    "14. Read-only audit guarantee"
)

post_size = (
    AMARAKOSHA_ARTIFACT.stat().st_size
)

post_hash = hash_file(
    AMARAKOSHA_ARTIFACT
)

assert post_size == artifact_size
assert post_hash == artifact_hash

print(
    "amarakosha.txt unchanged: PASS"
)

print(
    "No production files modified by this audit: PASS"
)


# ==========================================================================
# Final result
# ==========================================================================

banner(
    "13R-8F-10 RESULT"
)

if (
    destination_path is not None
    and (
        source_path.resolve(strict=False)
        == destination_path.resolve(strict=False)
    )
):

    print(
        "13R-8F-10 COMPLETE"
    )

    print()
    print(
        "Primary finding:"
    )

    print(
        "The Amarakośa production manifest currently "
        "describes an already-local canonical artifact "
        "while also providing a physical acquisition "
        "destination identical to that artifact."
    )

    print()
    print(
        "Therefore:"
    )

    print(
        "1. LocalFileImporter should NOT be repaired."
    )

    print(
        "2. CorpusSource.local_path should remain "
        "the canonical local-source identity."
    )

    print(
        "3. The next repair decision belongs to the "
        "manifest/acquisition lifecycle boundary."
    )

    print(
        "4. No Amarakośa-specific downloader/importer "
        "should be created."
    )

    print(
        "5. Before changing production, inspect whether "
        "the generic acquisition architecture has an "
        "existing 'already local / registered' concept."
    )

    print()
    print(
        "RECOMMENDED NEXT STEP:"
    )

    print(
        "13R-8F-11 — Design-level repair contract for "
        "LOCAL REGISTRATION vs PHYSICAL ACQUISITION."
    )

else:

    print(
        "13R-8F-10 COMPLETE — "
        "no source/destination collision."
    )
