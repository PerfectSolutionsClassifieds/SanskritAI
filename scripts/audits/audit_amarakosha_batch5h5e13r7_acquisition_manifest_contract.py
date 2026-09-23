
from __future__ import annotations

"""
SanskritAI
==========

13R-7 — Amarakośa AcquisitionManifest Contract Audit
------------------------------------------------------

Read-only audit of the ACTUAL LOCAL AcquisitionManifest contract.

The local production implementation is:

    SanskritAI.acquisition.models.acquisition_manifest.AcquisitionManifest

This audit does NOT copy the public GitHub Monier-Williams
manifest implementation.

It:

1. Locates the actual local AcquisitionManifest implementation.
2. Inspects its constructor.
3. Verifies its dataclass fields.
4. Constructs an Amarakośa AcquisitionManifest using the
   actual local constructor.
5. Verifies the manifest semantics against the already verified
   local Amarakośa artifact.

Production files are NOT modified.

13R sequence:

    13R-6  CorpusSource
       ↓
    13R-7  AcquisitionManifest
       ↓
    13R-8  Runtime acquisition
       ↓
    13R-9  Existing Amarakośa parser/importer
       ↓
    13R-10 Canonical lexical bridge
"""

# from __future__ import annotations

import ast
import dataclasses
import importlib
import inspect
import sys
from pathlib import Path
from typing import Any


# ----------------------------------------------------------------------
# Repository
# ----------------------------------------------------------------------

REPO_ROOT = Path("/content/SanskritAI")


# ----------------------------------------------------------------------
# Verified Amarakośa artifact
# ----------------------------------------------------------------------

AMARAKOSHA_ARTIFACT = (
    REPO_ROOT / "amarakosha.txt"
)

AMARAKOSHA_SOURCE_ID = "amarakosha"

AMARAKOSHA_NAME = "Amarakośa"

AMARAKOSHA_SHA256 = (
    "d82a5234e4bc15ef295b1b375a6548e02df9a10d6eb94e0f97223289c46c3190"
)

AMARAKOSHA_PROVENANCE_URL = (
    "http://sanskrit.uohyd.ac.in/scl/"
)

AMARAKOSHA_MANIFEST_ID = (
    "amarakosha-local-txt"
)


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def fail(message: str) -> None:
    raise RuntimeError(message)


def bootstrap() -> None:
    if not REPO_ROOT.exists():
        fail(
            f"Repository root not found: {REPO_ROOT}"
        )

    parent = REPO_ROOT.parent

    if str(parent) not in sys.path:
        sys.path.insert(0, str(parent))


def is_historical_or_duplicate(path: Path) -> bool:
    """
    Ignore historical/duplicate Python files.

    User-required audit rule:

        * files ending with numeric suffixes
        * files containing _G<number>
        * audit scripts
        * repair scripts
        * __pycache__
    """

    if "__pycache__" in path.parts:
        return True

    stem = path.stem

    if stem.startswith("audit_"):
        return True

    if stem.startswith("repair_"):
        return True

    # Ignore files ending in a numeric suffix:
    #
    # example:
    #
    # foo1.py
    # foo2.py
    # foo10.py
    #
    if stem and stem[-1].isdigit():
        index = len(stem) - 1

        while index >= 0 and stem[index].isdigit():
            index -= 1

        if index >= 0:
            return True

    # Ignore _G<number>.py
    if "_G" in stem:
        suffix = stem.rsplit("_G", 1)[-1]

        if suffix.isdigit():
            return True

    return False


# ----------------------------------------------------------------------
# Locate actual AcquisitionManifest source
# ----------------------------------------------------------------------

def locate_acquisition_manifest_source() -> tuple[str, Path]:

    acquisition_root = (
        REPO_ROOT / "acquisition"
    )

    if not acquisition_root.exists():
        fail(
            f"Acquisition package not found: "
            f"{acquisition_root}"
        )

    candidates: list[tuple[str, Path]] = []

    for path in acquisition_root.rglob("*.py"):

        if is_historical_or_duplicate(path):
            continue

        try:
            source = path.read_text(
                encoding="utf-8"
            )
        except Exception:
            continue

        try:
            tree = ast.parse(
                source,
                filename=str(path),
            )
        except SyntaxError:
            continue

        found = False

        for node in ast.walk(tree):
            if (
                isinstance(node, ast.ClassDef)
                and node.name == "AcquisitionManifest"
            ):
                found = True
                break

        if not found:
            continue

        relative = path.relative_to(
            REPO_ROOT
        )

        module_parts = list(
            relative.with_suffix("").parts
        )

        module_name = (
            "SanskritAI."
            + ".".join(module_parts)
        )

        candidates.append(
            (module_name, path)
        )

    if not candidates:
        fail(
            "No production AcquisitionManifest "
            "class found under acquisition/."
        )

    if len(candidates) > 1:

        print()
        print(
            "WARNING: multiple production "
            "AcquisitionManifest definitions found:"
        )

        for module_name, path in candidates:
            print(
                f"  {module_name} -> {path}"
            )

        candidates.sort(
            key=lambda item: (
                len(item[1].parts),
                str(item[1]),
            )
        )

    return candidates[0]


