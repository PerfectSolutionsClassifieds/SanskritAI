
from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path


ROOT = Path("/content/SanskritAI")
PARENT = ROOT.parent
ARTIFACT = ROOT / "amarakosha.txt"

if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))


MODULE = "SanskritAI.acquisition.sources.amarakosha_manifest"


def section(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def main() -> int:
    section(
        "13R-7A — Amarakośa production manifest runtime audit"
    )

    print(f"Repository root : {ROOT}")
    print(f"Artifact        : {ARTIFACT}")

    # ------------------------------------------------------------------
    # Artifact
    # ------------------------------------------------------------------

    section("Verified canonical artifact")

    if not ARTIFACT.exists():
        print("artifact exists : FAIL")
        return 1

    if not ARTIFACT.is_file():
        print("artifact file   : FAIL")
        return 1

    print("artifact exists : PASS")
    print(
        f"size            : "
        f"{ARTIFACT.stat().st_size:,} bytes"
    )

    # ------------------------------------------------------------------
    # Manifest module
    # ------------------------------------------------------------------

    section("Production manifest module")

    try:
        module = import_module(MODULE)
    except Exception as exc:
        print(
            "module import  : FAIL — "
            f"{type(exc).__name__}: {exc}"
        )
        return 1

    print(f"module import  : PASS — {MODULE}")

    factory = getattr(
        module,
        "create_amarakosha_manifest",
        None,
    )

    getter = getattr(
        module,
        "get_amarakosha_manifest",
        None,
    )

    if not callable(factory):
        print("factory         : FAIL")
        return 1

    if not callable(getter):
        print("getter          : FAIL")
        return 1

    print("factory         : PASS")
    print("getter          : PASS")

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    section("Manifest construction")

    try:
        manifest = factory()
    except Exception as exc:
        print(
            "construction   : FAIL — "
            f"{type(exc).__name__}: {exc}"
        )
        return 1

    print("construction   : PASS")

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    section("Manifest identity")

    checks = {
        "manifest_id":
            manifest.manifest_id
            == "amarakosha-local-txt",

        "source_id":
            manifest.source.source_id
            == "amarakosha",

        "source_name":
            manifest.source.name
            == "Amarakośa",

        "source_type":
            str(manifest.source.source_type).lower()
            == "lexicon",

        "source_format":
            str(manifest.source.source_format).lower()
            == "txt",
    }

    all_passed = True

    for label, result in checks.items():
        print(
            f"{label:<20}: "
            f"{'PASS' if result else 'FAIL'}"
        )

        if not result:
            all_passed = False

    # ------------------------------------------------------------------
    # Local acquisition contract
    # ------------------------------------------------------------------

    section("Local acquisition contract")

    local_checks = {
        "urls empty":
            manifest.urls == [],

        "mirrors empty":
            manifest.mirrors == [],

        "requires download":
            manifest.requires_download is False,

        "preferred format":
            str(manifest.preferred_format).lower()
            == "txt",

        "expected filename":
            manifest.expected_filename
            == "amarakosha.txt",

        "expected size":
            manifest.expected_size
            == ARTIFACT.stat().st_size,

        "destination":
            manifest.destination_directory == ROOT,

        "cache directory":
            manifest.cache_directory is None,

        "overwrite":
            manifest.overwrite_existing is False,

        "extract archives":
            manifest.extract_archives is False,

        "importer":
            manifest.importer == "amarakosha",

        "encoding":
            manifest.encoding == "utf-8",

        "normalize unicode":
            manifest.normalize_unicode is True,
    }

    for label, result in local_checks.items():
        print(
            f"{label:<20}: "
            f"{'PASS' if result else 'FAIL'}"
        )

        if not result:
            all_passed = False

    # ------------------------------------------------------------------
    # Integrity contract
    # ------------------------------------------------------------------

    section("Integrity contract")

    integrity_checks = {
        "checksum":
            manifest.checksum
            == "d82a5234e4bc15ef295b1b375a6548e02df9a10d6eb94e0f97223289c46c3190",

        "checksum algorithm":
            manifest.checksum_algorithm
            == "sha256",

        "checksum validation":
            manifest.requires_checksum_validation is True,

        "license validation":
            manifest.requires_license_validation is True,

        "priority":
            manifest.priority == 100,

        "enabled":
            manifest.enabled is True,
    }

    for label, result in integrity_checks.items():
        print(
            f"{label:<20}: "
            f"{'PASS' if result else 'FAIL'}"
        )

        if not result:
            all_passed = False

    # ------------------------------------------------------------------
    # Provenance metadata
    # ------------------------------------------------------------------

    section("Provenance metadata")

    metadata = manifest.metadata

    provenance_checks = {
        "filename":
            metadata.get("filename")
            == "amarakosha.txt",

        "encoding":
            metadata.get("encoding")
            == "utf-8",

        "size":
            metadata.get("size_bytes")
            == ARTIFACT.stat().st_size,

        "sha256":
            metadata.get("sha256")
            == manifest.checksum,

        "provenance URL":
            metadata.get("provenance_url")
            == "http://sanskrit.uohyd.ac.in/scl/",

        "acquisition mode":
            metadata.get("acquisition_mode")
            == "local",

        "relationship":
            "direct PDF-to-TXT derivation"
            in metadata.get(
                "provenance_relationship",
                "",
            ),
    }

    for label, result in provenance_checks.items():
        print(
            f"{label:<20}: "
            f"{'PASS' if result else 'FAIL'}"
        )

        if not result:
            all_passed = False

    # ------------------------------------------------------------------
    # Getter equivalence
    # ------------------------------------------------------------------

    section("Getter equivalence")

    try:
        getter_manifest = getter()
    except Exception as exc:
        print(
            "getter          : FAIL — "
            f"{type(exc).__name__}: {exc}"
        )
        return 1

    getter_checks = {
        "manifest_id":
            getter_manifest.manifest_id
            == manifest.manifest_id,

        "source_id":
            getter_manifest.source.source_id
            == manifest.source.source_id,

        "expected filename":
            getter_manifest.expected_filename
            == manifest.expected_filename,

        "checksum":
            getter_manifest.checksum
            == manifest.checksum,
    }

    for label, result in getter_checks.items():
        print(
            f"{label:<20}: "
            f"{'PASS' if result else 'FAIL'}"
        )

        if not result:
            all_passed = False

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    section("Manifest serialization")

    try:
        serialized = manifest.to_dict()
    except Exception as exc:
        print(
            "to_dict         : FAIL — "
            f"{type(exc).__name__}: {exc}"
        )
        return 1

    print("to_dict         : PASS")

    serialization_checks = {
        "manifest_id":
            serialized.get("manifest_id")
            == "amarakosha-local-txt",

        "source_id":
            serialized.get("source_id")
            == "amarakosha",

        "expected filename":
            serialized.get("expected_filename")
            == "amarakosha.txt",

        "checksum":
            serialized.get("checksum")
            == manifest.checksum,
    }

    for label, result in serialization_checks.items():
        print(
            f"{label:<20}: "
            f"{'PASS' if result else 'FAIL'}"
        )

        if not result:
            all_passed = False

    # ------------------------------------------------------------------
    # Final decision
    # ------------------------------------------------------------------

    section("13R-7A decision")

    if not all_passed:
        print(
            "RESULT: FAIL — Amarakośa production manifest "
            "contract is incomplete."
        )
        return 1

    print(
        "Production Amarakośa manifest : PASS"
    )
    print(
        "Local TXT acquisition contract : PASS"
    )
    print(
        "Integrity contract              : PASS"
    )
    print(
        "Provenance metadata             : PASS"
    )
    print(
        "Serialization                   : PASS"
    )

    print()
    print(
        "RESULT: PASS — Amarakośa production "
        "AcquisitionManifest is established."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
