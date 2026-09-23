
from __future__ import annotations

"""
SanskritAI
==========

13R-7 — Amarakośa AcquisitionManifest Contract Audit
------------------------------------------------------

Read-only audit of the ACTUAL LOCAL AcquisitionManifest contract.

This audit intentionally does NOT copy the public GitHub
Monier-Williams manifest implementation.

It discovers the local AcquisitionManifest implementation,
inspects its constructor and fields, and then constructs a
real Amarakośa manifest using the actual local contract.

Production files are NOT modified.

Scope:

    13R-6 CorpusSource
        ↓
    13R-7 AcquisitionManifest
        ↓
    13R-8 Runtime acquisition
        ↓
    13R-9 Existing Amarakośa parser/importer
        ↓
    13R-10 Canonical lexical bridge

This audit is intentionally limited to 13R-7.
"""

# from __future__ import annotations

import ast
import dataclasses
import inspect
import importlib
import pkgutil
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path("/content/SanskritAI")

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


def fail(message: str) -> None:
    raise RuntimeError(message)


def bootstrap() -> None:
    if not REPO_ROOT.exists():
        fail(f"Repository root not found: {REPO_ROOT}")

    parent = REPO_ROOT.parent

    if str(parent) not in sys.path:
        sys.path.insert(0, str(parent))


def locate_acquisition_manifest_source() -> tuple[str, Path]:
    """
    Locate the production Python file containing the actual
    AcquisitionManifest class.

    Historical/duplicate audit scripts are deliberately ignored.
    """

    acquisition_root = REPO_ROOT / "acquisition"

    if not acquisition_root.exists():
        fail(
            f"Acquisition package not found: {acquisition_root}"
        )

    candidates: list[tuple[str, Path]] = []

    for path in acquisition_root.rglob("*.py"):
        name = path.name

        # Ignore Python cache.
        if "__pycache__" in path.parts:
            continue

        # Ignore obvious historical/duplicate files.
        stem = path.stem

        if stem.endswith(tuple(str(i) for i in range(10))):
            continue

        if "_G" in stem:
            tail = stem.split("_G", 1)[-1]
            if tail.isdigit():
                continue

        if (
            "audit_" in stem
            or stem.startswith("repair_")
        ):
            continue

        try:
            source = path.read_text(
                encoding="utf-8"
            )
        except Exception:
            continue

        if "class AcquisitionManifest" not in source:
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

        relative = path.relative_to(REPO_ROOT)
        module_parts = list(relative.with_suffix("").parts)

        module_name = (
            "SanskritAI."
            + ".".join(module_parts)
        )

        candidates.append(
            (module_name, path)
        )

    if not candidates:
        fail(
            "No production AcquisitionManifest class "
            "was found under acquisition/."
        )

    if len(candidates) > 1:
        print()
        print(
            "WARNING: multiple AcquisitionManifest "
            "definitions were found:"
        )

        for module_name, path in candidates:
            print(
                f"  {module_name} -> {path}"
            )

        # Prefer the shortest path as the likely canonical
        # production implementation, but report all candidates.
        candidates.sort(
            key=lambda item: (
                len(item[1].parts),
                str(item[1]),
            )
        )

    return candidates[0]


def import_manifest_class(
    module_name: str,
) -> type:
    module = importlib.import_module(module_name)

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


def print_signature(cls: type) -> inspect.Signature:
    signature = inspect.signature(cls)

    print()
    print("Actual local AcquisitionManifest constructor:")
    print()
    print(f"  {cls.__module__}.AcquisitionManifest")
    print(f"  signature = {signature}")

    print()
    print("Constructor parameters:")

    for name, parameter in signature.parameters.items():
        annotation = parameter.annotation

        if annotation is inspect.Parameter.empty:
            annotation_text = "<empty>"
        else:
            annotation_text = repr(annotation)

        if parameter.default is inspect.Parameter.empty:
            default_text = "<required>"
        else:
            default_text = repr(parameter.default)

        print(
            f"  {name}"
            f" | kind={parameter.kind}"
            f" | annotation={annotation_text}"
            f" | default={default_text}"
        )

    return signature


def print_class_structure(cls: type) -> None:
    print()
    print("Class structure:")

    print(
        f"  dataclass : {dataclasses.is_dataclass(cls)}"
    )

    if dataclasses.is_dataclass(cls):
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

    if annotations:
        for name, annotation in annotations.items():
            print(
                f"  {name}: {annotation!r}"
            )
    else:
        print("  <none>")


