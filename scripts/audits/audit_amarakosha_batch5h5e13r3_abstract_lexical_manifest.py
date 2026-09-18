
from __future__ import annotations

"""
BATCH 5H-5E-13R-3
=================

AMARAKOSHA ABSTRACT LEXICAL MANIFEST AUDIT

Purpose
-------
Determine whether the existing abstract lexical manifest boundary
is sufficient for Amarakośa acquisition.

Read-only audit.

No production mutation.
No new classes.
No enum changes.
"""

from pathlib import Path
import inspect
import sys

PROJECT_ROOT = Path("/content/SanskritAI")


def section(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def fail(message: str) -> None:
    raise RuntimeError(message)


def show_class(cls, label: str) -> None:
    print()
    print(f"{label}")
    print(f"Class       : {cls}")
    print(f"Module      : {cls.__module__}")
    print(f"Name        : {cls.__name__}")
    print(f"Docstring   :")
    print(inspect.getdoc(cls) or "<none>")

    print()
    print("Constructor:")
    try:
        print(inspect.signature(cls))
    except Exception as exc:
        print(f"<unavailable: {exc}>")


def show_members(cls) -> None:
    print()
    print("Members:")

    for name, value in inspect.getmembers(cls):
        if name.startswith("__"):
            continue

        if inspect.isfunction(value) or inspect.ismethod(value):
            try:
                signature = inspect.signature(value)
            except Exception:
                signature = "<signature unavailable>"

            print(
                f"  method {name}{signature}"
            )

        elif isinstance(value, property):
            print(
                f"  property {name}"
            )


def main() -> None:

    section(
        "BATCH 5H-5E-13R-3 — "
        "AMARAKOSHA ABSTRACT LEXICAL MANIFEST AUDIT"
    )

    if not PROJECT_ROOT.exists():
        fail(
            f"Project root does not exist: {PROJECT_ROOT}"
        )

    parent = str(PROJECT_ROOT.parent)

    if parent not in sys.path:
        sys.path.insert(0, parent)

    section("1. PACKAGE BOOTSTRAP")

    import SanskritAI

    print(
        f"SanskritAI import : PASS ({SanskritAI.__name__})"
    )

    section("2. ABSTRACT LEXICAL MANIFEST IMPORT")

    from SanskritAI.acquisition.knowledge.abstract_lexical_manifest import (
        AbstractLexicalManifest,
    )

    print(
        "AbstractLexicalManifest import : PASS"
    )

    show_class(
        AbstractLexicalManifest,
        "AbstractLexicalManifest",
    )

    show_members(
        AbstractLexicalManifest,
    )

    section("3. ABSTRACT LEXICAL MANIFEST SOURCE")

    manifest_path = (
        PROJECT_ROOT
        / "acquisition"
        / "knowledge"
        / "abstract_lexical_manifest.py"
    )

    print(
        f"Path : {manifest_path}"
    )

    if not manifest_path.exists():
        fail(
            "abstract_lexical_manifest.py not found."
        )

    print(
        manifest_path.read_text(
            encoding="utf-8"
        )
    )

    section("4. AMARAKOSHA REFERENCES IN MANIFEST MODULE")

    source = manifest_path.read_text(
        encoding="utf-8"
    )

    lines = source.splitlines()

    matches = []

    for number, line in enumerate(
        lines,
        start=1,
    ):
        if "amarakosha" in line.lower():
            matches.append(
                (number, line)
            )

    print(
        f"Amarakośa references : {len(matches)}"
    )

    for number, line in matches:
        print(
            f"  {number}: {line}"
        )

    section("5. ABSTRACT MANIFEST SUBCLASS DISCOVERY")

    subclasses = []

    def walk(cls):
        for subclass in cls.__subclasses__():
            subclasses.append(subclass)
            walk(subclass)

    walk(AbstractLexicalManifest)

    print(
        f"Concrete/in-memory subclasses currently visible : "
        f"{len(subclasses)}"
    )

    for subclass in subclasses:
        print(
            f"  {subclass.__module__}.{subclass.__name__}"
        )

    section("6. ACQUISITION MANIFEST COMPARISON")

    from SanskritAI.acquisition.models.acquisition_manifest import (
        AcquisitionManifest,
    )

    print(
        "AcquisitionManifest import : PASS"
    )

    show_class(
        AcquisitionManifest,
        "AcquisitionManifest",
    )

    show_members(
        AcquisitionManifest,
    )

    section("7. MANIFEST RELATIONSHIP")

    abstract_fields = set(
        getattr(
            AbstractLexicalManifest,
            "__annotations__",
            {},
        ).keys()
    )

    acquisition_fields = set(
        getattr(
            AcquisitionManifest,
            "__annotations__",
            {},
        ).keys()
    )

    print(
        "AbstractLexicalManifest annotations:"
    )

    for field in sorted(abstract_fields):
        print(
            f"  {field}"
        )

    print()
    print(
        "AcquisitionManifest annotations:"
    )

    for field in sorted(acquisition_fields):
        print(
            f"  {field}"
        )

    print()
    print(
        "Fields shared:"
    )

    for field in sorted(
        abstract_fields & acquisition_fields
    ):
        print(
            f"  {field}"
        )

    print()
    print(
        "Abstract-only fields:"
    )

    for field in sorted(
        abstract_fields - acquisition_fields
    ):
        print(
            f"  {field}"
        )

    print()
    print(
        "Acquisition-only fields:"
    )

    for field in sorted(
        acquisition_fields - abstract_fields
    ):
        print(
            f"  {field}"
        )

    section("8. REPAIR DECISION")

    print(
        "NO PRODUCTION REPAIR."
    )

    print(
        "No AmarakoshaManifest class created."
    )

    print(
        "No AcquisitionManifest changes."
    )

    print(
        "No AbstractLexicalManifest changes."
    )

    section("9. FINAL RESULT")

    print(
        "BATCH 5H-5E-13R-3 — RESULT: PASS"
    )

    print(
        "Abstract lexical manifest boundary has been "
        "inspected without mutation."
    )

    print(
        "Next step: compare generic acquisition "
        "manifest/provider/acquirer contracts."
    )


if __name__ == "__main__":
    main()
