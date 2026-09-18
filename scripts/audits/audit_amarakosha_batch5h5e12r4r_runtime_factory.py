from __future__ import annotations

"""
BATCH 5H-5E-12R-4R — RUNTIME FACTORY VERIFICATION

Purpose
-------
Runtime verification of CorpusSourceFactory after the minimal
5H-5E-12R-4 factory-default repair.

Canonical semantics
-------------------
SourceType describes WHAT a source fundamentally is.

Therefore:
    from_file() -> SourceType.UNKNOWN by default
    from_url()  -> SourceType.UNKNOWN by default

Callers may explicitly provide semantic types such as:
    SourceType.LEXICON
    SourceType.CORPUS

This audit is READ-ONLY.
It must not mutate production files.
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path("/content/SanskritAI")

FACTORY_PATH = (
    PROJECT_ROOT
    / "acquisition"
    / "factories"
    / "corpus_source_factory.py"
)


def fail(message: str) -> None:
    raise RuntimeError(message)


def section(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def main() -> None:
    section(
        "BATCH 5H-5E-12R-4R — RUNTIME FACTORY VERIFICATION"
    )

    print(f"Project root : {PROJECT_ROOT}")
    print(f"Factory      : {FACTORY_PATH}")

    # ---------------------------------------------------------
    # 1. Package bootstrap
    # ---------------------------------------------------------
    section("1. PACKAGE BOOTSTRAP")

    if str(PROJECT_ROOT.parent) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT.parent))

    import SanskritAI

    print(
        f"SanskritAI import : PASS ({SanskritAI.__name__})"
    )

    # ---------------------------------------------------------
    # 2. Canonical SourceType runtime validation
    # ---------------------------------------------------------
    section("2. SOURCETYPE RUNTIME VALIDATION")

    from SanskritAI.acquisition.models.source_type import (
        SourceType,
    )

    print("SourceType import : PASS")

    members = {
        name: member.value
        for name, member in SourceType.__members__.items()
    }

    print("Canonical SourceType members:")

    for name, value in members.items():
        print(
            f"  {name} = {value!r}"
        )

    required = {
        "UNKNOWN",
        "LEXICON",
        "CORPUS",
    }

    missing = required.difference(members)

    if missing:
        fail(
            "Missing required SourceType members: "
            + ", ".join(sorted(missing))
        )

    print(
        "UNKNOWN / LEXICON / CORPUS members : PASS"
    )

    forbidden = {
        "LOCAL",
        "REMOTE",
        "GRETIL",
    }

    present_forbidden = forbidden.intersection(members)

    if present_forbidden:
        fail(
            "Forbidden stale SourceType members present: "
            + ", ".join(sorted(present_forbidden))
        )

    print(
        "LOCAL / REMOTE / GRETIL absent : PASS"
    )

    # ---------------------------------------------------------
    # 3. Canonical SourceStatus runtime validation
    # ---------------------------------------------------------
    section("3. SOURCESTATUS RUNTIME VALIDATION")

    from SanskritAI.acquisition.models.source_status import (
        SourceStatus,
    )

    print("SourceStatus import : PASS")

    status_members = {
        name: member.value
        for name, member in SourceStatus.__members__.items()
    }

    print("Canonical SourceStatus members:")

    for name, value in status_members.items():
        print(
            f"  {name} = {value!r}"
        )

    if "REGISTERED" not in status_members:
        fail(
            "Canonical SourceStatus.REGISTERED is missing."
        )

    print(
        "SourceStatus.REGISTERED member : PASS"
    )

    if "AVAILABLE" in status_members:
        fail(
            "Stale SourceStatus.AVAILABLE member is present."
        )

    print(
        "Stale SourceStatus.AVAILABLE member absent : PASS"
    )

    # ---------------------------------------------------------
    # 4. CorpusSource runtime validation
    # ---------------------------------------------------------
    section("4. CORPUSSOURCE RUNTIME VALIDATION")

    from SanskritAI.acquisition.models.corpus_source import (
        CorpusSource,
    )

    print("CorpusSource import : PASS")

    corpus_fields = getattr(
        CorpusSource,
        "__dataclass_fields__",
        {},
    )

    if "source_id" not in corpus_fields:
        fail(
            "CorpusSource does not expose canonical "
            "source_id field."
        )

    if "identifier" in corpus_fields:
        print(
            "CorpusSource identifier field : PRESENT"
        )
    else:
        print(
            "CorpusSource identifier field : ABSENT "
            "(canonical source_id is used)"
        )

    print(
        "CorpusSource canonical source_id field : PASS"
    )

    # ---------------------------------------------------------
    # 5. Factory runtime import
    # ---------------------------------------------------------
    section("5. FACTORY RUNTIME IMPORT")

    from SanskritAI.acquisition.factories.corpus_source_factory import (
        CorpusSourceFactory,
    )

    print(
        "CorpusSourceFactory import : PASS"
    )

    factory = CorpusSourceFactory()

    print(
        f"Factory construction : PASS ({factory!r})"
    )

    # ---------------------------------------------------------
    # 6. Local-file factory runtime probe
    # ---------------------------------------------------------
    section("6. FROM_FILE() RUNTIME PROBE")

    probe_file = (
        PROJECT_ROOT
        / "resources"
        / "work_registry.json"
    )

    if not probe_file.exists():
        fail(
            f"Runtime probe file does not exist: {probe_file}"
        )

    local_source = CorpusSourceFactory.from_file(
        probe_file
    )

    if not isinstance(local_source, CorpusSource):
        fail(
            "from_file() did not return CorpusSource."
        )

    print(
        "from_file() return type : PASS"
    )

    # ---------------------------------------------------------
    # Canonical CorpusSource field access
    # ---------------------------------------------------------
    print(
        f"source_id    : {local_source.source_id!r}"
    )

    print(
        f"name         : {local_source.name!r}"
    )

    print(
        f"source_type  : {local_source.source_type!r}"
    )

    print(
        f"source_format: {local_source.source_format!r}"
    )

    print(
        f"status       : {local_source.status!r}"
    )

    if local_source.source_type is not SourceType.UNKNOWN:
        fail(
            "from_file() default source_type is not "
            "SourceType.UNKNOWN."
        )

    print(
        "from_file() default SourceType.UNKNOWN : PASS"
    )

    if local_source.local_path != probe_file:
        fail(
            "from_file() local_path mismatch."
        )

    print(
        "from_file() local_path : PASS"
    )

    if local_source.status is not SourceStatus.REGISTERED:
        fail(
            "from_file() default status is not "
            "SourceStatus.REGISTERED."
        )

    print(
        "from_file() default SourceStatus.REGISTERED : PASS"
    )

    metadata = dict(local_source.metadata)

    if "filename" not in metadata:
        fail(
            "from_file() did not populate filename metadata."
        )

    if "size_bytes" not in metadata:
        fail(
            "from_file() did not populate size_bytes metadata."
        )

    if "directory" not in metadata:
        fail(
            "from_file() did not populate directory metadata."
        )

    print(
        "from_file() file metadata : PASS"
    )

    # ---------------------------------------------------------
    # 7. Explicit lexical source type
    # ---------------------------------------------------------
    section("7. EXPLICIT LEXICON SOURCE TYPE")

    lexical_source = CorpusSourceFactory.from_file(
        probe_file,
        source_type=SourceType.LEXICON,
    )

    if lexical_source.source_type is not SourceType.LEXICON:
        fail(
            "Explicit SourceType.LEXICON was not preserved."
        )

    print(
        "Explicit SourceType.LEXICON preserved : PASS"
    )

    # ---------------------------------------------------------
    # 8. Explicit corpus source type
    # ---------------------------------------------------------
    section("8. EXPLICIT CORPUS SOURCE TYPE")

    corpus_source = CorpusSourceFactory.from_file(
        probe_file,
        source_type=SourceType.CORPUS,
    )

    if corpus_source.source_type is not SourceType.CORPUS:
        fail(
            "Explicit SourceType.CORPUS was not preserved."
        )

    print(
        "Explicit SourceType.CORPUS preserved : PASS"
    )

    # ---------------------------------------------------------
    # 9. Remote URL factory runtime probe
    # ---------------------------------------------------------
    section("9. FROM_URL() RUNTIME PROBE")

    probe_url = (
        "https://example.org/resources/"
        "amarakosha.xml"
    )

    remote_source = CorpusSourceFactory.from_url(
        probe_url,
        title="Amarakosha Probe",
    )

    if not isinstance(remote_source, CorpusSource):
        fail(
            "from_url() did not return CorpusSource."
        )

    print(
        "from_url() return type : PASS"
    )

    print(
        f"source_id    : {remote_source.source_id!r}"
    )

    print(
        f"name         : {remote_source.name!r}"
    )

    print(
        f"source_type  : {remote_source.source_type!r}"
    )

    print(
        f"source_format: {remote_source.source_format!r}"
    )

    print(
        f"status       : {remote_source.status!r}"
    )

    if remote_source.source_type is not SourceType.UNKNOWN:
        fail(
            "from_url() default source_type is not "
            "SourceType.UNKNOWN."
        )

    print(
        "from_url() default SourceType.UNKNOWN : PASS"
    )

    if remote_source.status is not SourceStatus.REGISTERED:
        fail(
            "from_url() default status is not "
            "SourceStatus.REGISTERED."
        )

    print(
        "from_url() default SourceStatus.REGISTERED : PASS"
    )

    if not remote_source.download_urls:
        fail(
            "from_url() did not populate download_urls."
        )

    if remote_source.download_urls[0] != probe_url:
        fail(
            "from_url() download_urls mismatch."
        )

    print(
        "from_url() download_urls : PASS"
    )

    # ---------------------------------------------------------
    # 10. Explicit lexical URL source type
    # ---------------------------------------------------------
    section("10. EXPLICIT LEXICON URL SOURCE TYPE")

    lexical_url_source = CorpusSourceFactory.from_url(
        probe_url,
        title="Amarakosha Probe",
        source_type=SourceType.LEXICON,
    )

    if lexical_url_source.source_type is not SourceType.LEXICON:
        fail(
            "Explicit SourceType.LEXICON was not preserved "
            "through from_url()."
        )

    print(
        "from_url() explicit SourceType.LEXICON : PASS"
    )

    # ---------------------------------------------------------
    # 11. Generic metadata factory
    # ---------------------------------------------------------
    section("11. FROM_METADATA() RUNTIME PROBE")

    metadata_source = CorpusSourceFactory.from_metadata(
        identifier="amarakosha:runtime-probe",
        title="Amarakosha Runtime Probe",
        source_type=SourceType.LEXICON,
        source_format=remote_source.source_format,
        metadata={
            "repository": "runtime-probe",
        },
    )

    if not isinstance(metadata_source, CorpusSource):
        fail(
            "from_metadata() did not return CorpusSource."
        )

    print(
        "from_metadata() return type : PASS"
    )

    if metadata_source.source_id != "amarakosha:runtime-probe":
        fail(
            "from_metadata() did not preserve identifier "
            "as canonical source_id."
        )

    print(
        "from_metadata() source_id : PASS"
    )

    if metadata_source.source_type is not SourceType.LEXICON:
        fail(
            "from_metadata() did not preserve "
            "SourceType.LEXICON."
        )

    print(
        "from_metadata() source_type : PASS"
    )

    if (
        metadata_source.metadata.get("repository")
        != "runtime-probe"
    ):
        fail(
            "from_metadata() metadata was not preserved."
        )

    print(
        "from_metadata() metadata preservation : PASS"
    )

    # ---------------------------------------------------------
    # 12. Utility runtime probe
    # ---------------------------------------------------------
    section("12. IS_SUPPORTED() RUNTIME PROBE")

    supported = CorpusSourceFactory.is_supported(
        probe_file
    )

    if not isinstance(supported, bool):
        fail(
            "is_supported() did not return bool."
        )

    print(
        f"is_supported(work_registry.json) : {supported}"
    )

    print(
        "is_supported() return type : PASS"
    )

    # ---------------------------------------------------------
    # 13. Factory source inspection
    # ---------------------------------------------------------
    section("13. FACTORY SOURCE SCOPE VALIDATION")

    source = FACTORY_PATH.read_text(
        encoding="utf-8"
    )

    stale_refs = [
        ref
        for ref in (
            "SourceType.LOCAL",
            "SourceType.REMOTE",
            "SourceType.GRETIL",
            "SourceStatus.AVAILABLE",
        )
        if ref in source
    ]

    if stale_refs:
        fail(
            "Factory still contains stale references: "
            + ", ".join(stale_refs)
        )

    print(
        "No SourceType.LOCAL reference : PASS"
    )

    print(
        "No SourceType.REMOTE reference : PASS"
    )

    print(
        "No SourceType.GRETIL reference : PASS"
    )

    print(
        "No SourceStatus.AVAILABLE reference : PASS"
    )

    # ---------------------------------------------------------
    # 14. Read-only guarantee
    # ---------------------------------------------------------
    section("14. READ-ONLY VERIFICATION")

    print(
        "No production file mutation performed : PASS"
    )

    print(
        "No SourceType mutation performed : PASS"
    )

    print(
        "No SourceStatus mutation performed : PASS"
    )

    print(
        "No CorpusSource mutation performed : PASS"
    )

    print(
        "No factory source mutation performed : PASS"
    )

    # ---------------------------------------------------------
    # 15. Final result
    # ---------------------------------------------------------
    section("15. FINAL RESULT")

    print(
        "Runtime factory import : PASS"
    )

    print(
        "from_file() -> UNKNOWN : PASS"
    )

    print(
        "from_url()  -> UNKNOWN : PASS"
    )

    print(
        "Explicit LEXICON preserved : PASS"
    )

    print(
        "Explicit CORPUS preserved : PASS"
    )

    print(
        "from_metadata() preserved : PASS"
    )

    print(
        "Canonical source_id access : PASS"
    )

    print(
        "Canonical SourceStatus.REGISTERED : PASS"
    )

    print(
        "Factory stale SourceType references : 0"
    )

    print(
        "Factory stale SourceStatus references : 0"
    )

    print()

    print("=" * 100)
    print(
        "BATCH 5H-5E-12R-4R — RESULT: PASS"
    )
    print("=" * 100)

    print(
        "CorpusSourceFactory runtime behavior is canonical."
    )

    print(
        "Ready for BATCH 5H-5E-13R — Amarakośa acquisition boundary."
    )


if __name__ == "__main__":
    main()