# ----------------------------------------------------------------------
# Import actual class
# ----------------------------------------------------------------------

def import_manifest_class(
    module_name: str,
) -> type:

    module = importlib.import_module(
        module_name
    )

    if not hasattr(
        module,
        "AcquisitionManifest",
    ):
        fail(
            f"{module_name} does not expose "
            "AcquisitionManifest."
        )

    cls = getattr(
        module,
        "AcquisitionManifest",
    )

    if not inspect.isclass(cls):
        fail(
            "AcquisitionManifest is not a class."
        )

    return cls


# ----------------------------------------------------------------------
# Constructor inspection
# ----------------------------------------------------------------------

def inspect_constructor(
    cls: type,
) -> inspect.Signature:

    signature = inspect.signature(cls)

    print()
    print(
        "Actual local AcquisitionManifest constructor:"
    )
    print()
    print(
        f"  {cls.__module__}."
        f"{cls.__name__}"
    )
    print(
        f"  signature = {signature}"
    )

    print()
    print("Constructor parameters:")

    for name, parameter in (
        signature.parameters.items()
    ):

        annotation = parameter.annotation

        if (
            annotation
            is inspect.Parameter.empty
        ):
            annotation_text = "<empty>"
        else:
            annotation_text = repr(
                annotation
            )

        if (
            parameter.default
            is inspect.Parameter.empty
        ):
            default_text = "<required>"
        else:
            default_text = repr(
                parameter.default
            )

        print(
            f"  {name}"
            f" | kind={parameter.kind}"
            f" | annotation={annotation_text}"
            f" | default={default_text}"
        )

    return signature


# ----------------------------------------------------------------------
# Class structure
# ----------------------------------------------------------------------

def inspect_class_structure(
    cls: type,
) -> None:

    print()
    print("Class structure:")

    is_dataclass = dataclasses.is_dataclass(
        cls
    )

    print(
        f"  dataclass : {is_dataclass}"
    )

    if not is_dataclass:
        fail(
            "Expected AcquisitionManifest "
            "to be a dataclass."
        )

    print()
    print("Dataclass fields:")

    for field in dataclasses.fields(cls):

        print(
            f"  {field.name}"
            f" | type={field.type!r}"
            f" | default={field.default!r}"
            f" | factory={field.default_factory!r}"
        )

    print()
    print("Class annotations:")

    annotations = getattr(
        cls,
        "__annotations__",
        {},
    )

    for name, annotation in annotations.items():
        print(
            f"  {name}: {annotation!r}"
        )


# ----------------------------------------------------------------------
# Verify expected local constructor contract
# ----------------------------------------------------------------------

def verify_required_contract(
    signature: inspect.Signature,
) -> None:

    parameters = signature.parameters

    required_names = {
        name
        for name, parameter
        in parameters.items()
        if (
            parameter.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            )
            and parameter.default
            is inspect.Parameter.empty
        )
    }

    expected_required = {
        "manifest_id",
        "source",
    }

    print()
    print(
        "Required constructor contract:"
    )

    print(
        f"  actual required = "
        f"{sorted(required_names)}"
    )

    print(
        f"  expected required = "
        f"{sorted(expected_required)}"
    )

    if required_names != expected_required:

        fail(
            "Unexpected required AcquisitionManifest "
            "constructor contract.\n"
            f"Actual   : {sorted(required_names)}\n"
            f"Expected : {sorted(expected_required)}"
        )

    print(
        "  manifest_id : REQUIRED : PASS"
    )

    print(
        "  source      : REQUIRED : PASS"
    )


# ----------------------------------------------------------------------
# Construct actual Amarakośa CorpusSource
# ----------------------------------------------------------------------