def discover_parameter_names(
    signature: inspect.Signature,
) -> set[str]:
    return set(signature.parameters.keys())


def construct_actual_manifest(
    cls: type,
    signature: inspect.Signature,
) -> Any:
    """
    Construct an Amarakośa AcquisitionManifest using only
    parameter names that actually exist in the local constructor.

    This is deliberately explicit and conservative.

    If the constructor uses an unexpected semantic contract,
    the audit FAILS rather than guessing.
    """

    parameter_names = discover_parameter_names(
        signature
    )

    print()
    print(
        "Building Amarakośa manifest from actual "
        "constructor parameters..."
    )

    # Candidate semantic values.
    source_object = None

    try:
        from SanskritAI.acquisition.sources.amarakosha import (
            create_amarakosha_source,
        )

        source_object = create_amarakosha_source()

        print(
            "  Amarakośa CorpusSource : PASS"
        )

    except Exception as exc:
        fail(
            "Could not construct Amarakośa CorpusSource "
            f"before manifest construction: {exc}"
        )

    values: dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Known semantic parameter mappings.
    #
    # We only use a value if the actual constructor exposes that
    # parameter name.
    # ------------------------------------------------------------------

    mappings: dict[str, Any] = {
        "source": source_object,
        "corpus_source": source_object,

        "destination": AMARAKOSHA_ARTIFACT,
        "destination_path": AMARAKOSHA_ARTIFACT,
        "local_path": AMARAKOSHA_ARTIFACT,
        "file_path": AMARAKOSHA_ARTIFACT,

        "source_id": AMARAKOSHA_SOURCE_ID,
        "identifier": AMARAKOSHA_SOURCE_ID,

        "name": AMARAKOSHA_NAME,
        "title": AMARAKOSHA_NAME,

        "urls": [],
        "download_urls": [],
        "url": None,
        "download_url": None,

        "expected_filename": (
            AMARAKOSHA_ARTIFACT.name
        ),

        "encoding": "utf-8",

        "format": "txt",
        "source_format": None,

        "importer": "amarakosha",

        "enabled": True,
        "requires_download": False,

        "overwrite_existing": False,

        "checksum": AMARAKOSHA_SHA256,
        "sha256": AMARAKOSHA_SHA256,

        "metadata": {
            "filename": AMARAKOSHA_ARTIFACT.name,
            "encoding": "utf-8",
            "size_bytes": (
                AMARAKOSHA_ARTIFACT.stat().st_size
            ),
            "sha256": AMARAKOSHA_SHA256,
            "provenance_url": (
                AMARAKOSHA_PROVENANCE_URL
            ),
        },
    }

    # Do not silently guess unknown required parameters.
    for name, parameter in signature.parameters.items():

        if name == "self":
            continue

        if parameter.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            continue

        if name in mappings:
            value = mappings[name]

            # Do not pass None to an enum/source-format field.
            if (
                name == "source_format"
                and value is None
            ):
                continue

            values[name] = value
            continue

        if parameter.default is not inspect.Parameter.empty:
            # Optional parameter; let constructor use its default.
            continue

        fail(
            "AcquisitionManifest has an unsupported "
            "required constructor parameter:\n"
            f"  {name}\n\n"
            "The audit intentionally refuses to guess "
            "its meaning. The local constructor must be "
            "reviewed before 13R-7 production code is written."
        )

    print()
    print("Constructor values selected:")

    for name, value in values.items():
        print(
            f"  {name} = {value!r}"
        )

    try:
        manifest = cls(**values)
    except Exception as exc:
        fail(
            "Actual local AcquisitionManifest constructor "
            "rejected the audit values:\n"
            f"  {type(exc).__name__}: {exc}"
        )

    return manifest


def print_manifest(manifest: Any) -> None:
    print()
    print("Constructed AcquisitionManifest:")
    print()
    print(
        f"  type = "
        f"{type(manifest).__module__}."
        f"{type(manifest).__name__}"
    )

    if dataclasses.is_dataclass(manifest):
        for field in dataclasses.fields(manifest):
            value = getattr(
                manifest,
                field.name,
            )

            print(
                f"  {field.name} = {value!r}"
            )

    else:
        try:
            values = vars(manifest)

            for name, value in values.items():
                print(
                    f"  {name} = {value!r}"
                )

        except TypeError:
            print(
                "  <object has no __dict__>"
            )


