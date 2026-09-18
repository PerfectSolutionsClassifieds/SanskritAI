
from __future__ import annotations

"""
BATCH 5H-5E-13R-4R
==================

AMARAKOSHA GENERIC ACQUISITION BOUNDARY AUDIT — REVISED

Purpose
-------
Re-audit the generic acquisition execution chain without assuming
that particular concrete implementations exist.

The previous 13R-4 audit correctly exposed two architectural facts:

1. HttpDownloader is not exported by the current
   acquisition.downloaders.http_downloader module.

2. ProviderRegistry is abstract and therefore cannot be instantiated
   directly.

This revision makes the audit discovery-driven.

Target architecture
-------------------

    CorpusSource
         |
         v
    AcquisitionManifest
         |
         v
    Provider / Request
         |
         v
    SourceAcquirer
         |
         v
    Downloader
         |
         v
    AcquisitionResult


Questions
---------
1. Can AcquisitionManifest represent an Amarakośa acquisition?
2. What downloader abstractions actually exist?
3. Which downloader classes are abstract/concrete?
4. What provider implementations actually import?
5. Is ProviderRegistry abstract or concrete?
6. Are concrete registry implementations present?
7. Can SourceAcquirer consume AcquisitionManifest?
8. Does a concrete SourceAcquirer exist?
9. Does AcquisitionManager import successfully?
10. Do acquisition services import successfully?
11. Which production acquisition modules currently fail to import?
12. Is an Amarakośa-specific acquisition implementation present?
13. Are stale SourceType / SourceStatus references present in
    actual production code?

Important
---------
Audit scripts, repair scripts, tests, __pycache__, and historical
numbered/_G<number>.py files are excluded from production conclusions.

This audit is READ-ONLY.

No production files are modified.
No new classes are created.
No enum members are added.
No source manifests are created.
No network acquisition is performed.
No provider acquire/discover operation is executed.
"""

from pathlib import Path
import importlib
import inspect
import re
import sys
from typing import Any


