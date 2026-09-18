from __future__ import annotations

"""
BATCH 5H-5E-10R-4B
==================

Minimal SourceFormatDetector compatibility repair.

Purpose
-------
Repair detector references to SourceFormat members that do not exist
in the canonical SourceFormat enum.

Current canonical archive members:
    SourceFormat.ZIP
    SourceFormat.TAR
    SourceFormat.GZIP

There is currently no:
    SourceFormat.TAR_GZIP
    SourceFormat.SEVEN_ZIP
    SourceFormat.RAR

Therefore this repair:
    .tar.gz -> SourceFormat.GZIP
    .tgz    -> SourceFormat.GZIP

and removes unsupported:
    .7z
    .rar

TEI mappings are intentionally preserved:
    .tei     -> SourceFormat.TEI_XML
    .tei.xml -> SourceFormat.TEI_XML

No SourceFormat enum modification is performed.
"""

from pathlib import Path
import py_compile
import re
import shutil


ROOT = Path("/content/SanskritAI")
TARGET = ROOT / "acquisition" / "detectors" / "source_format_detector.py"

BACKUP = TARGET.with_name(
    TARGET.name + ".5h5e10r4b.sourceformat_compatibility.bak"
)


def section(title: str) -> None:
    print()
    print("-" * 112)
    print(title)
    print("-" * 112)


