
from __future__ import annotations

import inspect
import sys
from importlib import import_module
from pathlib import Path


# ============================================================================
# Repository bootstrap
# ============================================================================

ROOT = Path("/content/SanskritAI")
PARENT = ROOT.parent

if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))


ARTIFACT = ROOT / "amarakosha.txt"

SOURCE_MODULE = "SanskritAI.acquisition.sources.amarakosha"

# IMPORTANT:
# This is the expected Amarakośa-specific production manifest module.
#
# Do NOT confuse it with:
#
# SanskritAI.acquisition.models.acquisition_manifest
#
# The latter is only the generic AcquisitionManifest model.
MANIFEST_MODULE = "SanskritAI.acquisition.sources.amarakosha_manifest"

GENERIC_MANIFEST_MODULE = (
    "SanskritAI.acquisition.models.acquisition_manifest"
)


def section(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def import_module_checked(module_name: str):
    try:
        module = import_module(module_name)
    except Exception as exc:
        print(
            f"module import : FAIL — "
            f"{type(exc).__name__}: {exc}"
        )
        return None

    print(f"module import : PASS — {module_name}")
    return module


def describe_public_members(module, title: str) -> None:
    print()
    print(title)

    members = []

    for name, value in inspect.getmembers(module):
        if name.startswith("_"):
            continue

        if (
            inspect.isfunction(value)
            or inspect.isclass(value)
        ):
            members.append((name, value))

    if not members:
        print("  NONE")
        return

    for name, value in members:
        if inspect.isclass(value):
            kind = "class"
        else:
            kind = "function"

        try:
            signature = inspect.signature(value)
        except Exception:
            signature = "<unavailable>"

        print(f"  {kind:<8} {name}{signature}")


def find_manifest_factory(module):
    candidates = (
        "create_amarakosha_manifest",
        "get_amarakosha_manifest",
        "create_manifest",
        "get_manifest",
    )

    for name in candidates:
        value = getattr(module, name, None)

        if callable(value):
            return name, value

    return None, None


def bootstrap_check() -> bool:
    section("Python package bootstrap")

    print(f"Repository root : {ROOT}")
    print(f"Python parent   : {PARENT}")

    if not ROOT.exists():
        print()
        print("Repository root : FAIL")
        return False

    print()
    print("Repository root : PASS")

    package_marker = ROOT / "__init__.py"

    if package_marker.exists():
        print("SanskritAI package marker : PASS")
    else:
        print("SanskritAI package marker : NOT FOUND")

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


def describe_runtime_class(
    module_name: str,
    class_name: str,
) -> object | None:

    print()
    print(f"[{module_name}.{class_name}]")

    module = import_module_checked(module_name)

    if module is None:
        return None

    cls = getattr(module, class_name, None)

    if cls is None:
        print("class         : NOT FOUND")
        return None

    print(f"class         : {cls}")
    print(f"abstract      : {inspect.isabstract(cls)}")

    try:
        print(f"constructor   : {inspect.signature(cls)}")
    except Exception:
        print("constructor   : <unavailable>")

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

    section(
        "13R-8 — Amarakośa runtime acquisition contract audit"
    )

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
    # Canonical artifact
    # ------------------------------------------------------------------------

    section("Canonical Amarakośa artifact")

    if not ARTIFACT.exists():
        print("Amarakośa TXT  : FAIL — artifact missing")
        return 1

    if not ARTIFACT.is_file():
        print("Amarakośa TXT  : FAIL — artifact is not a file")
        return 1

    print("Amarakośa TXT  : PASS")
    print(
        f"size           : "
        f"{ARTIFACT.stat().st_size:,} bytes"
    )

    # ------------------------------------------------------------------------
    # Amarakośa source
    # ------------------------------------------------------------------------

    section("Existing Amarakośa source")

    source_module = import_module_checked(SOURCE_MODULE)

    if source_module is None:
        print()
        print(
            "RESULT: FAIL — Amarakośa source module unavailable."
        )
        return 1

    describe_public_members(
        source_module,
        "Amarakośa source public members:",
    )

    create_source = getattr(
        source_module,
        "create_amarakosha_source",
        None,
    )

    get_source = getattr(
        source_module,
        "get_amarakosha_source",
        None,
    )

    if callable(create_source):
        source_factory_name = "create_amarakosha_source"
        source_factory = create_source
    elif callable(get_source):
        source_factory_name = "get_amarakosha_source"
        source_factory = get_source
    else:
        print()
        print(
            "Amarakośa source factory : FAIL"
        )
        print(
            "Expected one of:"
        )
        print(
            "  create_amarakosha_source()"
        )
        print(
            "  get_amarakosha_source()"
        )
        return 1

    try:
        source = source_factory()
    except Exception as exc:
        print(
            f"{source_factory_name} : FAIL — "
            f"{type(exc).__name__}: {exc}"
        )
        return 1

    print()
    print(
        f"{source_factory_name} : PASS"
    )

    print()
    print("Source:")
    print(f"  source_id     = {source.source_id}")
    print(f"  name          = {source.name}")
    print(f"  source_type   = {source.source_type}")
    print(f"  source_format = {source.source_format}")
    print(f"  status        = {source.status}")
    print(f"  local_path    = {source.local_path}")

    # ------------------------------------------------------------------------
    # Generic AcquisitionManifest model
    # ------------------------------------------------------------------------

    section(
        "Generic AcquisitionManifest model"
    )

    generic_manifest_module = import_module_checked(
        GENERIC_MANIFEST_MODULE
    )

    if generic_manifest_module is None:
        print()
        print(
            "RESULT: FAIL — generic AcquisitionManifest "
            "model unavailable."
        )
        return 1

    GenericAcquisitionManifest = getattr(
        generic_manifest_module,
        "AcquisitionManifest",
        None,
    )

    if GenericAcquisitionManifest is None:
        print(
            "AcquisitionManifest class : FAIL"
        )
        return 1

    print(
        "AcquisitionManifest class : PASS"
    )

    try:
        print(
            "constructor              : "
            f"{inspect.signature(GenericAcquisitionManifest)}"
        )
    except Exception:
        print(
            "constructor              : <unavailable>"
        )

    print()
    print(
        "This module is the GENERIC MODEL only."
    )
    print(
        "It is not treated as the Amarakośa production "
        "manifest."
    )

    # ------------------------------------------------------------------------
    # Amarakośa production manifest
    # ------------------------------------------------------------------------

    section(
        "Amarakośa production manifest implementation"
    )

    print(
        f"Expected module : {MANIFEST_MODULE}"
    )

    manifest_module = import_module_checked(
        MANIFEST_MODULE
    )

    if manifest_module is None:

        print()
        print(
            "Amarakośa production manifest : NOT FOUND"
        )
        print()
        print(
            "This is an implementation gap, not a generic "
            "AcquisitionManifest-model failure."
        )
        print()
        print(
            "13R-8 decision:"
        )
        print(
            "  Existing source = PASS"
        )
        print(
            "  Generic manifest model = PASS"
        )
        print(
            "  Amarakośa production manifest = MISSING"
        )
        print()
        print(
            "RESULT: BLOCKED — create the Amarakośa "
            "production manifest before runtime acquisition."
        )
        return 1

    describe_public_members(
        manifest_module,
        "Amarakośa manifest public members:",
    )

    manifest_factory_name, manifest_factory = (
        find_manifest_factory(manifest_module)
    )

    if manifest_factory is None:

        print()
        print(
            "Amarakośa manifest factory : FAIL"
        )
        print(
            "No supported Amarakośa manifest factory "
            "was found."
        )
        print()
        print(
            "Expected one of:"
        )

        for name in (
            "create_amarakosha_manifest",
            "get_amarakosha_manifest",
            "create_manifest",
            "get_manifest",
        ):
            print(f"  {name}()")

        print()
        print(
            "RESULT: BLOCKED — manifest implementation "
            "exists but its construction contract is unclear."
        )
        return 1

    try:
        manifest = manifest_factory()
    except Exception as exc:
        print(
            f"{manifest_factory_name} : FAIL — "
            f"{type(exc).__name__}: {exc}"
        )
        return 1

    print()
    print(
        f"{manifest_factory_name} : PASS"
    )

    # ------------------------------------------------------------------------
    # Manifest contract
    # ------------------------------------------------------------------------

    section("Amarakośa manifest runtime semantics")

    checks = {
        "manifest object":
            manifest is not None,

        "source identity":
            manifest.source.source_id == "amarakosha",

        "manifest identity":
            manifest.manifest_id
            == "amarakosha-local-txt",

        "local acquisition":
            manifest.requires_download is False,

        "TXT format":
            str(manifest.preferred_format).lower().endswith(
                "txt"
            ),

        "expected filename":
            manifest.expected_filename
            == "amarakosha.txt",

        "expected size":
            manifest.expected_size
            == ARTIFACT.stat().st_size,

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

        "checksum algorithm":
            manifest.checksum_algorithm.lower()
            == "sha256",
    }

    all_passed = True

    for label, result in checks.items():

        status = "PASS" if result else "FAIL"

        print(
            f"{label:<24}: {status}"
        )

        if not result:
            all_passed = False

    if not all_passed:

        print()
        print(
            "RESULT: FAIL — Amarakośa manifest "
            "semantic contract mismatch."
        )

        return 1

    # ------------------------------------------------------------------------
    # Acquisition runtime classes
    # ------------------------------------------------------------------------

    section(
        "Existing acquisition runtime classes"
    )

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

    runtime_results = {}

    for module_name, class_name in candidates:

        runtime_results[class_name] = (
            describe_runtime_class(
                module_name,
                class_name,
            )
        )

    # ------------------------------------------------------------------------
    # Package exports
    # ------------------------------------------------------------------------

    section(
        "Acquisition package exports"
    )

    try:
        acquisition_package = import_module(
            "SanskritAI.acquisition"
        )

        print(
            "module import : PASS — "
            "SanskritAI.acquisition"
        )

    except Exception as exc:

        print(
            "module import : FAIL — "
            f"{type(exc).__name__}: {exc}"
        )

        acquisition_package = None

    if acquisition_package is not None:

        export_names = [
            "SourceAcquirer",
            "DefaultSourceAcquirer",
            "AcquisitionService",
            "DefaultAcquisitionService",
            "AcquisitionManager",
            "HTTPDownloader",
            "LocalFileImporter",
        ]

        for name in export_names:

            value = getattr(
                acquisition_package,
                name,
                None,
            )

            print(
                f"  {name:<28} = "
                f"{'PASS' if value is not None else 'NOT EXPORTED'}"
            )

    # ------------------------------------------------------------------------
    # Architectural decision
    # ------------------------------------------------------------------------

    section(
        "13R-8 architectural decision"
    )

    print(
        "Python package bootstrap              : PASS"
    )

    print(
        "Canonical Amarakośa artifact          : PASS"
    )

    print(
        "Amarakośa CorpusSource                : PASS"
    )

    print(
        "Generic AcquisitionManifest model    : PASS"
    )

    print(
        "Amarakośa production manifest         : PASS"
    )

    print()
    print(
        "The next task is NOT to create another "
        "Amarakośa acquisition abstraction."
    )

    print()
    print(
        "Next task:"
    )
    print(
        "  identify the existing runtime entry "
        "point that executes a LOCAL"
    )
    print(
        "  AcquisitionManifest."
    )

    print()
    print(
        "Canonical acquisition input:"
    )
    print(
        f"  {ARTIFACT}"
    )

    print()
    print(
        "PDF collection remains an external "
        "representation/reference source."
    )

    print()
    print(
        "RESULT: PASS — Amarakośa source and "
        "production manifest are ready for "
        "runtime acquisition-contract tracing."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