PROJECT_ROOT = Path("/content/SanskritAI")


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def section(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def fail(message: str) -> None:
    raise RuntimeError(message)


def is_historical_python(path: Path) -> bool:
    """
    Exclude files whose stem ends with a numeric suffix or _G<number>.
    """
    stem = path.stem

    if re.search(r"\d+$", stem):
        return True

    if re.search(r"_G\d+$", stem):
        return True

    return False


def classify_path(path: Path) -> str:
    relative = path.relative_to(PROJECT_ROOT)
    parts = set(relative.parts)

    if "__pycache__" in parts:
        return "cache"

    if "tests" in parts:
        return "test"

    if "scripts" in parts:

        if "audits" in parts:
            return "audit"

        if "repairs" in parts or "repair" in parts:
            return "repair"

        return "script"

    return "production"


def production_files() -> list[Path]:
    result: list[Path] = []

    for path in PROJECT_ROOT.rglob("*.py"):

        if is_historical_python(path):
            continue

        if classify_path(path) != "production":
            continue

        result.append(path)

    return sorted(result)


def print_class(cls: type[Any], label: str) -> None:
    print()
    print(label)
    print(f"Class     : {cls}")
    print(f"Module    : {cls.__module__}")
    print(f"Name      : {cls.__name__}")
    print(f"Abstract  : {inspect.isabstract(cls)}")

    abstract_methods = sorted(
        getattr(cls, "__abstractmethods__", set())
    )

    print(
        "Abstract methods: "
        + (
            ", ".join(abstract_methods)
            if abstract_methods
            else "<none>"
        )
    )

    print()
    print("Constructor:")

    try:
        print(f"  {inspect.signature(cls)}")
    except Exception as exc:
        print(f"  <unavailable: {exc}>")

    print()
    print("Docstring:")

    print(
        inspect.getdoc(cls)
        or "<none>"
    )


def print_public_methods(cls: type[Any]) -> None:
    print()
    print(
        f"Public members of {cls.__name__}:"
    )

    for name, value in inspect.getmembers(cls):

        if name.startswith("_"):
            continue

        if inspect.isfunction(value) or inspect.ismethod(value):

            try:
                signature = inspect.signature(value)
            except Exception:
                signature = "<signature unavailable>"

            print(
                f"  {name}{signature}"
            )

        elif isinstance(value, property):

            print(
                f"  property {name}"
            )


def find_token(
    token: str,
    files: list[Path],
) -> list[tuple[str, int, str]]:

    results: list[tuple[str, int, str]] = []

    for path in files:

        try:
            text = path.read_text(
                encoding="utf-8"
            )

        except Exception:
            continue

        for number, line in enumerate(
            text.splitlines(),
            start=1,
        ):

            if token.lower() in line.lower():

                results.append(
                    (
                        str(
                            path.relative_to(
                                PROJECT_ROOT
                            )
                        ),
                        number,
                        line.strip(),
                    )
                )

    return results


def print_token(
    label: str,
    token: str,
    files: list[Path],
    limit: int = 80,
) -> list[tuple[str, int, str]]:

    results = find_token(
        token,
        files,
    )

    print()
    print(
        f"{label}: {token!r}"
    )

    print(
        f"Matches: {len(results)}"
    )

    for path, number, line in results[:limit]:

        print(
            f"  {path}:{number}: {line}"
        )

    if len(results) > limit:

        print(
            f"  ... "
            f"{len(results) - limit} additional matches"
        )

    return results


def safe_import(
    module_path: str,
) -> tuple[Any | None, Exception | None]:

    try:

        module = importlib.import_module(
            module_path
        )

        return module, None

    except Exception as exc:

        return None, exc


def classes_defined_in_module(
    module: Any,
) -> list[type[Any]]:

    result: list[type[Any]] = []

    for _, value in inspect.getmembers(
        module,
        inspect.isclass,
    ):

        if value.__module__ != module.__name__:
            continue

        result.append(value)

    return sorted(
        result,
        key=lambda cls: cls.__name__,
    )


def print_module_classes(
    module: Any,
) -> list[type[Any]]:

    classes = classes_defined_in_module(
        module
    )

    for cls in classes:

        print()
        print(
            f"  class: {cls.__name__}"
        )

        print(
            f"    abstract : "
            f"{inspect.isabstract(cls)}"
        )

        abstract_methods = sorted(
            getattr(
                cls,
                "__abstractmethods__",
                set(),
            )
        )

        print(
            f"    abstract_methods : "
            f"{abstract_methods}"
        )

    return classes


# ---------------------------------------------------------------------
# Main audit
# ---------------------------------------------------------------------

def main() -> None:

    section(
        "BATCH 5H-5E-13R-4R — "
        "GENERIC ACQUISITION BOUNDARY AUDIT — REVISED"
    )

    if not PROJECT_ROOT.exists():

        fail(
            f"Project root does not exist: "
            f"{PROJECT_ROOT}"
        )

    # -----------------------------------------------------------------
    # 1
    # -----------------------------------------------------------------

    section(
        "1. PACKAGE BOOTSTRAP"
    )

    parent = str(
        PROJECT_ROOT.parent
    )

    if parent not in sys.path:

        sys.path.insert(
            0,
            parent,
        )

    import SanskritAI

    print(
        f"SanskritAI import : PASS "
        f"({SanskritAI.__name__})"
    )

    # -----------------------------------------------------------------
    # 2
    # -----------------------------------------------------------------

    section(
        "2. PRODUCTION FILE CLASSIFICATION"
    )

    production = production_files()

    print(
        f"Production Python files : "
        f"{len(production)}"
    )

    print(
        "Historical numbered/_G<number>.py files : excluded"
    )

    print(
        "Audit scripts : excluded"
    )

    print(
        "Repair scripts : excluded"
    )

    print(
        "Tests : excluded"
    )

    print(
        "__pycache__ : excluded"
    )

    # -----------------------------------------------------------------
    # 3
    # -----------------------------------------------------------------

    section(
        "3. CORE ACQUISITION MODELS"
    )

    from SanskritAI.acquisition.models.corpus_source import (
        CorpusSource,
    )

    from SanskritAI.acquisition.models.acquisition_manifest import (
        AcquisitionManifest,
    )

    from SanskritAI.acquisition.models.acquisition_result import (
        AcquisitionResult,
    )

    from SanskritAI.acquisition.models.source_type import (
        SourceType,
    )

    from SanskritAI.acquisition.models.source_format import (
        SourceFormat,
    )

    from SanskritAI.acquisition.models.source_status import (
        SourceStatus,
    )

    print_class(
        CorpusSource,
        "CorpusSource",
    )

    print_class(
        AcquisitionManifest,
        "AcquisitionManifest",
    )

    print_class(
        AcquisitionResult,
        "AcquisitionResult",
    )

    # -----------------------------------------------------------------
    # 4
    # -----------------------------------------------------------------

    section(
        "4. SOURCETYPE CONTRACT"
    )

    print(
        "SourceType members:"
    )

    for name, member in SourceType.__members__.items():

        print(
            f"  {name} = {member.value!r}"
        )

    print()

    for stale in (
        "LOCAL",
        "REMOTE",
        "GRETIL",
    ):

        print(
            f"SourceType.{stale} exists : "
            f"{hasattr(SourceType, stale)}"
        )

    # -----------------------------------------------------------------
    # 5
    # -----------------------------------------------------------------

    section(
        "5. SOURCE FORMAT CONTRACT"
    )

    print(
        "SourceFormat members:"
    )

    for name, member in SourceFormat.__members__.items():

        print(
            f"  {name} = {member.value!r}"
        )

    # -----------------------------------------------------------------
    # 6
    # -----------------------------------------------------------------

    section(
        "6. SOURCE STATUS CONTRACT"
    )

    print(
        "SourceStatus members:"
    )

    for name, member in SourceStatus.__members__.items():

        print(
            f"  {name} = {member.value!r}"
        )

    print()

    print(
        "SourceStatus.AVAILABLE exists : "
        f"{hasattr(SourceStatus, 'AVAILABLE')}"
    )

    # -----------------------------------------------------------------
    # 7
    # -----------------------------------------------------------------

    section(
        "7. ACQUISITION MANIFEST BEHAVIOUR"
    )

    manifest_annotations = getattr(
        AcquisitionManifest,
        "__annotations__",
        {},
    )

    print(
        "AcquisitionManifest fields:"
    )

    for name in sorted(
        manifest_annotations
    ):

        print(
            f"  {name}"
        )

    print()

    print(
        "Executable manifest behaviour:"
    )

    for name in (
        "all_urls",
        "has_urls",
        "requires_download",
        "requires_checksum_validation",
        "requires_license_validation",
    ):

        value = getattr(
            AcquisitionManifest,
            name,
            None,
        )

        print(
            f"  {name}: "
            f"{'present' if value is not None else 'ABSENT'}"
        )

    # -----------------------------------------------------------------
    # 8
    # -----------------------------------------------------------------

    section(
        "8. GENERIC PROVIDER LAYER"
    )

    from SanskritAI.acquisition.providers.base_provider import (
        BaseProvider,
    )

    from SanskritAI.acquisition.providers.acquisition_request import (
        AcquisitionRequest,
    )

    from SanskritAI.acquisition.providers.acquisition_response import (
        AcquisitionResponse,
    )

    provider_registry_module, provider_registry_error = (
        safe_import(
            "SanskritAI.acquisition.providers.provider_registry"
        )
    )

    print_class(
        BaseProvider,
        "BaseProvider",
    )

    print_class(
        AcquisitionRequest,
        "AcquisitionRequest",
    )

    print_class(
        AcquisitionResponse,
        "AcquisitionResponse",
    )

    if provider_registry_module is None:

        print(
            "ProviderRegistry module import : FAIL"
        )

        print(
            f"  {provider_registry_error!r}"
        )

        ProviderRegistry = None

    else:

        print(
            "ProviderRegistry module import : PASS"
        )

        registry_classes = (
            classes_defined_in_module(
                provider_registry_module
            )
        )

        ProviderRegistry = next(
            (
                cls
                for cls in registry_classes
                if cls.__name__ == "ProviderRegistry"
            ),
            None,
        )

        if ProviderRegistry is None:

            print(
                "ProviderRegistry class : ABSENT"
            )

        else:

            print_class(
                ProviderRegistry,
                "ProviderRegistry",
            )

            print_public_methods(
                ProviderRegistry
            )

    # -----------------------------------------------------------------
    # 9
    # -----------------------------------------------------------------

    section(
        "9. EXISTING PROVIDER IMPLEMENTATIONS"
    )

    provider_modules = (
        "cologne_provider",
        "github_provider",
        "gretil_provider",
        "internet_archive_provider",
        "muktabodha_provider",
        "sanskritdocuments_provider",
        "sarit_provider",
        "xml_corpus_provider",
    )

    provider_classes: list[type[Any]] = []

    provider_import_failures: dict[
        str,
        Exception,
    ] = {}

    for module_name in provider_modules:

        module_path = (
            "SanskritAI.acquisition.providers."
            + module_name
        )

        module, error = safe_import(
            module_path
        )

        if module is None:

            provider_import_failures[
                module_name
            ] = error

            print(
                f"  {module_name}: "
                f"IMPORT FAIL -> {error!r}"
            )

            continue

        print()
        print(
            f"  {module_name}: IMPORT PASS"
        )

        classes = print_module_classes(
            module
        )

        for cls in classes:

            if cls is BaseProvider:
                continue

            if issubclass(
                cls,
                BaseProvider,
            ):

                provider_classes.append(
                    cls
                )

    # -----------------------------------------------------------------
    # 10
    # -----------------------------------------------------------------

    section(
        "10. PROVIDER REGISTRY — ABSTRACTNESS / IMPLEMENTATION AUDIT"
    )

    if ProviderRegistry is None:

        print(
            "ProviderRegistry : UNAVAILABLE"
        )

    else:

        print(
            "ProviderRegistry abstract : "
            f"{inspect.isabstract(ProviderRegistry)}"
        )

        print(
            "ProviderRegistry abstract methods : "
            f"{sorted(getattr(ProviderRegistry, '__abstractmethods__', set()))}"
        )

        if inspect.isabstract(
            ProviderRegistry
        ):

            print(
                "Direct construction : SKIPPED"
            )

            print(
                "Reason : ProviderRegistry is abstract."
            )

        else:

            try:

                registry = ProviderRegistry()

                print(
                    "ProviderRegistry construction : PASS"
                )

                print(
                    f"Registry repr : {registry!r}"
                )

            except Exception as exc:

                print(
                    "ProviderRegistry construction : FAIL"
                )

                print(
                    f"  {exc!r}"
                )

    # -----------------------------------------------------------------
    # 11
    # -----------------------------------------------------------------

    section(
        "11. SOURCE ACQUIRER LAYER"
    )

    source_acquirer_module, source_acquirer_error = (
        safe_import(
            "SanskritAI.acquisition.acquirers.source_acquirer"
        )
    )

    default_source_acquirer_module, default_source_acquirer_error = (
        safe_import(
            "SanskritAI.acquisition.acquirers.default_source_acquirer"
        )
    )

    if source_acquirer_module is None:

        print(
            "SourceAcquirer module : IMPORT FAIL"
        )

        print(
            f"  {source_acquirer_error!r}"
        )

        SourceAcquirer = None

    else:

        SourceAcquirer = getattr(
            source_acquirer_module,
            "SourceAcquirer",
            None,
        )

        print(
            "SourceAcquirer module : IMPORT PASS"
        )

        if SourceAcquirer is not None:

            print_class(
                SourceAcquirer,
                "SourceAcquirer",
            )

            print_public_methods(
                SourceAcquirer
            )

    if default_source_acquirer_module is None:

        print(
            "DefaultSourceAcquirer module : "
            "IMPORT FAIL"
        )

        print(
            f"  {default_source_acquirer_error!r}"
        )

        DefaultSourceAcquirer = None

    else:

        DefaultSourceAcquirer = getattr(
            default_source_acquirer_module,
            "DefaultSourceAcquirer",
            None,
        )

        print(
            "DefaultSourceAcquirer module : "
            "IMPORT PASS"
        )

        if DefaultSourceAcquirer is not None:

            print_class(
                DefaultSourceAcquirer,
                "DefaultSourceAcquirer",
            )

            print_public_methods(
                DefaultSourceAcquirer
            )

    # -----------------------------------------------------------------
    # 12
    # -----------------------------------------------------------------

    section(
        "12. DOWNLOADER LAYER — DISCOVERY DRIVEN"
    )

    downloader_modules = (
        "base_downloader",
        "http_downloader",
        "local_file_importer",
    )

    downloader_classes: list[type[Any]] = []

    downloader_import_failures: dict[
        str,
        Exception,
    ] = {}

    for module_name in downloader_modules:

        module_path = (
            "SanskritAI.acquisition.downloaders."
            + module_name
        )

        module, error = safe_import(
            module_path
        )

        if module is None:

            downloader_import_failures[
                module_name
            ] = error

            print()
            print(
                f"{module_name}: "
                f"IMPORT FAIL -> {error!r}"
            )

            continue

        print()
        print(
            f"{module_name}: IMPORT PASS"
        )

        classes = print_module_classes(
            module
        )

        for cls in classes:

            downloader_classes.append(
                cls
            )

    # -----------------------------------------------------------------
    # 13
    # -----------------------------------------------------------------

    section(
        "13. CONCRETE DOWNLOADER SUMMARY"
    )

    if not downloader_classes:

        print(
            "No downloader classes discovered."
        )

    else:

        for cls in downloader_classes:

            print(
                f"  {cls.__module__}.{cls.__name__}"
            )

            print(
                f"    abstract : "
                f"{inspect.isabstract(cls)}"
            )

            if not inspect.isabstract(cls):

                try:

                    print(
                        f"    constructor : "
                        f"{inspect.signature(cls)}"
                    )

                except Exception:

                    print(
                        "    constructor : "
                        "<signature unavailable>"
                    )

    # -----------------------------------------------------------------
    # 14
    # -----------------------------------------------------------------

    section(
        "14. ACQUISITION MANAGER"
    )

    acquisition_manager_module, acquisition_manager_error = (
        safe_import(
            "SanskritAI.acquisition.acquisition_manager"
        )
    )

    if acquisition_manager_module is None:

        print(
            "AcquisitionManager module : "
            "IMPORT FAIL"
        )

        print(
            f"  {acquisition_manager_error!r}"
        )

        AcquisitionManager = None

    else:

        print(
            "AcquisitionManager module : "
            "IMPORT PASS"
        )

        manager_classes = (
            classes_defined_in_module(
                acquisition_manager_module
            )
        )

        for cls in manager_classes:

            print_class(
                cls,
                cls.__name__,
            )

            print_public_methods(
                cls
            )

        AcquisitionManager = getattr(
            acquisition_manager_module,
            "AcquisitionManager",
            None,
        )

    # -----------------------------------------------------------------
    # 15
    # -----------------------------------------------------------------

    section(
        "15. ACQUISITION SERVICE"
    )

    acquisition_service_modules = (
        "SanskritAI.acquisition.services.acquisition_service",
        "SanskritAI.acquisition.services.default_acquisition_service",
    )

    acquisition_service_classes: list[type[Any]] = []

    acquisition_service_failures: dict[
        str,
        Exception,
    ] = {}

    for module_path in acquisition_service_modules:

        module, error = safe_import(
            module_path
        )

        if module is None:

            acquisition_service_failures[
                module_path
            ] = error

            print()
            print(
                f"{module_path}: "
                f"IMPORT FAIL -> {error!r}"
            )

            continue

        print()
        print(
            f"{module_path}: IMPORT PASS"
        )

        classes = print_module_classes(
            module
        )

        for cls in classes:

            acquisition_service_classes.append(
                cls
            )

            print_public_methods(
                cls
            )

    # -----------------------------------------------------------------
    # 16
    # -----------------------------------------------------------------

    section(
        "16. GENERIC ACQUISITION REFERENCES — PRODUCTION"
    )

    acquisition_tokens = (
        "AcquisitionManifest",
        "SourceAcquirer",
        "DefaultSourceAcquirer",
        "BaseDownloader",
        "HttpDownloader",
        "AcquisitionManager",
        "AcquisitionService",
        "DefaultAcquisitionService",
    )

    for token in acquisition_tokens:

        print_token(
            "Production acquisition reference",
            token,
            production,
        )

    # -----------------------------------------------------------------
    # 17
    # -----------------------------------------------------------------

    section(
        "17. PROVIDER REGISTRY REFERENCES — PRODUCTION"
    )

    for token in (
        "ProviderRegistry",
        "register",
        "get_provider",
        "find_provider",
    ):

        print_token(
            "Production provider-registry reference",
            token,
            production,
        )

    # -----------------------------------------------------------------
    # 18
    # -----------------------------------------------------------------

    section(
        "18. AMARAKOSHA ACQUISITION REFERENCES — PRODUCTION"
    )

    for token in (
        "amarakosha",
        "Amarakosha",
        "AMARAKOSHA",
    ):

        print_token(
            "Production Amarakośa reference",
            token,
            production,
        )

    # -----------------------------------------------------------------
    # 19
    # -----------------------------------------------------------------

    section(
        "19. AMARAKOSHA-SPECIFIC ACQUISITION CLASSES"
    )

    specific_tokens = (
        "AmarakoshaProvider",
        "AmarakoshaAcquirer",
        "AmarakoshaDownloader",
        "AmarakoshaSource",
        "AmarakoshaManifest",
    )

    specific_results: dict[
        str,
        list[tuple[str, int, str]],
    ] = {}

    for token in specific_tokens:

        results = print_token(
            "Production Amarakośa acquisition class",
            token,
            production,
        )

        specific_results[
            token
        ] = results

    # -----------------------------------------------------------------
    # 20
    # -----------------------------------------------------------------

    section(
        "20. EXISTING PROVIDER SEMANTIC CAPABILITIES"
    )

    for cls in provider_classes:

        print()
        print(
            f"{cls.__name__}"
        )

        print(
            f"  module : "
            f"{cls.__module__}"
        )

        first_doc_line = (
            inspect.getdoc(cls)
            or "<none>"
        ).splitlines()[0]

        print(
            f"  docstring : "
            f"{first_doc_line}"
        )

        for name, value in inspect.getmembers(cls):

            if name.startswith("_"):
                continue

            if inspect.isfunction(value) or inspect.ismethod(value):

                try:
                    signature = inspect.signature(
                        value
                    )

                except Exception:

                    signature = (
                        "<signature unavailable>"
                    )

                print(
                    f"  method {name}{signature}"
                )

    # -----------------------------------------------------------------
    # 21
    # -----------------------------------------------------------------

    section(
        "21. STALE PRODUCTION ACQUISITION SEMANTICS"
    )

    stale_tokens = (
        "SourceType.LOCAL",
        "SourceType.REMOTE",
        "SourceType.GRETIL",
        "SourceStatus.AVAILABLE",
    )

    stale_counts: dict[
        str,
        int,
    ] = {}

    for token in stale_tokens:

        results = print_token(
            "Production stale acquisition reference",
            token,
            production,
        )

        stale_counts[
            token
        ] = len(results)

    # -----------------------------------------------------------------
    # 22
    # -----------------------------------------------------------------

    section(
        "22. READ-ONLY GENERIC MANIFEST PROBE"
    )

    probe_source = CorpusSource(
        source_id="amarakosha:probe",
        name="Amarakosha Probe",
        source_type=SourceType.LEXICON,
        source_format=SourceFormat.TXT,
        status=SourceStatus.REGISTERED,
        download_urls=[
            "https://example.invalid/amarakosha.txt"
        ],
        metadata={
            "work_identifier": "amarakosha",
            "probe": True,
        },
    )

    print(
        "Probe CorpusSource construction : PASS"
    )

    print(
        f"  source_id    : "
        f"{probe_source.source_id!r}"
    )

    print(
        f"  name         : "
        f"{probe_source.name!r}"
    )

    print(
        f"  source_type  : "
        f"{probe_source.source_type!r}"
    )

    print(
        f"  source_format: "
        f"{probe_source.source_format!r}"
    )

    print(
        f"  status       : "
        f"{probe_source.status!r}"
    )

    manifest = AcquisitionManifest(
        manifest_id="amarakosha:probe",
        source=probe_source,
        urls=list(
            probe_source.download_urls
        ),
        preferred_format=SourceFormat.TXT,
        importer="amarakosha",
        encoding="utf-8",
        normalize_unicode=True,
        validate_checksum=False,
        validate_license=False,
        enabled=True,
        metadata={
            "work_identifier": "amarakosha",
            "probe": True,
        },
    )

    print(
        "Probe AcquisitionManifest construction : PASS"
    )

    print(
        f"  manifest_id : "
        f"{manifest.manifest_id!r}"
    )

    print(
        f"  all_urls    : "
        f"{manifest.all_urls!r}"
    )

    print(
        f"  preferred_format : "
        f"{manifest.preferred_format!r}"
    )

    print(
        f"  importer : "
        f"{manifest.importer!r}"
    )

    print(
        f"  enabled : "
        f"{manifest.enabled!r}"
    )

    print(
        f"  requires_download : "
        f"{manifest.requires_download}"
    )

    # -----------------------------------------------------------------
    # 23
    # -----------------------------------------------------------------

    section(
        "23. PROVIDER / ACQUISITION COMPATIBILITY"
    )

    print(
        "The following questions are answered "
        "from observed contracts only."
    )

    print()

    print(
        "CorpusSource can represent a lexical source : "
        f"{probe_source.source_type is SourceType.LEXICON}"
    )

    print(
        "AcquisitionManifest can reference CorpusSource : "
        f"{manifest.source is probe_source}"
    )

    print(
        "Manifest contains acquisition URL : "
        f"{manifest.has_urls}"
    )

    print(
        "Manifest has preferred format : "
        f"{manifest.preferred_format is not SourceFormat.UNKNOWN}"
    )

    print(
        "Manifest identifies Amarakośa importer : "
        f"{manifest.importer == 'amarakosha'}"
    )

    print(
        "Manifest can carry work metadata : "
        f"{manifest.get_metadata('work_identifier') == 'amarakosha'}"
    )

    # -----------------------------------------------------------------
    # 24
    # -----------------------------------------------------------------

    section(
        "24. SPECIFIC PROVIDER NECESSITY TEST"
    )

    print(
        "Amarakośa-specific provider exists : "
        f"{bool(specific_results['AmarakoshaProvider'])}"
    )

    print(
        "Amarakośa-specific acquirer exists : "
        f"{bool(specific_results['AmarakoshaAcquirer'])}"
    )

    print(
        "Amarakośa-specific downloader exists : "
        f"{bool(specific_results['AmarakoshaDownloader'])}"
    )

    print(
        "Amarakośa-specific source exists : "
        f"{bool(specific_results['AmarakoshaSource'])}"
    )

    print(
        "Amarakośa-specific manifest exists : "
        f"{bool(specific_results['AmarakoshaManifest'])}"
    )

    print()

    print(
        "Absence of a source-specific implementation "
        "does not imply that a new class should be created."
    )

    # -----------------------------------------------------------------
    # 25
    # -----------------------------------------------------------------

    section(
        "25. OBSERVED IMPORT BLOCKERS"
    )

    blockers: list[str] = []

    for module_name, error in (
        provider_import_failures.items()
    ):

        blockers.append(
            f"provider:{module_name}: {error!r}"
        )

    for module_name, error in (
        downloader_import_failures.items()
    ):

        blockers.append(
            f"downloader:{module_name}: {error!r}"
        )

    for module_path, error in (
        acquisition_service_failures.items()
    ):

        blockers.append(
            f"service:{module_path}: {error!r}"
        )

    if acquisition_manager_module is None:

        blockers.append(
            "manager: "
            f"{acquisition_manager_error!r}"
        )

    if blockers:

        print(
            "Production import blockers detected:"
        )

        for blocker in blockers:

            print(
                f"  - {blocker}"
            )

    else:

        print(
            "No production import blockers detected "
            "in audited generic acquisition modules."
        )

    # -----------------------------------------------------------------
    # 26
    # -----------------------------------------------------------------

    section(
        "26. IMPORTANT ARCHITECTURAL INTERPRETATION"
    )

    print(
        "The audit does NOT treat missing concrete implementations "
        "as defects by themselves."
    )

    print()

    print(
        "The audit DOES treat production import failures and "
        "syntax errors as compatibility findings."
    )

    print()

    print(
        "ProviderRegistry abstractness is recorded as an "
        "architectural contract, not as a failure."
    )

    print()

    print(
        "Downloader class names are discovered from the actual "
        "module rather than assumed by the audit."
    )

    print()

    print(
        "No Amarakośa-specific provider/acquirer/downloader/source/"
        "manifest is created by this audit."
    )

    # -----------------------------------------------------------------
    # 27
    # -----------------------------------------------------------------

    section(
        "27. REPAIR DECISION"
    )

    print(
        "NO PRODUCTION REPAIR."
    )

    print(
        "No provider created."
    )

    print(
        "No acquirer created."
    )

    print(
        "No downloader created."
    )

    print(
        "No manifest created."
    )

    print(
        "No SourceType members added."
    )

    print(
        "No SourceStatus members added."
    )

    print(
        "No acquisition APIs changed."
    )

    print(
        "This revision is audit-only."
    )

    # -----------------------------------------------------------------
    # 28
    # -----------------------------------------------------------------

    section(
        "28. FINAL RESULT"
    )

    if blockers:

        print(
            "BATCH 5H-5E-13R-4R — "
            "RESULT: AUDIT COMPLETE WITH PRODUCTION BLOCKERS"
        )

        print()

        print(
            "The generic acquisition boundary was successfully "
            "inspected, but one or more production modules currently "
            "fail to import."
        )

        print()

        print(
            "These blockers must be separated from the Amarakośa "
            "architecture decision."
        )

        print()

        print(
            "Next step: inspect the concrete downloader/provider/"
            "manager contracts exposed by this revised audit before "
            "performing any production repair."
        )

    else:

        print(
            "BATCH 5H-5E-13R-4R — RESULT: PASS"
        )

        print()

        print(
            "Generic acquisition boundaries have been audited."
        )

        print()

        print(
            "Next step: identify and audit the concrete "
            "Amarakośa source artifact and transport."
        )


if __name__ == "__main__":
    main()
