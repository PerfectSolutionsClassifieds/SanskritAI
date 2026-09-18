
from __future__ import annotations

"""
BATCH 5H-5E-13R-4
=================

AMARAKOSHA GENERIC ACQUISITION BOUNDARY AUDIT

Purpose
-------
Audit the existing generic acquisition execution chain before
introducing any Amarakośa-specific acquisition implementation.

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
2. Can an existing provider handle the request?
3. Can SourceAcquirer consume the manifest?
4. Can the downloader consume the manifest?
5. Does AcquisitionManager orchestrate the path?
6. Is provider selection generic?
7. Is an Amarakośa-specific provider actually necessary?
8. Are there stale SourceType / SourceStatus references in
   actual production execution paths?

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
"""

from pathlib import Path
import inspect
import re
import sys


PROJECT_ROOT = Path("/content/SanskritAI")


def section(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def fail(message: str) -> None:
    raise RuntimeError(message)


def is_historical_python(path: Path) -> bool:
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

    result = []

    for path in PROJECT_ROOT.rglob("*.py"):

        if is_historical_python(path):
            continue

        if classify_path(path) != "production":
            continue

        result.append(path)

    return sorted(result)


def print_class(cls, label: str) -> None:

    print()
    print(f"{label}")
    print(f"Class     : {cls}")
    print(f"Module    : {cls.__module__}")
    print(f"Name      : {cls.__name__}")

    print()
    print("Constructor:")

    try:
        print(
            f"  {inspect.signature(cls)}"
        )
    except Exception as exc:
        print(
            f"  <unavailable: {exc}>"
        )

    print()
    print("Docstring:")

    print(
        inspect.getdoc(cls) or "<none>"
    )


def print_public_methods(cls) -> None:

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

    results = []

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
            f"  ... {len(results) - limit} additional matches"
        )

    return results


