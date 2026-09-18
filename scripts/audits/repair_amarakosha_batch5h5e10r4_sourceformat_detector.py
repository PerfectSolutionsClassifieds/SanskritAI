from __future__ import annotations

"""
BATCH 5H-5E-10R-4B
==================

Minimal SourceFormatDetector compatibility repair.

Purpose
-------
Repair stale SourceFormat references in the detector without modifying
the canonical SourceFormat enum.

Canonical package bootstrap
---------------------------
This script may be executed directly from:

    /content/SanskritAI/scripts/audits/

Therefore /content MUST be added to sys.path before importing:

    SanskritAI

Canonical SourceFormat members verified by the runtime audit include:

    SourceFormat.TEI_XML
    SourceFormat.TAR
    SourceFormat.GZIP
    SourceFormat.ZIP

Known invalid legacy detector references:

    SourceFormat.TEI
    SourceFormat.TAR_GZIP
    SourceFormat.SEVEN_ZIP
    SourceFormat.RAR

Minimal repair:

    .tei     -> SourceFormat.TEI_XML
    .tei.xml -> SourceFormat.TEI_XML

    .tar.gz  -> SourceFormat.GZIP
    .tgz     -> SourceFormat.GZIP

Unsupported formats:

    .7z
    .rar

are removed from the detector mapping.

IMPORTANT
---------
This script does NOT modify:

    SourceFormat
    CorpusSourceFactory
    WorkRegistry
    WorkDefinition
    CorpusSource

Only the stale consumer references in SourceFormatDetector are repaired.
"""

from pathlib import Path
import py_compile
import re
import shutil
import sys


# =============================================================================
# 0. PACKAGE BOOTSTRAP
# =============================================================================

# File:
#   /content/SanskritAI/scripts/audits/<this_file>
#
# Package root:
#   /content/SanskritAI
#
# Python package parent:
#   /content
#
# Therefore /content must be present on sys.path for:
#   import SanskritAI
#
PROJECT_ROOT = Path("/content/SanskritAI")
PACKAGE_PARENT = PROJECT_ROOT.parent

if str(PACKAGE_PARENT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_PARENT))


# =============================================================================
# PATHS
# =============================================================================

TARGET = (
    PROJECT_ROOT
    / "acquisition"
    / "detectors"
    / "source_format_detector.py"
)

BACKUP = TARGET.with_name(
    TARGET.name
    + ".5h5e10r4.sourceformat_compatibility.bak"
)


# =============================================================================
# HELPERS
# =============================================================================

def section(title: str) -> None:
    print()
    print("-" * 112)
    print(title)
    print("-" * 112)


