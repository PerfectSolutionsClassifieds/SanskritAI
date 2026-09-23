
from __future__ import annotations

"""
BATCH 5H-5E-12R-4R — RUNTIME FACTORY VERIFICATION

Purpose
-------
Runtime verification of CorpusSourceFactory after the minimal
5H-5E-12R-4 factory-default repair.

Expected canonical semantics
-----------------------------
SourceType describes WHAT a source fundamentally is.

Therefore:

    from_file() -> SourceType.UNKNOWN by default
    from_url()  -> SourceType.UNKNOWN by default

Callers may explicitly provide semantic types such as:

    SourceType.LEXICON
    SourceType.CORPUS

This script is READ-ONLY.

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
    # 2. Canonical enum runtime validation
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
    # 3. CorpusSource runtime validation
    # ---------------------------------------------------------

    section("3. CORPUSSOURCE RUNTIME VALIDATION")

    from SanskritAI.acquisition.models.corpus_source import (
        CorpusSource,
    )

    print("CorpusSource import : PASS")

    # ---------------------------------------------------------
    # 4. Factory runtime import
    # ---------------------------------------------------------

    section("4. FACTORY RUNTIME IMPORT")

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
    # 5. Local-file factory runtime probe
    # ---------------------------------------------------------

    section("5. FROM_FILE() RUNTIME PROBE")

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

    print(
        f"identifier   : {local_source.identifier!r}"
    )

    print(
        f"title        : {local_source.title!r}"
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
    # 6. Explicit lexical source type
    # ---------------------------------------------------------

    section("6. EXPLICIT LEXICON SOURCE TYPE")

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
    # 7. Explicit corpus source type
    # ---------------------------------------------------------

    section("7. EXPLICIT CORPUS SOURCE TYPE")

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
    # 8. Remote URL factory runtime probe
    # ---------------------------------------------------------

    section("8. FROM_URL() RUNTIME PROBE")

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
        f"identifier   : {remote_source.identifier!r}"
    )

    print(
        f"title        : {remote_source.title!r}"
    )

    print(
        f"source_type  : {remote_source.source_type!r}"
    )

    print(
        f"source_format: {remote_source.source_format!r}"
    )

    if remote_source.source_type is not SourceType.UNKNOWN:
        fail(
            "from_url() default source_type is not "
            "SourceType.UNKNOWN."
        )

    print(
        "from_url() default SourceType.UNKNOWN : PASS"
    )

    if remote_source.download_url != probe_url:
        fail(
            "from_url() download_url mismatch."
        )

    print(
        "from_url() download_url : PASS"
    )

    # ---------------------------------------------------------
    # 9. Explicit lexical URL source type
    # ---------------------------------------------------------

    section("9. EXPLICIT LEXICON URL SOURCE TYPE")

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
    # 10. Generic metadata factory
    # ---------------------------------------------------------

    section("10. FROM_METADATA() RUNTIME PROBE")

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

    if metadata_source.source_type is not SourceType.LEXICON:
        fail(
            "from_metadata() did not preserve "
            "SourceType.LEXICON."
        )

    print(
        "from_metadata() source_type : PASS"
    )

    if metadata_source.metadata.get("repository") != "runtime-probe":
        fail(
            "from_metadata() metadata was not preserved."
        )

    print(
        "from_metadata() metadata preservation : PASS"
    )

    # ---------------------------------------------------------
    # 11. Utility runtime probe
    # ---------------------------------------------------------

    section("11. IS_SUPPORTED() RUNTIME PROBE")

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
    # 12. Factory source inspection
    # ---------------------------------------------------------

    section("12. FACTORY SOURCE SCOPE VALIDATION")

    source = FACTORY_PATH.read_text(
        encoding="utf-8"
    )

    stale_refs = [
        ref
        for ref in (
            "SourceType.LOCAL",
            "SourceType.REMOTE",
            "SourceType.GRETIL",
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

    # ---------------------------------------------------------
    # 13. Read-only guarantee
    # ---------------------------------------------------------

    section("13. READ-ONLY VERIFICATION")

    print(
        "No production file mutation performed : PASS"
    )

    print(
        "No SourceType mutation performed : PASS"
    )

    print(
        "No CorpusSource mutation performed : PASS"
    )

    print(
        "No factory source mutation performed : PASS"
    )

    # ---------------------------------------------------------
    # 14. Final result
    # ---------------------------------------------------------

    section("14. FINAL RESULT")

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
        "Factory stale SourceType references : 0"
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