def main() -> None:

    section(
        "BATCH 5H-5E-13R-4 — "
        "GENERIC ACQUISITION BOUNDARY AUDIT"
    )

    if not PROJECT_ROOT.exists():

        fail(
            f"Project root does not exist: "
            f"{PROJECT_ROOT}"
        )

    section("1. PACKAGE BOOTSTRAP")

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
        f"SanskritAI import : PASS ({SanskritAI.__name__})"
    )

    section("2. PRODUCTION FILE CLASSIFICATION")

    production = production_files()

    print(
        f"Production Python files : {len(production)}"
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

    section("3. CORE ACQUISITION MODELS")

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

    section("4. SOURCETYPE CONTRACT")

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

    section("5. SOURCE FORMAT CONTRACT")

    print(
        "SourceFormat members:"
    )

    for name, member in SourceFormat.__members__.items():

        print(
            f"  {name} = {member.value!r}"
        )

    section("6. SOURCE STATUS CONTRACT")

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

    section("7. ACQUISITION MANIFEST BEHAVIOUR")

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

    section("8. GENERIC PROVIDER LAYER")

    from SanskritAI.acquisition.providers.base_provider import (
        BaseProvider,
    )

    from SanskritAI.acquisition.providers.acquisition_request import (
        AcquisitionRequest,
    )

    from SanskritAI.acquisition.providers.acquisition_response import (
        AcquisitionResponse,
    )

    from SanskritAI.acquisition.providers.provider_registry import (
        ProviderRegistry,
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

    print_class(
        ProviderRegistry,
        "ProviderRegistry",
    )

    print_public_methods(
        BaseProvider
    )

    print_public_methods(
        ProviderRegistry
    )

    section("9. EXISTING PROVIDER IMPLEMENTATIONS")

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

    provider_classes = []

    import importlib

    for module_name in provider_modules:

        module_path = (
            "SanskritAI.acquisition.providers."
            + module_name
        )

        try:

            module = importlib.import_module(
                module_path
            )

        except Exception as exc:

            print(
                f"  {module_name}: IMPORT FAIL -> {exc!r}"
            )

            continue

        print()
        print(
            f"  {module_name}: IMPORT PASS"
        )

        for name, value in inspect.getmembers(
            module,
            inspect.isclass,
        ):

            if (
                value.__module__ == module.__name__
                and value is not BaseProvider
            ):

                provider_classes.append(
                    value
                )

                print(
                    f"    class: {name}"
                )

    section("10. PROVIDER REGISTRY RUNTIME")

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

        registry = None

    section("11. SOURCE ACQUIRER LAYER")

    from SanskritAI.acquisition.acquirers.source_acquirer import (
        SourceAcquirer,
    )

    from SanskritAI.acquisition.acquirers.default_source_acquirer import (
        DefaultSourceAcquirer,
    )

    print_class(
        SourceAcquirer,
        "SourceAcquirer",
    )

    print_class(
        DefaultSourceAcquirer,
        "DefaultSourceAcquirer",
    )

    print_public_methods(
        SourceAcquirer
    )

    print_public_methods(
        DefaultSourceAcquirer
    )

    section("12. DOWNLOADER LAYER")

    from SanskritAI.acquisition.downloaders.base_downloader import (
        BaseDownloader,
    )

    from SanskritAI.acquisition.downloaders.http_downloader import (
        HttpDownloader,
    )

    from SanskritAI.acquisition.downloaders.local_file_importer import (
        LocalFileImporter,
    )

    print_class(
        BaseDownloader,
        "BaseDownloader",
    )

    print_class(
        HttpDownloader,
        "HttpDownloader",
    )

    print_class(
        LocalFileImporter,
        "LocalFileImporter",
    )

    print_public_methods(
        BaseDownloader
    )

    print_public_methods(
        HttpDownloader
    )

    print_public_methods(
        LocalFileImporter
    )

    section("13. ACQUISITION MANAGER")

    from SanskritAI.acquisition.acquisition_manager import (
        AcquisitionManager,
    )

    print_class(
        AcquisitionManager,
        "AcquisitionManager",
    )

    print_public_methods(
        AcquisitionManager
    )

    section("14. ACQUISITION SERVICE")

    from SanskritAI.acquisition.services.acquisition_service import (
        AcquisitionService,
    )

    from SanskritAI.acquisition.services.default_acquisition_service import (
        DefaultAcquisitionService,
    )

    print_class(
        AcquisitionService,
        "AcquisitionService",
    )

    print_class(
        DefaultAcquisitionService,
        "DefaultAcquisitionService",
    )

    print_public_methods(
        AcquisitionService
    )

    print_public_methods(
        DefaultAcquisitionService
    )

    section("15. GENERIC ACQUISITION REFERENCES — PRODUCTION")

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

    section("16. PROVIDER REGISTRY REFERENCES — PRODUCTION")

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

    section("17. AMARAKOSHA ACQUISITION REFERENCES — PRODUCTION")

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

    section("18. AMARAKOSHA-SPECIFIC ACQUISITION CLASSES")

    specific_tokens = (
        "AmarakoshaProvider",
        "AmarakoshaAcquirer",
        "AmarakoshaDownloader",
        "AmarakoshaSource",
        "AmarakoshaManifest",
    )

    specific_results = {}

    for token in specific_tokens:

        results = print_token(
            "Production Amarakośa acquisition class",
            token,
            production,
        )

        specific_results[token] = results

    section("19. EXISTING PROVIDER SEMANTIC CAPABILITIES")

    for cls in provider_classes:

        print()
        print(
            f"{cls.__name__}"
        )

        print(
            f"  module : {cls.__module__}"
        )

        print(
            f"  docstring : "
            f"{(inspect.getdoc(cls) or '<none>').splitlines()[0]}"
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
                    f"  method {name}{signature}"
                )

    section("20. STALE PRODUCTION ACQUISITION SEMANTICS")

    stale_tokens = (
        "SourceType.LOCAL",
        "SourceType.REMOTE",
        "SourceType.GRETIL",
        "SourceStatus.AVAILABLE",
    )

    stale_counts = {}

    for token in stale_tokens:

        results = print_token(
            "Production stale acquisition reference",
            token,
            production,
        )

        stale_counts[token] = len(results)

    section("21. READ-ONLY GENERIC MANIFEST PROBE")

    from pathlib import Path

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
        f"  source_id   : {probe_source.source_id!r}"
    )

    print(
        f"  name        : {probe_source.name!r}"
    )

    print(
        f"  source_type : {probe_source.source_type!r}"
    )

    print(
        f"  source_format: {probe_source.source_format!r}"
    )

    print(
        f"  status      : {probe_source.status!r}"
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
        f"  manifest_id : {manifest.manifest_id!r}"
    )

    print(
        f"  all_urls    : {manifest.all_urls!r}"
    )

    print(
        f"  preferred_format : "
        f"{manifest.preferred_format!r}"
    )

    print(
        f"  importer : {manifest.importer!r}"
    )

    print(
        f"  enabled : {manifest.enabled!r}"
    )

    print(
        f"  requires_download : "
        f"{manifest.requires_download}"
    )

    section("22. PROVIDER / ACQUISITION COMPATIBILITY")

    print(
        "The following questions are intentionally "
        "answered from observed contracts only."
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

    section("23. SPECIFIC PROVIDER NECESSITY TEST")

    print(
        "Amarakośa-specific provider exists : "
        f"{any(specific_results[token] for token in ('AmarakoshaProvider',))}"
    )

    print(
        "Amarakośa-specific acquirer exists : "
        f"{any(specific_results[token] for token in ('AmarakoshaAcquirer',))}"
    )

    print(
        "Amarakośa-specific downloader exists : "
        f"{any(specific_results[token] for token in ('AmarakoshaDownloader',))}"
    )

    print(
        "Amarakośa-specific manifest exists : "
        f"{any(specific_results[token] for token in ('AmarakoshaManifest',))}"
    )

    print()

    print(
        "These absence results do NOT imply that new classes "
        "should be created."
    )

    print(
        "The next decision depends on the concrete Amarakośa "
        "source artifact and its transport/discovery requirements."
    )

    section("24. REPAIR DECISION")

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

    section("25. FINAL RESULT")

    print(
        "BATCH 5H-5E-13R-4 — RESULT: PASS"
    )

    print(
        "Generic acquisition boundaries have been audited."
    )

    print(
        "Next step: identify and audit the concrete "
        "Amarakośa source artifact and transport."
    )


if __name__ == "__main__":
    main()