def main() -> None:
    print("=" * 112)
    print("BATCH 5H-5E-10R-4B — MINIMAL SOURCEFORMAT DETECTOR COMPATIBILITY REPAIR")
    print("=" * 112)

    # ------------------------------------------------------------------
    # 1. Target
    # ------------------------------------------------------------------
    section("1. TARGET")

    print(f"Target : {TARGET}")
    print(f"Exists : {TARGET.exists()}")

    if not TARGET.exists():
        raise FileNotFoundError(
            f"Production target does not exist: {TARGET}"
        )

    # ------------------------------------------------------------------
    # 2. Read production source
    # ------------------------------------------------------------------
    source = TARGET.read_text(encoding="utf-8")

    # ------------------------------------------------------------------
    # 3. Verify canonical SourceFormat
    # ------------------------------------------------------------------
    section("2. CANONICAL SOURCEFORMAT VALIDATION")

    from SanskritAI.acquisition.models.source_format import SourceFormat

    print(f"SourceFormat.TEI_XML : {SourceFormat.TEI_XML}")
    print(f"Has TEI             : {hasattr(SourceFormat, 'TEI')}")
    print(f"Has TAR              : {hasattr(SourceFormat, 'TAR')}")
    print(f"Has GZIP             : {hasattr(SourceFormat, 'GZIP')}")
    print(f"Has ZIP              : {hasattr(SourceFormat, 'ZIP')}")
    print(f"Has TAR_GZIP         : {hasattr(SourceFormat, 'TAR_GZIP')}")
    print(f"Has SEVEN_ZIP        : {hasattr(SourceFormat, 'SEVEN_ZIP')}")
    print(f"Has RAR              : {hasattr(SourceFormat, 'RAR')}")

    if not hasattr(SourceFormat, "TEI_XML"):
        raise RuntimeError(
            "Canonical SourceFormat.TEI_XML is missing."
        )

    if hasattr(SourceFormat, "TEI"):
        raise RuntimeError(
            "Unexpected legacy SourceFormat.TEI exists."
        )

    # ------------------------------------------------------------------
    # 4. Current detector references
    # ------------------------------------------------------------------
    section("3. CURRENT DETECTOR REFERENCES")

    interesting = (
        "SourceFormat.TEI",
        "SourceFormat.TEI_XML",
        "SourceFormat.TAR",
        "SourceFormat.GZIP",
        "SourceFormat.ZIP",
        "SourceFormat.TAR_GZIP",
        "SourceFormat.SEVEN_ZIP",
        "SourceFormat.RAR",
    )

    for index, line in enumerate(source.splitlines(), start=1):
        if any(token in line for token in interesting):
            print(f"{index:4}: {line}")

    # ------------------------------------------------------------------
    # 5. Exact diagnosis
    # ------------------------------------------------------------------
    section("4. EXACT-STATE DIAGNOSIS")

    tei_stale = re.findall(
        r"SourceFormat\.TEI(?!_XML)",
        source,
    )

    tei_double = source.count(
        "SourceFormat.TEI_XML_XML"
    )

    unsupported_tar_gzip = source.count(
        "SourceFormat.TAR_GZIP"
    )

    unsupported_seven_zip = source.count(
        "SourceFormat.SEVEN_ZIP"
    )

    unsupported_rar = source.count(
        "SourceFormat.RAR"
    )

    print(
        "Exact stale SourceFormat.TEI occurrences :",
        len(tei_stale),
    )
    print(
        "SourceFormat.TEI_XML_XML occurrences      :",
        tei_double,
    )
    print(
        "SourceFormat.TAR_GZIP occurrences         :",
        unsupported_tar_gzip,
    )
    print(
        "SourceFormat.SEVEN_ZIP occurrences        :",
        unsupported_seven_zip,
    )
    print(
        "SourceFormat.RAR occurrences              :",
        unsupported_rar,
    )

    # ------------------------------------------------------------------
    # 6. Backup
    # ------------------------------------------------------------------
    section("5. BACKUP CURRENT PRODUCTION FILE")

    shutil.copy2(TARGET, BACKUP)

    print(f"Backup : {BACKUP}")
    print(f"Exists : {BACKUP.exists()}")

    # ------------------------------------------------------------------
    # 7. Minimal repair
    # ------------------------------------------------------------------
    section("6. MINIMAL EXACT REPAIR")

    repaired = source

    # Safety correction for any accidental double corruption.
    repaired = repaired.replace(
        "SourceFormat.TEI_XML_XML",
        "SourceFormat.TEI_XML",
    )

    # Exact stale TEI reference only.
    repaired = re.sub(
        r"SourceFormat\.TEI(?!_XML)",
        "SourceFormat.TEI_XML",
        repaired,
    )

    # Canonical archive compatibility.
    repaired = repaired.replace(
        "SourceFormat.TAR_GZIP",
        "SourceFormat.GZIP",
    )

    repaired = repaired.replace(
        "SourceFormat.SEVEN_ZIP",
        "SourceFormat.UNKNOWN",
    )

    repaired = repaired.replace(
        "SourceFormat.RAR",
        "SourceFormat.UNKNOWN",
    )

    # ------------------------------------------------------------------
    # 8. Remove unsupported 7z/RAR mappings
    # ------------------------------------------------------------------
    #
    # UNKNOWN is not useful as a "supported" detector mapping.
    # Therefore remove the extension entries entirely after converting
    # the references, rather than pretending that these formats are
    # supported.
    #
    repaired = re.sub(
        r'^\s*"\.7z":\s*SourceFormat\.UNKNOWN,\s*\n',
        "",
        repaired,
        flags=re.MULTILINE,
    )

    repaired = re.sub(
        r'^\s*"\.rar":\s*SourceFormat\.UNKNOWN,\s*\n',
        "",
        repaired,
        flags=re.MULTILINE,
    )

    changed = repaired != source

    if changed:
        TARGET.write_text(
            repaired,
            encoding="utf-8",
            newline="\n",
        )
        print("Production file rewritten : YES")
    else:
        print("Production file rewritten : NO")
        print("Already in canonical compatible state.")

    # ------------------------------------------------------------------
    # 9. Lexical validation
    # ------------------------------------------------------------------
    section("7. POST-REPAIR LEXICAL VALIDATION")

    final_source = TARGET.read_text(encoding="utf-8")

    final_tei_double = final_source.count(
        "SourceFormat.TEI_XML_XML"
    )

    final_tei_stale = re.findall(
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
        final_tei_double,
    )
    print(
        "Exact SourceFormat.TEI remaining    :",
        len(final_tei_stale),
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

    if final_tei_double:
        raise RuntimeError(
            "SourceFormat.TEI_XML_XML still remains."
        )

    if final_tei_stale:
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

    # ------------------------------------------------------------------
    # 10. Python compilation
    # ------------------------------------------------------------------
    section("8. PYTHON SYNTAX VALIDATION")

    py_compile.compile(
        str(TARGET),
        doraise=True,
    )

    print("Production source compilation : PASS")

    # ------------------------------------------------------------------
    # 11. Runtime detector validation
    # ------------------------------------------------------------------
    section("9. SOURCEFORMAT DETECTOR RUNTIME VALIDATION")

    from SanskritAI.acquisition.detectors.source_format_detector import (
        SourceFormatDetector,
    )

    print(
        "SourceFormatDetector import : PASS"
    )

    tei_result = SourceFormatDetector.detect(
        "sample.tei"
    )

    tei_xml_result = SourceFormatDetector.detect(
        "sample.tei.xml"
    )

    tar_gz_result = SourceFormatDetector.detect(
        "sample.tar.gz"
    )

    tgz_result = SourceFormatDetector.detect(
        "sample.tgz"
    )

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
        ".7z        ->",
        seven_zip_result,
    )
    print(
        ".rar       ->",
        rar_result,
    )

    if tei_result is not SourceFormat.TEI_XML:
        raise RuntimeError(
            f".tei did not resolve to TEI_XML: {tei_result!r}"
        )

    if tei_xml_result is not SourceFormat.TEI_XML:
        raise RuntimeError(
            f".tei.xml did not resolve to TEI_XML: {tei_xml_result!r}"
        )

    if tar_gz_result is not SourceFormat.GZIP:
        raise RuntimeError(
            f".tar.gz did not resolve to GZIP: {tar_gz_result!r}"
        )

    if tgz_result is not SourceFormat.GZIP:
        raise RuntimeError(
            f".tgz did not resolve to GZIP: {tgz_result!r}"
        )

    if seven_zip_result is not None:
        raise RuntimeError(
            f".7z unexpectedly remains supported: {seven_zip_result!r}"
        )

    if rar_result is not None:
        raise RuntimeError(
            f".rar unexpectedly remains supported: {rar_result!r}"
        )

    print("TEI detection : PASS")
    print("GZIP compound detection : PASS")
    print("Unsupported 7z detection : PASS")
    print("Unsupported RAR detection : PASS")

    # ------------------------------------------------------------------
    # 12. Final
    # ------------------------------------------------------------------
    print()
    print("=" * 112)
    print("BATCH 5H-5E-10R-4B RESULT : PASS")
    print("=" * 112)
    print()
    print("Production changes:")
    print("  .tei       -> SourceFormat.TEI_XML")
    print("  .tei.xml   -> SourceFormat.TEI_XML")
    print("  .tar.gz    -> SourceFormat.GZIP")
    print("  .tgz       -> SourceFormat.GZIP")
    print("  .7z        -> unsupported / None")
    print("  .rar       -> unsupported / None")
    print()
    print("SourceFormat enum was NOT modified.")
    print("CorpusSourceFactory was NOT modified.")
    print("WorkRegistry was NOT modified.")
    print()


if __name__ == "__main__":
    main()
