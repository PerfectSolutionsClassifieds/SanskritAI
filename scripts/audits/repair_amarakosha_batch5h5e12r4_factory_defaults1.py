"""
Batch 5H-5E-12R-4
-----------------

Minimal CorpusSourceFactory default repair.

MUTATION.

Changes ONLY:

    from_file():
        SourceType.LOCAL -> SourceType.UNKNOWN

    from_url():
        SourceType.REMOTE -> SourceType.UNKNOWN

No other production architecture is changed.

Safety
------
- Requires the exact stale source text to be present.
- Refuses to continue if the expected text is absent.
- Refuses to continue if either target occurs more than once.
- Creates a timestamped backup.
- Verifies the resulting source text.
- Compiles the repaired factory.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path("/content/SanskritAI")

FACTORY = (
    PROJECT_ROOT
    / "acquisition"
    / "factories"
    / "corpus_source_factory.py"
)

BACKUP_DIR = (
    PROJECT_ROOT
    / "scripts"
    / "audits"
    / "backups"
)


def section(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def fail(message: str) -> None:
    raise RuntimeError(message)


def main() -> None:

    section(
        "BATCH 5H-5E-12R-4 — MINIMAL FACTORY DEFAULT REPAIR"
    )

    print()
    print("Project root :", PROJECT_ROOT)
    print("Factory      :", FACTORY)

    # ------------------------------------------------------------------
    # 1. Validate target
    # ------------------------------------------------------------------

    section("1. TARGET VALIDATION")

    if not FACTORY.exists():
        fail(f"Factory file not found: {FACTORY}")

    print("Factory exists : PASS")

    original = FACTORY.read_text(encoding="utf-8")

    print("Factory read   : PASS")

    # ------------------------------------------------------------------
    # 2. Exact stale patterns
    # ------------------------------------------------------------------

    section("2. EXACT STALE DEFAULT VALIDATION")

    file_pattern = (
        "source_type: SourceType = SourceType.LOCAL,"
    )

    url_pattern = (
        "source_type: SourceType = SourceType.REMOTE,"
    )

    file_count = original.count(file_pattern)
    url_count = original.count(url_pattern)

    print(
        "from_file stale default occurrences :",
        file_count,
    )

    print(
        "from_url stale default occurrences  :",
        url_count,
    )

    if file_count != 1:
        fail(
            "Expected exactly one from_file stale default."
        )

    if url_count != 1:
        fail(
            "Expected exactly one from_url stale default."
        )

    print("Exact target validation : PASS")

    # ------------------------------------------------------------------
    # 3. Ensure unrelated stale enum references are not silently
    #    modified.
    # ------------------------------------------------------------------

    section("3. SCOPE VALIDATION")

    source_type_local = "SourceType.LOCAL"
    source_type_remote = "SourceType.REMOTE"
    source_type_gretil = "SourceType.GRETIL"

    print(
        "SourceType.LOCAL occurrences :",
        original.count(source_type_local),
    )

    print(
        "SourceType.REMOTE occurrences:",
        original.count(source_type_remote),
    )

    print(
        "SourceType.GRETIL occurrences:",
        original.count(source_type_gretil),
    )

    if original.count(source_type_local) != 1:
        fail(
            "Unexpected SourceType.LOCAL scope."
        )

    if original.count(source_type_remote) != 1:
        fail(
            "Unexpected SourceType.REMOTE scope."
        )

    if source_type_gretil in original:
        fail(
            "Unexpected SourceType.GRETIL reference "
            "inside CorpusSourceFactory."
        )

    print("Scope validation : PASS")

    # ------------------------------------------------------------------
    # 4. Backup
    # ------------------------------------------------------------------

    section("4. BACKUP")

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup = (
        BACKUP_DIR
        / f"corpus_source_factory_pre_5h5e12r4_{timestamp}.py"
    )

    shutil.copy2(
        FACTORY,
        backup,
    )

    print("Backup :", backup)
    print("Backup creation : PASS")

    # ------------------------------------------------------------------
    # 5. Exact mutation
    # ------------------------------------------------------------------

    section("5. MINIMAL MUTATION")

    repaired = original.replace(
        file_pattern,
        "source_type: SourceType = SourceType.UNKNOWN,",
    )

    repaired = repaired.replace(
        url_pattern,
        "source_type: SourceType = SourceType.UNKNOWN,",
    )

    if repaired == original:
        fail(
            "No source change occurred."
        )

    FACTORY.write_text(
        repaired,
        encoding="utf-8",
    )

    print(
        "from_file default : "
        "SourceType.LOCAL -> SourceType.UNKNOWN"
    )

    print(
        "from_url default  : "
        "SourceType.REMOTE -> SourceType.UNKNOWN"
    )

    print("Factory mutation : PASS")

    # ------------------------------------------------------------------
    # 6. Post-mutation lexical verification
    # ------------------------------------------------------------------

    section("6. POST-MUTATION LEXICAL VERIFICATION")

    current = FACTORY.read_text(
        encoding="utf-8"
    )

    checks = {
        "old from_file default absent":
            file_pattern not in current,

        "old from_url default absent":
            url_pattern not in current,

        "new from_file default present":
            "source_type: SourceType = SourceType.UNKNOWN,"
            in current,

        "new from_url default present":
            "source_type: SourceType = SourceType.UNKNOWN,"
            in current,
    }

    for label, result in checks.items():
        print(
            f"{label:<45}: "
            f"{'PASS' if result else 'FAIL'}"
        )

        if not result:
            fail(
                f"Verification failed: {label}"
            )

    print()
    print(
        "Remaining SourceType.LOCAL :",
        current.count("SourceType.LOCAL"),
    )

    print(
        "Remaining SourceType.REMOTE:",
        current.count("SourceType.REMOTE"),
    )

    print(
        "Remaining SourceType.GRETIL:",
        current.count("SourceType.GRETIL"),
    )

    # ------------------------------------------------------------------
    # 7. Syntax verification
    # ------------------------------------------------------------------

    section("7. SYNTAX VERIFICATION")

    result = subprocess.run(
        [
            "python",
            "-m",
            "py_compile",
            str(FACTORY),
        ],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:

        print(result.stdout)
        print(result.stderr)

        fail(
            "Repaired CorpusSourceFactory failed py_compile."
        )

    print(
        "CorpusSourceFactory py_compile : PASS"
    )

    # ------------------------------------------------------------------
    # 8. Final scope verification
    # ------------------------------------------------------------------

    section("8. FINAL SCOPE VERIFICATION")

    print(
        "Modified production file:"
    )
    print(
        "  acquisition/factories/corpus_source_factory.py"
    )

    print()
    print(
        "Intentionally NOT modified:"
    )
    print(
        "  acquisition/models/source_type.py"
    )
    print(
        "  acquisition/models/corpus_source.py"
    )
    print(
        "  acquisition/discovery/providers/local_directory_provider.py"
    )
    print(
        "  acquisition/parsers/gretil_catalog_parser.py"
    )

    # ------------------------------------------------------------------
    # 9. Conclusion
    # ------------------------------------------------------------------

    section("9. REPAIR CONCLUSION")

    print("Factory default repair : COMPLETE")
    print("Backup                 : COMPLETE")
    print("Exact mutation         : COMPLETE")
    print("Lexical verification   : PASS")
    print("Syntax verification    : PASS")
    print()
    print(
        "READY FOR 5H-5E-12R-4R RUNTIME FACTORY VERIFICATION."
    )

    print()
    print("=" * 100)
    print(
        "BATCH 5H-5E-12R-4 — MINIMAL FACTORY DEFAULT REPAIR COMPLETE"
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