def create_amarakosha_source() -> Any:

    from SanskritAI.acquisition.sources.amarakosha import (
        create_amarakosha_source as factory,
    )

    source = factory()

    print()
    print(
        "Amarakośa CorpusSource construction : PASS"
    )

    if source.source_id != AMARAKOSHA_SOURCE_ID:
        fail(
            "Unexpected Amarakośa source_id:\n"
            f"expected={AMARAKOSHA_SOURCE_ID!r}\n"
            f"actual={source.source_id!r}"
        )

    if source.name != AMARAKOSHA_NAME:
        fail(
            "Unexpected Amarakośa source name:\n"
            f"expected={AMARAKOSHA_NAME!r}\n"
            f"actual={source.name!r}"
        )

    return source


# ----------------------------------------------------------------------
# Construct manifest
# ----------------------------------------------------------------------

def construct_manifest(
    ManifestClass: type,
    signature: inspect.Signature,
    source: Any,
) -> Any:

    parameters = signature.parameters

    # --------------------------------------------------------------
    # Values are based ONLY on the actual local constructor.
    # --------------------------------------------------------------

    values: dict[str, Any] = {}

    # REQUIRED
    values["manifest_id"] = (
        AMARAKOSHA_MANIFEST_ID
    )

    values["source"] = source

    # Acquisition URLs
    if "urls" in parameters:
        values["urls"] = []

    if "mirrors" in parameters:
        values["mirrors"] = []

    # Format
    if "preferred_format" in parameters:

        from SanskritAI.acquisition.models.source_format import (
            SourceFormat,
        )

        values["preferred_format"] = (
            SourceFormat.TXT
        )

    # Expected artifact
    if "expected_filename" in parameters:
        values["expected_filename"] = (
            AMARAKOSHA_ARTIFACT.name
        )

    if "expected_size" in parameters:
        values["expected_size"] = (
            AMARAKOSHA_ARTIFACT.stat().st_size
        )

    if "checksum" in parameters:
        values["checksum"] = (
            AMARAKOSHA_SHA256
        )

    if "checksum_algorithm" in parameters:
        values["checksum_algorithm"] = (
            "sha256"
        )

    # Storage
    if "destination_directory" in parameters:
        values["destination_directory"] = (
            AMARAKOSHA_ARTIFACT.parent
        )

    if "cache_directory" in parameters:
        values["cache_directory"] = None

    if "overwrite_existing" in parameters:
        values["overwrite_existing"] = False

    if "extract_archives" in parameters:
        values["extract_archives"] = False

    # Processing
    if "importer" in parameters:
        values["importer"] = (
            "amarakosha"
        )

    if "encoding" in parameters:
        values["encoding"] = "utf-8"

    if "normalize_unicode" in parameters:
        values["normalize_unicode"] = True

    if "validate_checksum" in parameters:
        values["validate_checksum"] = True

    if "validate_license" in parameters:
        values["validate_license"] = True

    # Priority / activation
    if "priority" in parameters:
        values["priority"] = 100

    if "enabled" in parameters:
        values["enabled"] = True

    # Metadata
    if "metadata" in parameters:
        values["metadata"] = {
            "filename": (
                AMARAKOSHA_ARTIFACT.name
            ),
            "encoding": "utf-8",
            "size_bytes": (
                AMARAKOSHA_ARTIFACT.stat().st_size
            ),
            "sha256": AMARAKOSHA_SHA256,
            "provenance_url": (
                AMARAKOSHA_PROVENANCE_URL
            ),
            "artifact_provenance": (
                "Embedded metadata in verified "
                "amarakosha.txt artifact."
            ),
        }

    print()
    print(
        "Constructor values selected:"
    )

    for name, value in values.items():
        print(
            f"  {name} = {value!r}"
        )

    # --------------------------------------------------------------
    # Ensure every supplied parameter actually exists.
    # --------------------------------------------------------------

    unknown = set(values) - set(
        parameters
    )

    if unknown:
        fail(
            "Audit attempted to pass constructor "
            "parameters that do not exist:\n"
            f"  {sorted(unknown)}"
        )

    # --------------------------------------------------------------
    # Construct.
    # --------------------------------------------------------------

    try:
        manifest = ManifestClass(
            **values
        )
    except Exception as exc:
        fail(
            "Actual local AcquisitionManifest "
            "constructor failed:\n"
            f"  {type(exc).__name__}: {exc}"
        )

    print()
    print(
        "AcquisitionManifest construction : PASS"
    )

    return manifest


# ----------------------------------------------------------------------
# Print manifest
# ----------------------------------------------------------------------

