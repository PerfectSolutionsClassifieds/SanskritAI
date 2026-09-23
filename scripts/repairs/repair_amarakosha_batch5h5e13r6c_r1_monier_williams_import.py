
from __future__ import annotations

"""
SanskritAI
==========

13R-6C-R1
---------

Repair stale Monier-Williams source imports that reference the retired
``SanskritAI.domain.acquisition`` package.

The current acquisition architecture owns the canonical acquisition
enums under:

    SanskritAI.acquisition.models.source_format
    SanskritAI.acquisition.models.source_type

This repair is intentionally minimal.

It does NOT:

    - create a new abstraction
    - modify the acquisition architecture
    - modify Amarakośa models
    - modify CorpusSource
    - modify CorpusSourceFactory
    - modify the lexical domain
    - modify parser/importer logic
    - change enum members
    - change Monier-Williams source semantics

It only repairs the stale import paths in the existing
MonierWilliamsSource definition and verifies that the package can
subsequently import the Amarakośa source module.

The repair is idempotent.
"""

from pathlib import Path
import ast
import sys


REPO_ROOT = Path("/content/SanskritAI")

MONIER_WILLIAMS_FILE = (
    REPO_ROOT
    / "acquisition"
    / "sources"
    / "monier_williams.py"
)

OLD_SOURCE_FORMAT_IMPORT = (
    "from SanskritAI.domain.acquisition.source_format "
    "import SourceFormat"
)

OLD_SOURCE_TYPE_IMPORT = (
    "from SanskritAI.domain.acquisition.source_type "
    "import SourceType"
)

NEW_SOURCE_FORMAT_IMPORT = (
    "from SanskritAI.acquisition.models.source_format "
    "import SourceFormat"
)

NEW_SOURCE_TYPE_IMPORT = (
    "from SanskritAI.acquisition.models.source_type "
    "import SourceType"
)


def fail(message: str) -> None:
    raise RuntimeError(message)