def main() -> None:

    print("=" * 112)
    print(
        "BATCH 5H-5E-10R-4B — "
        "MINIMAL SOURCEFORMAT DETECTOR COMPATIBILITY REPAIR"
    )
    print("=" * 112)

    # =========================================================================
    # 1. BOOTSTRAP VALIDATION
    # =========================================================================

    section("1. PACKAGE BOOTSTRAP")

    print("Project root   :", PROJECT_ROOT)
    print("Package parent :", PACKAGE_PARENT)

    print(
        "Package parent on sys.path :",
        str(PACKAGE_PARENT) in sys.path,
    )

    if str(PACKAGE_PARENT) not in sys.path:
        raise RuntimeError(
            "Package bootstrap failed: /content is not on sys.path."
        )

    import SanskritAI

    print(
        "SanskritAI import : PASS"
    )

    # =========================================================================
    # 2. TARGET
    # =========================================================================

    section("2. TARGET")

    print(
        "Target :",
        TARGET,
    )

    print(
        "Exists :",
        TARGET.exists(),
    )

    if not TARGET.exists():
        raise FileNotFoundError(
            f"Production target does not exist: {TARGET}"
        )

    # =========================================================================
    # 3. READ SOURCE
    # =========================================================================

    source = TARGET.read_text(
        encoding="utf-8"
    )

    # =========================================================================
    # 4. CANONICAL SOURCEFORMAT VALIDATION
    # =========================================================================

    section("3. CANONICAL SOURCEFORMAT VALIDATION")

    from SanskritAI.acquisition.models.source_format import (
        SourceFormat,
    )

    print(
        "SourceFormat import : PASS"
    )

    print(
        "SourceFormat.TEI_XML :",
        SourceFormat.TEI_XML,
    )

    print(
        "Has SourceFormat.TEI :",
        hasattr(SourceFormat, "TEI"),
    )

    print(
        "Has SourceFormat.TAR :",
        hasattr(SourceFormat, "TAR"),
    )

    print(
        "Has SourceFormat.GZIP :",
        hasattr(SourceFormat, "GZIP"),
    )

    print(
        "Has SourceFormat.ZIP :",
        hasattr(SourceFormat, "ZIP"),
    )

    print(
        "Has SourceFormat.TAR_GZIP :",
        hasattr(SourceFormat, "TAR_GZIP"),
    )

    print(
        "Has SourceFormat.SEVEN_ZIP :",
        hasattr(SourceFormat, "SEVEN_ZIP"),
    )

    print(
        "Has SourceFormat.RAR :",
        hasattr(SourceFormat, "RAR"),
    )

    if not hasattr(SourceFormat, "TEI_XML"):
        raise RuntimeError(
            "Canonical SourceFormat.TEI_XML is missing."
        )

    # =========================================================================
    # 5. CURRENT DETECTOR REFERENCES
    # =========================================================================

    section("4. CURRENT DETECTOR REFERENCES")

    interesting_tokens = (
        "SourceFormat.TEI",
        "SourceFormat.TEI_XML",
        "SourceFormat.TAR",
        "SourceFormat.GZIP",
        "SourceFormat.ZIP",
        "SourceFormat.TAR_GZIP",
        "SourceFormat.SEVEN_ZIP",
        "SourceFormat.RAR",
    )

    for index, line in enumerate(
        source.splitlines(),
        start=1,
    ):
        if any(
            token in line
            for token in interesting_tokens
        ):
            print(
                f"{index:4}: {line}"
            )

    # =========================================================================
    # 6. EXACT DIAGNOSIS
    # =========================================================================

    section("5. EXACT-STATE DIAGNOSIS")

    exact_stale_tei = re.findall(
        r"SourceFormat\.TEI(?!_XML)",
        source,
    )

    tei_xml_xml_count = source.count(
        "SourceFormat.TEI_XML_XML"
    )

    tar_gzip_count = source.count(
        "SourceFormat.TAR_GZIP"
    )

    seven_zip_count = source.count(
        "SourceFormat.SEVEN_ZIP"
    )

    rar_count = source.count(
        "SourceFormat.RAR"
    )

    print(
        "Exact stale SourceFormat.TEI occurrences :",
        len(exact_stale_tei),
    )

    print(
        "SourceFormat.TEI_XML_XML occurrences      :",
        tei_xml_xml_count,
    )

    print(
        "SourceFormat.TAR_GZIP occurrences         :",
        tar_gzip_count,
    )

    print(
        "SourceFormat.SEVEN_ZIP occurrences        :",
        seven_zip_count,
    )

    print(
        "SourceFormat.RAR occurrences              :",
        rar_count,
    )

    # =========================================================================
    # 7. BACKUP
    # =========================================================================

    section("6. BACKUP CURRENT PRODUCTION FILE")

    shutil.copy2(
        TARGET,
        BACKUP,
    )

    print(
        "Backup :",
        BACKUP,
    )

    print(
        "Exists :",
        BACKUP.exists(),
    )

    # =========================================================================
    # 8. MINIMAL REPAIR
    # =========================================================================

    section("7. MINIMAL EXACT REPAIR")

    repaired = source

    # -------------------------------------------------------------------------
    # Safety correction for the accidental previous repair corruption.
    # -------------------------------------------------------------------------

    repaired = repaired.replace(
        "SourceFormat.TEI_XML_XML",
        "SourceFormat.TEI_XML",
    )

    # -------------------------------------------------------------------------
    # Exact stale TEI reference.
    #
    # IMPORTANT:
    #
    #   SourceFormat.TEI_XML
    #
    # must NOT match this expression.
    # -------------------------------------------------------------------------

    repaired = re.sub(
        r"SourceFormat\.TEI(?!_XML)",
        "SourceFormat.TEI_XML",
        repaired,
    )

    # -------------------------------------------------------------------------
    # TAR.GZ / TGZ
    #
    # These are represented by the existing canonical GZIP member.
    # -------------------------------------------------------------------------

    repaired = repaired.replace(
        "SourceFormat.TAR_GZIP",
        "SourceFormat.GZIP",
    )

    # -------------------------------------------------------------------------
    # Remove unsupported 7z and RAR mappings.
    #
    # We do NOT replace these with SourceFormat.UNKNOWN because that would
    # introduce a semantic "supported" mapping without evidence that UNKNOWN
    # is the correct detector contract.
    #
    # Remove only the mapping lines.
    # -------------------------------------------------------------------------

    repaired = re.sub(
        r'^[ \t]*"\.7z"[ \t]*:[ \t]*SourceFormat\.SEVEN_ZIP[ \t]*,[ \t]*\n',
        "",
        repaired,
        flags=re.MULTILINE,
    )

    repaired = re.sub(
        r'^[ \t]*"\.rar"[ \t]*:[ \t]*SourceFormat\.RAR[ \t]*,[ \t]*\n',
        "",
        repaired,
        flags=re.MULTILINE,
    )

    changed = (
        repaired != source
    )

    if changed:

        TARGET.write_text(
            repaired,
            encoding="utf-8",
            newline="\n",
        )

        print(
            "Production file rewritten : YES"
        )

    else:

        print(
            "Production file rewritten : NO"
        )

        print(
            "Already in canonical compatible state."
        )

    # =========================================================================
    # 9. POST-REPAIR LEXICAL VALIDATION
    # =========================================================================

    section("8. POST-REPAIR LEXICAL VALIDATION")

    final_source = TARGET.read_text(
        encoding="utf-8"
    )

    final_tei_xml_xml = final_source.count(
        "SourceFormat.TEI_XML_XML"
    )

    final_exact_tei = re.findall(
        r"SourceFormat\.TEI(?!_XML)",
        final_source,
    )

    final_tar_gzip = final_source.count(
        "SourceFormat.TAR_GZIP"
    )

    final_seven_zip = final_source.count(
        "SourceFormat.SEVEN_ZIP"
    )

    final_rar = final_source.count(
        "SourceFormat.RAR"
    )

    final_tei_xml = final_source.count(
        "SourceFormat.TEI_XML"
    )

    print(
        "SourceFormat.TEI_XML_XML remaining :",
        final_tei_xml_xml,
    )

    print(
        "Exact SourceFormat.TEI remaining    :",
        len(final_exact_tei),
    )

    print(
        "SourceFormat.TAR_GZIP remaining     :",
        final_tar_gzip,
    )

    print(
        "SourceFormat.SEVEN_ZIP remaining    :",
        final_seven_zip,
    )

    print(
        "SourceFormat.RAR remaining          :",
        final_rar,
    )

    print(
        "SourceFormat.TEI_XML occurrences    :",
        final_tei_xml,
    )

    if final_tei_xml_xml:
        raise RuntimeError(
            "SourceFormat.TEI_XML_XML still remains."
        )

    if final_exact_tei:
        raise RuntimeError(
            "Exact stale SourceFormat.TEI references remain."
        )

    if final_tar_gzip:
        raise RuntimeError(
            "SourceFormat.TAR_GZIP still remains."
        )

    if final_seven_zip:
        raise RuntimeError(
            "SourceFormat.SEVEN_ZIP still remains."
        )

    if final_rar:
        raise RuntimeError(
            "SourceFormat.RAR still remains."
        )

    # =========================================================================
    # 10. PYTHON SYNTAX VALIDATION
    # =========================================================================

    section("9. PYTHON SYNTAX VALIDATION")

    py_compile.compile(
        str(TARGET),
        doraise=True,
    )

    print(
        "Production source compilation : PASS"
    )

    # =========================================================================
    # 11. RUNTIME DETECTOR IMPORT
    # =========================================================================

    section("10. SOURCEFORMAT DETECTOR RUNTIME VALIDATION")

    from SanskritAI.acquisition.detectors.source_format_detector import (
        SourceFormatDetector,
    )

    print(
        "SourceFormatDetector import : PASS"
    )

    # -------------------------------------------------------------------------
    # TEI
    # -------------------------------------------------------------------------

    tei_result = SourceFormatDetector.detect(
        "sample.tei"
    )

    tei_xml_result = SourceFormatDetector.detect(
        "sample.tei.xml"
    )

    # -------------------------------------------------------------------------
    # GZIP
    # -------------------------------------------------------------------------

    tar_gz_result = SourceFormatDetector.detect(
        "sample.tar.gz"
    )

    tgz_result = SourceFormatDetector.detect(
        "sample.tgz"
    )

    # -------------------------------------------------------------------------
    # Existing archive formats
    # -------------------------------------------------------------------------

    tar_result = SourceFormatDetector.detect(
        "sample.tar"
    )

    gzip_result = SourceFormatDetector.detect(
        "sample.gz"
    )

    zip_result = SourceFormatDetector.detect(
        "sample.zip"
    )

    # -------------------------------------------------------------------------
    # Unsupported formats
    # -------------------------------------------------------------------------

    seven_zip_result = SourceFormatDetector.detect(
        "sample.7z"
    )

    rar_result = SourceFormatDetector.detect(
        "sample.rar"
    )

    print(
        ".tei       ->",
        tei_result,
    )

    print(
        ".tei.xml   ->",
        tei_xml_result,
    )

    print(
        ".tar.gz    ->",
        tar_gz_result,
    )

    print(
        ".tgz       ->",
        tgz_result,
    )

    print(
        ".tar       ->",
        tar_result,
    )

    print(
        ".gz        ->",
        gzip_result,
    )

    print(
        ".zip       ->",
        zip_result,
    )

    print(
        ".7z        ->",
        seven_zip_result,
    )

    print(
        ".rar       ->",
        rar_result,
    )

    # =========================================================================
    # 12. ASSERTIONS
    # =========================================================================

    if tei_result is not SourceFormat.TEI_XML:
        raise RuntimeError(
            f".tei did not resolve to TEI_XML: {tei_result!r}"
        )

    if tei_xml_result is not SourceFormat.TEI_XML:
        raise RuntimeError(
            f".tei.xml did not resolve to TEI_XML: "
            f"{tei_xml_result!r}"
        )

    if tar_gz_result is not SourceFormat.GZIP:
        raise RuntimeError(
            f".tar.gz did not resolve to GZIP: "
            f"{tar_gz_result!r}"
        )

    if tgz_result is not SourceFormat.GZIP:
        raise RuntimeError(
            f".tgz did not resolve to GZIP: "
            f"{tgz_result!r}"
        )

    if tar_result is not SourceFormat.TAR:
        raise RuntimeError(
            f".tar did not resolve to TAR: "
            f"{tar_result!r}"
        )

    if gzip_result is not SourceFormat.GZIP:
        raise RuntimeError(
            f".gz did not resolve to GZIP: "
            f"{gzip_result!r}"
        )

    if zip_result is not SourceFormat.ZIP:
        raise RuntimeError(
            f".zip did not resolve to ZIP: "
            f"{zip_result!r}"
        )

    if seven_zip_result is not None:
        raise RuntimeError(
            f".7z unexpectedly remains supported: "
            f"{seven_zip_result!r}"
        )

    if rar_result is not None:
        raise RuntimeError(
            f".rar unexpectedly remains supported: "
            f"{rar_result!r}"
        )

    print(
        "TEI detection              : PASS"
    )

    print(
        "GZIP compound detection    : PASS"
    )

    print(
        "TAR detection              : PASS"
    )

    print(
        "ZIP detection              : PASS"
    )

    print(
        "Unsupported 7z detection   : PASS"
    )

    print(
        "Unsupported RAR detection  : PASS"
    )

    # =========================================================================
    # 13. FINAL
    # =========================================================================

    print()
    print("=" * 112)
    print(
        "BATCH 5H-5E-10R-4B RESULT : PASS"
    )
    print("=" * 112)

    print()
    print(
        "Production compatibility state:"
    )

    print(
        "  .tei       -> SourceFormat.TEI_XML"
    )

    print(
        "  .tei.xml   -> SourceFormat.TEI_XML"
    )

    print(
        "  .tar.gz    -> SourceFormat.GZIP"
    )

    print(
        "  .tgz       -> SourceFormat.GZIP"
    )

    print(
        "  .tar       -> SourceFormat.TAR"
    )

    print(
        "  .gz        -> SourceFormat.GZIP"
    )

    print(
        "  .zip       -> SourceFormat.ZIP"
    )

    print(
        "  .7z        -> unsupported"
    )

    print(
        "  .rar       -> unsupported"
    )

    print()
    print(
        "SourceFormat enum was NOT modified."
    )

    print(
        "CorpusSourceFactory was NOT modified."
    )

    print(
        "WorkRegistry was NOT modified."
    )

    print()


if __name__ == "__main__":
    main()