def print_manifest(
    manifest: Any,
) -> None:

    print()
    print(
        "Constructed AcquisitionManifest:"
    )
    print()

    print(
        f"  type = "
        f"{type(manifest).__module__}."
        f"{type(manifest).__name__}"
    )

    if dataclasses.is_dataclass(manifest):

        for field in dataclasses.fields(
            manifest
        ):

            value = getattr(
                manifest,
                field.name,
            )

            print(
                f"  {field.name} = {value!r}"
            )

    else:

        values = vars(manifest)

        for name, value in values.items():

            print(
                f"  {name} = {value!r}"
            )


# ----------------------------------------------------------------------
# Semantic validation
# ----------------------------------------------------------------------

def validate_manifest(
    manifest: Any,
    source: Any,
) -> None:

    print()
    print(
        "13R-7 Amarakośa manifest semantic validation:"
    )

    # Identity
    assert (
        manifest.manifest_id
        == AMARAKOSHA_MANIFEST_ID
    )

    print(
        "  manifest_id = "
        f"{manifest.manifest_id!r} : PASS"
    )

    # Source
    assert manifest.source is source

    assert (
        manifest.source.source_id
        == AMARAKOSHA_SOURCE_ID
    )

    print(
        "  source.source_id = "
        f"{manifest.source.source_id!r} : PASS"
    )

    # URLs
    assert manifest.urls == []

    print(
        "  urls = [] : PASS"
    )

    assert manifest.mirrors == []

    print(
        "  mirrors = [] : PASS"
    )

    # Preferred format
    from SanskritAI.acquisition.models.source_format import (
        SourceFormat,
    )

    assert (
        manifest.preferred_format
        == SourceFormat.TXT
    )

    print(
        "  preferred_format = "
        f"{manifest.preferred_format!s} : PASS"
    )

    # Expected filename
    assert (
        manifest.expected_filename
        == "amarakosha.txt"
    )

    print(
        "  expected_filename = "
        f"{manifest.expected_filename!r} : PASS"
    )

    # Expected size
    expected_size = (
        AMARAKOSHA_ARTIFACT.stat().st_size
    )

    assert (
        manifest.expected_size
        == expected_size
    )

    print(
        "  expected_size = "
        f"{manifest.expected_size} : PASS"
    )

    # Checksum
    assert (
        manifest.checksum
        == AMARAKOSHA_SHA256
    )

    print(
        "  checksum = "
        f"{manifest.checksum} : PASS"
    )

    assert (
        manifest.checksum_algorithm
        == "sha256"
    )

    print(
        "  checksum_algorithm = "
        f"{manifest.checksum_algorithm!r} : PASS"
    )

    # Destination
    assert (
        manifest.destination_directory
        == AMARAKOSHA_ARTIFACT.parent
    )

    print(
        "  destination_directory = "
        f"{manifest.destination_directory} : PASS"
    )

    # Local artifact already exists.
    assert (
        AMARAKOSHA_ARTIFACT.exists()
    )

    assert (
        AMARAKOSHA_ARTIFACT.is_file()
    )

    print(
        "  verified local artifact exists : PASS"
    )

    # Acquisition semantics
    assert (
        manifest.requires_download
        is False
    )

    print(
        "  requires_download = False : PASS"
    )

    assert (
        manifest.has_urls
        is False
    )

    print(
        "  has_urls = False : PASS"
    )

    # Checksum validation semantics
    assert (
        manifest.requires_checksum_validation
        is True
    )

    print(
        "  requires_checksum_validation = True : PASS"
    )

    # Importer
    assert (
        manifest.importer
        == "amarakosha"
    )

    print(
        "  importer = "
        f"{manifest.importer!r} : PASS"
    )

    # Encoding
    assert (
        manifest.encoding
        == "utf-8"
    )

    print(
        "  encoding = "
        f"{manifest.encoding!r} : PASS"
    )

    # Extraction
    assert (
        manifest.extract_archives
        is False
    )

    print(
        "  extract_archives = False : PASS"
    )

    # Enabled
    assert (
        manifest.enabled
        is True
    )

    print(
        "  enabled = True : PASS"
    )

    # Metadata
    metadata = manifest.metadata

    assert (
        metadata.get("filename")
        == "amarakosha.txt"
    )

    assert (
        metadata.get("encoding")
        == "utf-8"
    )

    assert (
        metadata.get("size_bytes")
        == expected_size
    )

    assert (
        metadata.get("sha256")
        == AMARAKOSHA_SHA256
    )

    assert (
        metadata.get("provenance_url")
        == AMARAKOSHA_PROVENANCE_URL
    )

    print(
        "  metadata filename : PASS"
    )

    print(
        "  metadata encoding : PASS"
    )

    print(
        "  metadata size     : PASS"
    )

    print(
        "  metadata sha256   : PASS"
    )

    print(
        "  metadata provenance_url : PASS"
    )


