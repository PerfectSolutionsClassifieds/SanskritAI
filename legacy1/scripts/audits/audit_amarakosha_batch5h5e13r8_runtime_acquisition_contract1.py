
from __future__ import annotations

import inspect
import sys
from importlib import import_module
from pathlib import Path


# ============================================================================
# Repository bootstrap
# ============================================================================
# The repository package is:
#
#     /content/SanskritAI/
#
# Therefore Python needs the PARENT directory:
#
#     /content/
#
# on sys.path in order for:
#
#     import SanskritAI
#
# to work correctly.
# ============================================================================

ROOT = Path("/content/SanskritAI")
PARENT = ROOT.parent

if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))


ARTIFACT = ROOT / "amarakosha.txt"

SOURCE_MODULE = "SanskritAI.acquisition.sources.amarakosha"
MANIFEST_MODULE = "SanskritAI.acquisition.sources.amarakosha_manifest"


def section(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def bootstrap_check() -> bool:
    section("Python package bootstrap")

    print(f"Repository root : {ROOT}")
    print(f"Python parent   : {PARENT}")
    print()

    if not ROOT.exists():
        print("Repository root : FAIL")
        return False

    print("Repository root : PASS")

    if not (ROOT / "__init__.py").exists():
        print("SanskritAI package marker : NOT FOUND")
    else:
        print("SanskritAI package marker : PASS")

    try:
        package = import_module("SanskritAI")
    except Exception as exc:
        print(
            "SanskritAI import : FAIL — "
            f"{type(exc).__name__}: {exc}"
        )
        return False

    print(f"SanskritAI import : PASS — {package}")

    print()
    print("sys.path[0:5]:")

    for entry in sys.path[:5]:
        print(f"  {entry}")

    return True


def describe_class(module_name: str, class_name: str) -> object | None:
    print()
    print(f"[{module_name}.{class_name}]")

    try:
        module = import_module(module_name)
    except Exception as exc:
        print(
            f"module import : FAIL — "
            f"{type(exc).__name__}: {exc}"
        )
        return None

    print("module import : PASS")

    cls = getattr(module, class_name, None)

    if cls is None:
        print("class         : NOT FOUND")
        return None

    print(f"class         : {cls}")
    print(f"abstract      : {inspect.isabstract(cls)}")

    try:
        print(f"constructor   : {inspect.signature(cls)}")
    except Exception as exc:
        print(f"constructor   : <unavailable: {exc}>")

    methods = []

    for name, value in inspect.getmembers(cls):
        if name.startswith("_"):
            continue

        if inspect.isfunction(value) or inspect.ismethoddescriptor(value):
            try:
                signature = inspect.signature(value)
            except Exception:
                signature = "<unavailable>"

            methods.append((name, signature))

    if methods:
        print("public methods :")

        for name, signature in methods:
            print(f"  {name}{signature}")
    else:
        print("public methods : NONE")

    return cls


def main() -> int:
    section("13R-8 — Amarakośa runtime acquisition contract audit")

    print(f"Repository root : {ROOT}")
    print(f"TXT artifact    : {ARTIFACT}")

    # ------------------------------------------------------------------------
    # Bootstrap
    # ------------------------------------------------------------------------
    if not bootstrap_check():
        print()
        print(
            "RESULT: FAIL — SanskritAI package bootstrap failed."
        )
        return 1

    # ------------------------------------------------------------------------
    # Artifact
    # ------------------------------------------------------------------------
    section("Canonical Amarakośa artifact")

    if not ARTIFACT.exists():
        print("Amarakośa TXT  : FAIL — artifact missing")
        return 1

    if not ARTIFACT.is_file():
        print("Amarakośa TXT  : FAIL — artifact is not a file")
        return 1

    print("Amarakośa TXT  : PASS")
    print(f"size           : {ARTIFACT.stat().st_size:,} bytes")

    # ------------------------------------------------------------------------
    # Existing Amarakośa source + manifest
    # ------------------------------------------------------------------------
    section("Existing Amarakośa source + manifest")

    try:
        source_module = import_module(SOURCE_MODULE)
        print(f"source module   : PASS — {SOURCE_MODULE}")
    except Exception as exc:
        print(
            "source module   : FAIL — "
            f"{type(exc).__name__}: {exc}"
        )
        return 1

    try:
        manifest_module = import_module(MANIFEST_MODULE)
        print(f"manifest module : PASS — {MANIFEST_MODULE}")
    except Exception as exc:
        print(
            "manifest module : FAIL — "
            f"{type(exc).__name__}: {exc}"
        )
        return 1

    create_source = getattr(
        source_module,
        "create_amarakosha_source",
        None,
    )

    create_manifest = getattr(
        manifest_module,
        "create_amarakosha_manifest",
        None,
    )

    if create_source is None:
        print("create source   : FAIL")
        return 1

    if create_manifest is None:
        print("create manifest : FAIL")
        return 1

    try:
        source = create_source()
    except Exception as exc:
        print(
            "source creation : FAIL — "
            f"{type(exc).__name__}: {exc}"
        )
        return 1

    try:
        manifest = create_manifest()
    except Exception as exc:
        print(
            "manifest        : FAIL — "
            f"{type(exc).__name__}: {exc}"
        )
        return 1

    print("source creation : PASS")
    print("manifest        : PASS")

    print()
    print("Source:")
    print(f"  source_id     = {source.source_id}")
    print(f"  name          = {source.name}")
    print(f"  source_type   = {source.source_type}")
    print(f"  source_format = {source.source_format}")
    print(f"  status        = {source.status}")
    print(f"  local_path    = {source.local_path}")

    print()
    print("Manifest:")
    print(f"  manifest_id   = {manifest.manifest_id}")
    print(f"  urls          = {manifest.urls}")
    print(f"  mirrors       = {manifest.mirrors}")
    print(f"  importer      = {manifest.importer}")
    print(f"  encoding      = {manifest.encoding}")
    print(f"  expected_file = {manifest.expected_filename}")
    print(f"  expected_size = {manifest.expected_size}")
    print(f"  checksum      = {manifest.checksum}")

    # ------------------------------------------------------------------------
    # Existing acquisition runtime classes
    # ------------------------------------------------------------------------
    section("Existing acquisition runtime classes")

    candidates = [
        (
            "SanskritAI.acquisition.acquirers.source_acquirer",
            "SourceAcquirer",
        ),
        (
            "SanskritAI.acquisition.acquirers.default_source_acquirer",
            "DefaultSourceAcquirer",
        ),
        (
            "SanskritAI.acquisition.services.acquisition_service",
            "AcquisitionService",
        ),
        (
            "SanskritAI.acquisition.services.acquisition_service",
            "DefaultAcquisitionService",
        ),
        (
            "SanskritAI.acquisition.managers.acquisition_manager",
            "AcquisitionManager",
        ),
        (
            "SanskritAI.acquisition.downloaders.base_downloader",
            "BaseDownloader",
        ),
        (
            "SanskritAI.acquisition.downloaders.http_downloader",
            "HTTPDownloader",
        ),
        (
            "SanskritAI.acquisition.importers.local_file_importer",
            "LocalFileImporter",
        ),
    ]

    discovered = {}

    for module_name, class_name in candidates:
        discovered[class_name] = describe_class(
            module_name,
            class_name,
        )

    # ------------------------------------------------------------------------
    # Package-level exports
    # ------------------------------------------------------------------------
    section("Acquisition package exports")

    export_checks = [
        (
            "SanskritAI.acquisition",
            [
                "SourceAcquirer",
                "DefaultSourceAcquirer",
                "AcquisitionService",
                "DefaultAcquisitionService",
                "AcquisitionManager",
                "HTTPDownloader",
                "LocalFileImporter",
            ],
        ),
    ]

    for module_name, names in export_checks:

        try:
            module = import_module(module_name)
            print(f"module import : PASS — {module_name}")
        except Exception as exc:
            print(
                f"module import : FAIL — "
                f"{type(exc).__name__}: {exc}"
            )
            continue

        for name in names:
            value = getattr(module, name, None)
            print(
                f"  {name:<28} = "
                f"{'PASS' if value is not None else 'NOT EXPORTED'}"
            )

    # ------------------------------------------------------------------------
    # Manifest runtime semantics
    # ------------------------------------------------------------------------
    section("Manifest runtime semantics")

    checks = {
        "source identity":
            manifest.source.source_id == "amarakosha",

        "local acquisition":
            manifest.requires_download is False,

        "TXT format":
            str(manifest.preferred_format).lower().endswith("txt"),

        "expected filename":
            manifest.expected_filename == "amarakosha.txt",

        "expected size":
            manifest.expected_size == ARTIFACT.stat().st_size,

        "checksum":
            manifest.checksum is not None,

        "checksum validation":
            manifest.requires_checksum_validation is True,

        "local destination":
            manifest.destination_directory == ROOT,

        "importer":
            manifest.importer == "amarakosha",

        "UTF-8":
            manifest.encoding == "utf-8",

        "normalization":
            manifest.normalize_unicode is True,
    }

    all_passed = True

    for label, result in checks.items():
        status = "PASS" if result else "FAIL"
        print(f"{label:<24}: {status}")

        if not result:
            all_passed = False

    if not all_passed:
        print()
        print(
            "RESULT: FAIL — manifest/runtime contract mismatch"
        )
        return 1

    # ------------------------------------------------------------------------
    # Architectural decision
    # ------------------------------------------------------------------------
    section("13R-8 architectural decision")

    print("Existing acquisition runtime inspected : PASS")
    print()
    print("No Amarakośa-specific acquisition class")
    print("should be created yet.")
    print()
    print("Required next step:")
    print("  determine the existing runtime entry point")
    print("  that consumes an AcquisitionManifest and/or")
    print("  CorpusSource for LOCAL artifacts.")
    print()
    print("PDF acquisition is NOT part of this runtime path.")
    print()
    print("The verified canonical input remains:")
    print(f"  {ARTIFACT}")
    print()
    print(
        "RESULT: PASS — runtime contracts inventoried;"
    )
    print(
        "        implementation boundary not yet modified."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
