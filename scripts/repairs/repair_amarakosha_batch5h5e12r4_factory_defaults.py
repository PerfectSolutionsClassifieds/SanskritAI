
from __future__ import annotations

"""
BATCH 5H-5E-12R-4 — MINIMAL FACTORY DEFAULT REPAIR

Purpose
-------
Repair stale SourceType.LOCAL / SourceType.REMOTE defaults in
CorpusSourceFactory.

Canonical semantic model
------------------------
SourceType describes WHAT a source fundamentally is.

Storage / transport are represented separately through:
* local_path
* download_url
* source_format
* metadata

Therefore:

    from_file() -> SourceType.UNKNOWN by default
    from_url()  -> SourceType.UNKNOWN by default

Callers may explicitly provide:
    SourceType.LEXICON
    SourceType.CORPUS
    SourceType.GRAMMAR
    etc.

This script is intentionally idempotent.

If the repair has already been applied, the script must:
* recognize the canonical state
* perform no mutation
* continue with validation
* report ALREADY CANONICAL

It must never fail simply because the repair was previously applied.
"""

from pathlib import Path
from datetime import datetime
import re
import shutil
import sys


PROJECT_ROOT = Path("/content/SanskritAI")

FACTORY_PATH = (
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


STALE_LOCAL = "source_type: SourceType = SourceType.LOCAL,"
STALE_REMOTE = "source_type: SourceType = SourceType.REMOTE,"

CANONICAL_UNKNOWN = "source_type: SourceType = SourceType.UNKNOWN,"

STALE_FACTORY_REFS = (
    "SourceType.LOCAL",
    "SourceType.REMOTE",
    "SourceType.GRETIL",
)


def fail(message: str) -> None:
    raise RuntimeError(message)


def section(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def count_exact(source: str, pattern: str) -> int:
    return source.count(pattern)


def active_source_type_refs(source: str) -> list[str]:
    """
    Return stale SourceType references in production code while
    ignoring comments and docstrings.

    The factory should contain no LOCAL / REMOTE / GRETIL semantic
    SourceType references after this repair.
    """

    lines = source.splitlines()

    refs: list[str] = []

    in_triple_double = False
    in_triple_single = False

    for line in lines:
        stripped = line.strip()

        if not in_triple_double and not in_triple_single:
            if stripped.startswith('"""'):
                if stripped.count('"""') == 1:
                    in_triple_double = True
                    continue
            elif stripped.startswith("'''"):
                if stripped.count("'''") == 1:
                    in_triple_single = True
                    continue

        elif in_triple_double:
            if '"""' in stripped:
                in_triple_double = False
            continue

        elif in_triple_single:
            if "'''" in stripped:
                in_triple_single = False
            continue

        if not stripped:
            continue

        if stripped.startswith("#"):
            continue

        for ref in STALE_FACTORY_REFS:
            if ref in line:
                refs.append(ref)

    return refs


def backup_factory() -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_path = (
        BACKUP_DIR
        / f"corpus_source_factory.py.5h5e12r4.{timestamp}.bak"
    )

    shutil.copy2(FACTORY_PATH, backup_path)

    return backup_path


def validate_signature_context(
    source: str,
    method_name: str,
    expected_default: str,
) -> None:
    """
    Verify the default belongs to the intended factory method.

    This avoids blindly counting a matching line elsewhere.
    """

    pattern = re.compile(
        rf"def\s+{re.escape(method_name)}\s*\("
        rf"(?P<body>.*?)(?=\n\s*def\s+|\Z)",
        re.DOTALL,
    )

    match = pattern.search(source)

    if not match:
        fail(
            f"Unable to locate CorpusSourceFactory.{method_name}()."
        )

    body = match.group("body")

    occurrences = body.count(expected_default)

    if occurrences != 1:
        fail(
            f"{method_name}() expected exactly one canonical "
            f"default occurrence; found {occurrences}."
        )


def main() -> None:

    section(
        "BATCH 5H-5E-12R-4 — MINIMAL FACTORY DEFAULT REPAIR"
    )

    print(f"Project root : {PROJECT_ROOT}")
    print(f"Factory      : {FACTORY_PATH}")

    # ---------------------------------------------------------
    # 1. Target validation
    # ---------------------------------------------------------

    section("1. TARGET VALIDATION")

    if not PROJECT_ROOT.exists():
        fail(
            f"Project root does not exist: {PROJECT_ROOT}"
        )

    print("Project root : PASS")

    if not FACTORY_PATH.exists():
        fail(
            f"Factory file does not exist: {FACTORY_PATH}"
        )

    print("Factory exists : PASS")

    source = FACTORY_PATH.read_text(
        encoding="utf-8"
    )

    print("Factory read   : PASS")

    # ---------------------------------------------------------
    # 2. Determine current state
    # ---------------------------------------------------------

    section("2. EXACT DEFAULT STATE VALIDATION")

    stale_local_count = count_exact(
        source,
        STALE_LOCAL,
    )

    stale_remote_count = count_exact(
        source,
        STALE_REMOTE,
    )

    canonical_unknown_count = count_exact(
        source,
        CANONICAL_UNKNOWN,
    )

    print(
        "from_file stale default occurrences : "
        f"{stale_local_count}"
    )

    print(
        "from_url stale default occurrences  : "
        f"{stale_remote_count}"
    )

    print(
        "canonical UNKNOWN default occurrences : "
        f"{canonical_unknown_count}"
    )

    # ---------------------------------------------------------
    # 3. Idempotent state decision
    # ---------------------------------------------------------

    section("3. IDEMPOTENT REPAIR DECISION")

    if stale_local_count > 1:
        fail(
            "Unexpected multiple from_file stale defaults."
        )

    if stale_remote_count > 1:
        fail(
            "Unexpected multiple from_url stale defaults."
        )

    if stale_local_count == 1:
        print(
            "from_file default : STALE -> SourceType.LOCAL"
        )
    else:
        print(
            "from_file default : no stale LOCAL default found"
        )

    if stale_remote_count == 1:
        print(
            "from_url default : STALE -> SourceType.REMOTE"
        )
    else:
        print(
            "from_url default : no stale REMOTE default found"
        )

    # ---------------------------------------------------------
    # 4. Apply minimal repair only when required
    # ---------------------------------------------------------

    needs_repair = (
        stale_local_count == 1
        or stale_remote_count == 1
    )

    backup_path: Path | None = None

    if needs_repair:

        section("4. APPLY MINIMAL FACTORY DEFAULT REPAIR")

        backup_path = backup_factory()

        print(
            f"Backup created : PASS\n"
            f"Backup path    : {backup_path}"
        )

        if stale_local_count == 1:
            source = source.replace(
                STALE_LOCAL,
                CANONICAL_UNKNOWN,
                1,
            )

            print(
                "from_file default : LOCAL -> UNKNOWN : PASS"
            )

        if stale_remote_count == 1:
            source = source.replace(
                STALE_REMOTE,
                CANONICAL_UNKNOWN,
                1,
            )

            print(
                "from_url default : REMOTE -> UNKNOWN : PASS"
            )

        FACTORY_PATH.write_text(
            source,
            encoding="utf-8",
        )

        print("Factory write : PASS")

    else:

        section("4. REPAIR STATUS")

        print(
            "Factory defaults : ALREADY CANONICAL"
        )

        print(
            "No mutation required : PASS"
        )

    # ---------------------------------------------------------
    # 5. Post-repair exact validation
    # ---------------------------------------------------------

    section("5. POST-REPAIR EXACT VALIDATION")

    source = FACTORY_PATH.read_text(
        encoding="utf-8"
    )

    post_local_count = count_exact(
        source,
        STALE_LOCAL,
    )

    post_remote_count = count_exact(
        source,
        STALE_REMOTE,
    )

    print(
        "from_file stale default occurrences : "
        f"{post_local_count}"
    )

    print(
        "from_url stale default occurrences  : "
        f"{post_remote_count}"
    )

    if post_local_count != 0:
        fail(
            "from_file still contains SourceType.LOCAL."
        )

    if post_remote_count != 0:
        fail(
            "from_url still contains SourceType.REMOTE."
        )

    print(
        "stale LOCAL default removed : PASS"
    )

    print(
        "stale REMOTE default removed : PASS"
    )

    # ---------------------------------------------------------
    # 6. Method-specific canonical validation
    # ---------------------------------------------------------

    section("6. METHOD-SPECIFIC CANONICAL VALIDATION")

    validate_signature_context(
        source,
        "from_file",
        CANONICAL_UNKNOWN,
    )

    print(
        "CorpusSourceFactory.from_file() "
        "default UNKNOWN : PASS"
    )

    validate_signature_context(
        source,
        "from_url",
        CANONICAL_UNKNOWN,
    )

    print(
        "CorpusSourceFactory.from_url() "
        "default UNKNOWN : PASS"
    )

    # ---------------------------------------------------------
    # 7. Stale semantic SourceType validation
    # ---------------------------------------------------------

    section("7. STALE SEMANTIC SOURCETYPE VALIDATION")

    active_refs = active_source_type_refs(source)

    print(
        "Active stale SourceType references : "
        f"{len(active_refs)}"
    )

    if active_refs:
        for ref in active_refs:
            print(
                f"  STALE REF : {ref}"
            )

        fail(
            "Factory still contains stale semantic "
            "SourceType references."
        )

    print(
        "SourceType.LOCAL absent from factory : PASS"
    )

    print(
        "SourceType.REMOTE absent from factory : PASS"
    )

    print(
        "SourceType.GRETIL absent from factory : PASS"
    )

    # ---------------------------------------------------------
    # 8. Scope validation
    # ---------------------------------------------------------

    section("8. CHANGE SCOPE VALIDATION")

    if "SourceType.UNKNOWN" not in source:
        fail(
            "Canonical SourceType.UNKNOWN is missing."
        )

    print(
        "SourceType.UNKNOWN present : PASS"
    )

    if "from_metadata" not in source:
        fail(
            "from_metadata() unexpectedly missing."
        )

    print(
        "from_metadata() preserved : PASS"
    )

    if "SourceFormatDetector" not in source:
        fail(
            "SourceFormatDetector dependency unexpectedly missing."
        )

    print(
        "SourceFormatDetector preserved : PASS"
    )

    if "CorpusSource(" not in source:
        fail(
            "CorpusSource construction unexpectedly missing."
        )

    print(
        "CorpusSource construction preserved : PASS"
    )

    # ---------------------------------------------------------
    # 9. Syntax validation
    # ---------------------------------------------------------

    section("9. SYNTAX VALIDATION")

    import py_compile

    py_compile.compile(
        str(FACTORY_PATH),
        doraise=True,
    )

    print(
        "corpus_source_factory.py py_compile : PASS"
    )

    # ---------------------------------------------------------
    # 10. Final state
    # ---------------------------------------------------------

    section("10. FINAL STATE")

    final_source = FACTORY_PATH.read_text(
        encoding="utf-8"
    )

    final_local = count_exact(
        final_source,
        STALE_LOCAL,
    )

    final_remote = count_exact(
        final_source,
        STALE_REMOTE,
    )

    final_unknown = count_exact(
        final_source,
        CANONICAL_UNKNOWN,
    )

    print(
        f"from_file LOCAL stale : {final_local}"
    )

    print(
        f"from_url REMOTE stale : {final_remote}"
    )

    print(
        f"UNKNOWN defaults      : {final_unknown}"
    )

    if final_local != 0 or final_remote != 0:
        fail(
            "Final factory state still contains stale defaults."
        )

    if final_unknown != 2:
        fail(
            "Expected exactly two canonical UNKNOWN defaults "
            "(from_file and from_url)."
        )

    print(
        "Canonical factory defaults : PASS"
    )

    if backup_path is not None:
        print(
            f"Mutation backup : {backup_path}"
        )
    else:
        print(
            "Mutation backup : not required; "
            "factory was already canonical"
        )

    print()
    print("=" * 100)
    print(
        "BATCH 5H-5E-12R-4 — RESULT: PASS"
    )
    print("=" * 100)
    print(
        "CorpusSourceFactory defaults are canonical."
    )
    print(
        "from_file()  -> SourceType.UNKNOWN"
    )
    print(
        "from_url()   -> SourceType.UNKNOWN"
    )
    print(
        "No SourceType enum mutation performed."
    )
    print(
        "No GRETIL repair performed."
    )
    print(
        "No LocalDirectoryProvider change performed."
    )
    print(
        "Ready for BATCH 5H-5E-12R-4R runtime verification."
    )


if __name__ == "__main__":
    main()