def compile_file(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    compile(source, str(path), "exec")


def validate_ast(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    ast.parse(source, filename=str(path))


def main() -> None:
    print("=" * 72)
    print("13R-6C-R1 — Monier-Williams stale acquisition import repair")
    print("=" * 72)

    # ------------------------------------------------------------------
    # Repository bootstrap
    # ------------------------------------------------------------------

    if not REPO_ROOT.exists():
        fail(f"Repository root not found: {REPO_ROOT}")

    if not MONIER_WILLIAMS_FILE.exists():
        fail(
            "Monier-Williams source file not found:\n"
            f"  {MONIER_WILLIAMS_FILE}"
        )

    parent = REPO_ROOT.parent

    if str(parent) not in sys.path:
        sys.path.insert(0, str(parent))

    print(f"Repository root : {REPO_ROOT}")
    print(f"Target file     : {MONIER_WILLIAMS_FILE}")
    print("Package bootstrap : PASS")

    # ------------------------------------------------------------------
    # Read current production file
    # ------------------------------------------------------------------

    original = MONIER_WILLIAMS_FILE.read_text(
        encoding="utf-8"
    )

    print()
    print("Checking stale imports...")

    old_format_count = original.count(
        OLD_SOURCE_FORMAT_IMPORT
    )

    old_type_count = original.count(
        OLD_SOURCE_TYPE_IMPORT
    )

    new_format_count = original.count(
        NEW_SOURCE_FORMAT_IMPORT
    )

    new_type_count = original.count(
        NEW_SOURCE_TYPE_IMPORT
    )

    print(
        "  stale SourceFormat imports :",
        old_format_count,
    )
    print(
        "  stale SourceType imports   :",
        old_type_count,
    )
    print(
        "  canonical SourceFormat imports :",
        new_format_count,
    )
    print(
        "  canonical SourceType imports   :",
        new_type_count,
    )

    # ------------------------------------------------------------------
    # Validate that the stale references are the exact known problem.
    # ------------------------------------------------------------------

    unexpected_domain_acquisition = []

    for line_number, line in enumerate(
        original.splitlines(),
        start=1,
    ):
        if (
            "SanskritAI.domain.acquisition"
            in line
        ):
            unexpected_domain_acquisition.append(
                (line_number, line)
            )

    allowed_stale_lines = {
        OLD_SOURCE_FORMAT_IMPORT,
        OLD_SOURCE_TYPE_IMPORT,
    }

    for line_number, line in unexpected_domain_acquisition:
        if line not in allowed_stale_lines:
            fail(
                "Unexpected SanskritAI.domain.acquisition "
                "reference found in Monier-Williams source:\n"
                f"  line {line_number}: {line}"
            )

    # ------------------------------------------------------------------
    # Repair
    # ------------------------------------------------------------------

    repaired = original

    repaired = repaired.replace(
        OLD_SOURCE_FORMAT_IMPORT,
        NEW_SOURCE_FORMAT_IMPORT,
    )

    repaired = repaired.replace(
        OLD_SOURCE_TYPE_IMPORT,
        NEW_SOURCE_TYPE_IMPORT,
    )

    if repaired != original:
        MONIER_WILLIAMS_FILE.write_text(
            repaired,
            encoding="utf-8",
        )

        print()
        print("Repair applied:")
        print(
            "  domain.acquisition.source_format"
            " -> acquisition.models.source_format"
        )
        print(
            "  domain.acquisition.source_type"
            "   -> acquisition.models.source_type"
        )
    else:
        print()
        print(
            "No textual repair required; "
            "validating existing canonical imports."
        )

    # ------------------------------------------------------------------
    # Static validation
    # ------------------------------------------------------------------

    current = MONIER_WILLIAMS_FILE.read_text(
        encoding="utf-8"
    )

    if OLD_SOURCE_FORMAT_IMPORT in current:
        fail(
            "Stale SourceFormat import remains after repair."
        )

    if OLD_SOURCE_TYPE_IMPORT in current:
        fail(
            "Stale SourceType import remains after repair."
        )

    if "SanskritAI.domain.acquisition" in current:
        fail(
            "Unexpected SanskritAI.domain.acquisition "
            "reference remains in Monier-Williams source."
        )

    validate_ast(MONIER_WILLIAMS_FILE)
    compile_file(MONIER_WILLIAMS_FILE)

    print()
    print("AST validation : PASS")
    print("Compilation     : PASS")

    # ------------------------------------------------------------------
    # Validate canonical acquisition enums directly.
    # ------------------------------------------------------------------

    from SanskritAI.acquisition.models.source_format import (
        SourceFormat,
    )

    from SanskritAI.acquisition.models.source_type import (
        SourceType,
    )

    print()
    print("Canonical acquisition enum imports : PASS")

    if not hasattr(SourceFormat, "TEXT"):
        fail(
            "Canonical SourceFormat.TEXT is missing."
        )

    if not hasattr(SourceType, "CORPUS"):
        fail(
            "Canonical SourceType.CORPUS is missing."
        )

    print("  SourceFormat.TEXT : PASS")
    print("  SourceType.CORPUS : PASS")

    # ------------------------------------------------------------------
    # Validate Monier-Williams import.
    # ------------------------------------------------------------------

    from SanskritAI.acquisition.sources.monier_williams import (
        MonierWilliamsSource,
    )

    mw = MonierWilliamsSource()

    print()
    print("Monier-Williams source import : PASS")
    print(f"  source_id     = {mw.source_id}")
    print(f"  name          = {mw.name}")
    print(f"  source_type   = {mw.source_type}")
    print(f"  source_format = {mw.source_format}")

    if mw.source_type != SourceType.CORPUS:
        fail(
            "MonierWilliamsSource.source_type changed unexpectedly."
        )

    if mw.source_format != SourceFormat.TEXT:
        fail(
            "MonierWilliamsSource.source_format changed unexpectedly."
        )

    print("  source semantics : PASS")

    # ------------------------------------------------------------------
    # Validate package-level import.
    # ------------------------------------------------------------------

    import SanskritAI.acquisition.sources as acquisition_sources

    if not hasattr(
        acquisition_sources,
        "MonierWilliamsSource",
    ):
        fail(
            "acquisition.sources does not expose "
            "MonierWilliamsSource."
        )

    print()
    print("acquisition.sources package import : PASS")

    # ------------------------------------------------------------------
    # Validate Amarakośa source import.
    #
    # This is the critical regression check because the original
    # failure occurred while importing the package before Amarakośa
    # could even be reached.
    # ------------------------------------------------------------------

    from SanskritAI.acquisition.sources.amarakosha import (
        create_amarakosha_source,
    )

    print(
        "Amarakośa source module import : PASS"
    )

    amarakosha_source = create_amarakosha_source()

    print(
        "Amarakośa source construction : PASS"
    )

    if amarakosha_source.source_id != "amarakosha":
        fail(
            "Unexpected Amarakośa source_id."
        )

    print(
        "  Amarakośa source_id :",
        amarakosha_source.source_id,
    )

    # ------------------------------------------------------------------
    # Final result
    # ------------------------------------------------------------------

    print()
    print("=" * 72)
    print(
        "RESULT: PASS — stale Monier-Williams acquisition imports "
        "repaired and Amarakośa source import unblocked."
    )
    print("=" * 72)


if __name__ == "__main__":
    main()