# ----------------------------------------------------------------------
# Serialization validation
# ----------------------------------------------------------------------

def validate_serialization(
    manifest: Any,
) -> None:

    print()
    print(
        "Manifest serialization validation:"
    )

    data = manifest.to_dict()

    if not isinstance(
        data,
        dict,
    ):
        fail(
            "AcquisitionManifest.to_dict() "
            "did not return dict."
        )

    print(
        "  to_dict() returns dict : PASS"
    )

    assert (
        data["manifest_id"]
        == AMARAKOSHA_MANIFEST_ID
    )

    assert (
        data["source_id"]
        == AMARAKOSHA_SOURCE_ID
    )

    assert (
        data["expected_filename"]
        == "amarakosha.txt"
    )

    assert (
        data["checksum"]
        == AMARAKOSHA_SHA256
    )

    assert (
        data["preferred_format"]
        == "txt"
    )

    print(
        "  manifest_id : PASS"
    )

    print(
        "  source_id : PASS"
    )

    print(
        "  expected_filename : PASS"
    )

    print(
        "  checksum : PASS"
    )

    print(
        "  preferred_format : PASS"
    )


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> None:

    print("=" * 72)
    print(
        "13R-7 — Amarakośa AcquisitionManifest "
        "actual-local-contract audit"
    )
    print("=" * 72)

    # --------------------------------------------------------------
    # Bootstrap
    # --------------------------------------------------------------

    bootstrap()

    print(
        f"Repository root : {REPO_ROOT}"
    )

    # --------------------------------------------------------------
    # Artifact
    # --------------------------------------------------------------

    if not AMARAKOSHA_ARTIFACT.exists():
        fail(
            "Verified Amarakośa artifact missing:\n"
            f"  {AMARAKOSHA_ARTIFACT}"
        )

    if not AMARAKOSHA_ARTIFACT.is_file():
        fail(
            "Verified Amarakośa artifact is not a file:\n"
            f"  {AMARAKOSHA_ARTIFACT}"
        )

    print(
        "Verified Amarakośa artifact : PASS"
    )

    print(
        f"  path = {AMARAKOSHA_ARTIFACT}"
    )

    print(
        f"  size = "
        f"{AMARAKOSHA_ARTIFACT.stat().st_size}"
    )

    # --------------------------------------------------------------
    # Locate actual local manifest
    # --------------------------------------------------------------

    module_name, manifest_path = (
        locate_acquisition_manifest_source()
    )

    print()
    print(
        "Actual AcquisitionManifest source:"
    )

    print(
        f"  module = {module_name}"
    )

    print(
        f"  file   = {manifest_path}"
    )

    # --------------------------------------------------------------
    # Import
    # --------------------------------------------------------------

    ManifestClass = (
        import_manifest_class(
            module_name
        )
    )

    print()
    print(
        "AcquisitionManifest import : PASS"
    )

    # --------------------------------------------------------------
    # Inspect
    # --------------------------------------------------------------

    signature = inspect_constructor(
        ManifestClass
    )

    inspect_class_structure(
        ManifestClass
    )

    verify_required_contract(
        signature
    )

    # --------------------------------------------------------------
    # Amarakośa source
    # --------------------------------------------------------------

    source = create_amarakosha_source()

    # --------------------------------------------------------------
    # Manifest
    # --------------------------------------------------------------

    manifest = construct_manifest(
        ManifestClass,
        signature,
        source,
    )

    print_manifest(
        manifest
    )

    # --------------------------------------------------------------
    # Semantic validation
    # --------------------------------------------------------------

    validate_manifest(
        manifest,
        source,
    )

    # --------------------------------------------------------------
    # Serialization
    # --------------------------------------------------------------

    validate_serialization(
        manifest
    )

    # --------------------------------------------------------------
    # Final
    # --------------------------------------------------------------

    print()
    print("=" * 72)
    print(
        "RESULT: PASS — actual local AcquisitionManifest "
        "contract verified and Amarakośa manifest "
        "constructed successfully."
    )
    print("=" * 72)


if __name__ == "__main__":
    main()