def validate_manifest_semantics(
    manifest: Any,
) -> None:
    """
    Validate only values that the actual object exposes.

    No assumptions are made about fields that do not exist.
    """

    print()
    print("Manifest semantic validation:")

    checks: list[tuple[str, Any]] = []

    for attribute, expected in (
        (
            "source",
            None,
        ),
        (
            "destination",
            AMARAKOSHA_ARTIFACT,
        ),
        (
            "destination_path",
            AMARAKOSHA_ARTIFACT,
        ),
        (
            "local_path",
            AMARAKOSHA_ARTIFACT,
        ),
        (
            "file_path",
            AMARAKOSHA_ARTIFACT,
        ),
        (
            "source_id",
            AMARAKOSHA_SOURCE_ID,
        ),
        (
            "identifier",
            AMARAKOSHA_SOURCE_ID,
        ),
        (
            "name",
            AMARAKOSHA_NAME,
        ),
        (
            "title",
            AMARAKOSHA_NAME,
        ),
        (
            "expected_filename",
            AMARAKOSHA_ARTIFACT.name,
        ),
        (
            "encoding",
            "utf-8",
        ),
        (
            "importer",
            "amarakosha",
        ),
        (
            "enabled",
            True,
        ),
        (
            "requires_download",
            False,
        ),
        (
            "overwrite_existing",
            False,
        ),
    ):
        if not hasattr(
            manifest,
            attribute,
        ):
            continue

        actual = getattr(
            manifest,
            attribute,
        )

        if attribute == "source":
            if actual is None:
                fail(
                    "Manifest exposes 'source' but it is None."
                )

            checks.append(
                (
                    attribute,
                    "Amarakośa source object",
                )
            )

            continue

        if isinstance(
            expected,
            Path,
        ):
            try:
                actual_path = Path(actual)
            except TypeError:
                fail(
                    f"Manifest field {attribute!r} "
                    "is not path-compatible."
                )

            if actual_path != expected:
                fail(
                    f"Manifest field {attribute!r} mismatch:\n"
                    f"  expected={expected}\n"
                    f"  actual={actual}"
                )

        else:
            if actual != expected:
                fail(
                    f"Manifest field {attribute!r} mismatch:\n"
                    f"  expected={expected!r}\n"
                    f"  actual={actual!r}"
                )

        checks.append(
            (
                attribute,
                actual,
            )
        )

    for attribute, value in checks:
        print(
            f"  {attribute} = {value!r} : PASS"
        )


def main() -> None:
    print("=" * 72)
    print(
        "13R-7 — Amarakośa AcquisitionManifest "
        "actual-local-contract audit"
    )
    print("=" * 72)

    bootstrap()

    print(
        f"Repository root : {REPO_ROOT}"
    )

    if not AMARAKOSHA_ARTIFACT.exists():
        fail(
            "Verified Amarakośa artifact is missing:\n"
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

    # ------------------------------------------------------------------
    # Locate actual local AcquisitionManifest.
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Import actual local class.
    # ------------------------------------------------------------------

    ManifestClass = import_manifest_class(
        module_name
    )

    print()
    print(
        "AcquisitionManifest import : PASS"
    )

    # ------------------------------------------------------------------
    # Inspect exact constructor.
    # ------------------------------------------------------------------

    signature = print_signature(
        ManifestClass
    )

    print_class_structure(
        ManifestClass
    )

    # ------------------------------------------------------------------
    # Construct using actual constructor.
    # ------------------------------------------------------------------

    manifest = construct_actual_manifest(
        ManifestClass,
        signature,
    )

    print_manifest(
        manifest
    )

    # ------------------------------------------------------------------
    # Validate semantics.
    # ------------------------------------------------------------------

    validate_manifest_semantics(
        manifest
    )

    # ------------------------------------------------------------------
    # Final result.
    # ------------------------------------------------------------------

    print()
    print("=" * 72)
    print(
        "RESULT: PASS — actual local AcquisitionManifest "
        "constructor identified and Amarakośa manifest "
        "constructed successfully."
    )
    print("=" * 72)


if __name__ == "__main__":
    main()
