from __future__ import annotations

"""
13R-8F-6 — LocalFileImporter canonical source-path resolution audit

Purpose
-------
Audit the current LocalFileImporter source-path contract before making
the minimal canonical-path repair.

Canonical candidate
-------------------
    manifest.source.local_path

Compatibility candidate
-----------------------
    manifest.metadata["source_path"]

This script is READ-ONLY.

It does not:
    - modify production Python files
    - modify manifests
    - modify CorpusSource objects
    - modify Amarakośa artifacts
    - create new production abstractions
"""

from pathlib import Path
import ast
import inspect
import sys


REPO_ROOT = Path("/content/SanskritAI").resolve()
WORKSPACE_ROOT = REPO_ROOT.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))


TARGET = (
    REPO_ROOT
    / "acquisition"
    / "downloaders"
    / "local_file_importer.py"
)


def read_source() -> str:
    if not TARGET.exists():
        raise FileNotFoundError(
            f"Target file not found: {TARGET}"
        )

    return TARGET.read_text(encoding="utf-8")


def inspect_ast(source: str) -> ast.Module:
    return ast.parse(
        source,
        filename=str(TARGET),
    )


def find_class(
    tree: ast.Module,
    name: str,
) -> ast.ClassDef:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node

    raise AssertionError(
        f"Class not found: {name}"
    )


def find_method(
    cls: ast.ClassDef,
    name: str,
) -> ast.FunctionDef:
    for node in cls.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node

    raise AssertionError(
        f"Method not found: {name}"
    )


def contains_text(
    source: str,
    text: str,
) -> bool:
    return text in source


def main() -> None:
    print("=" * 72)
    print("13R-8F-6 — LocalFileImporter source-path resolution audit")
    print("=" * 72)

    print(f"Repository: {REPO_ROOT}")
    print(f"Target:     {TARGET}")
    print()

    source = read_source()

    # ---------------------------------------------------------------
    # Syntax
    # ---------------------------------------------------------------

    tree = inspect_ast(source)

    print("Python syntax: PASS")

    # ---------------------------------------------------------------
    # Class / methods
    # ---------------------------------------------------------------

    cls = find_class(
        tree,
        "LocalFileImporter",
    )

    supports_method = find_method(
        cls,
        "supports",
    )

    download_method = find_method(
        cls,
        "download",
    )

    print("LocalFileImporter class: PASS")
    print("supports() method: PASS")
    print("download() method: PASS")
    print()

    # ---------------------------------------------------------------
    # Current metadata contract
    # ---------------------------------------------------------------

    metadata_path_refs = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "get_metadata"
    ]

    print(
        "get_metadata() calls:",
        len(metadata_path_refs),
    )

    source_path_metadata_refs = 0

    for node in metadata_path_refs:
        if (
            len(node.args) >= 1
            and isinstance(node.args[0], ast.Constant)
            and node.args[0].value == "source_path"
        ):
            source_path_metadata_refs += 1

    print(
        "manifest.metadata['source_path'] references:",
        source_path_metadata_refs,
    )

    # ---------------------------------------------------------------
    # Canonical source.local_path references
    # ---------------------------------------------------------------

    source_local_path_refs = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            if node.attr == "local_path":
                source_local_path_refs.append(node)

    print(
        "local_path attribute references:",
        len(source_local_path_refs),
    )

    print()

    # ---------------------------------------------------------------
    # Textual confirmation
    # ---------------------------------------------------------------

    print(
        "Current supports() metadata lookup:",
        "PASS"
        if 'get_metadata("source_path")' in source
        else "NOT FOUND",
    )

    print(
        "Current download() metadata lookup:",
        "PASS"
        if source.count('get_metadata("source_path")') >= 2
        else "NOT FOUND",
    )

    print(
        "CorpusSource.local_path used by LocalFileImporter:",
        "YES"
        if ".local_path" in source
        else "NO",
    )

    print()

    # ---------------------------------------------------------------
    # Runtime imports
    # ---------------------------------------------------------------

    from SanskritAI.acquisition.downloaders.local_file_importer import (
        LocalFileImporter,
    )
    from SanskritAI.acquisition.models.acquisition_manifest import (
        AcquisitionManifest,
    )
    from SanskritAI.acquisition.models.corpus_source import (
        CorpusSource,
    )

    print("Runtime imports: PASS")

    # ---------------------------------------------------------------
    # Signature inspection
    # ---------------------------------------------------------------

    print()
    print("Public contract:")
    print(
        "  supports:",
        inspect.signature(LocalFileImporter.supports),
    )
    print(
        "  download:",
        inspect.signature(LocalFileImporter.download),
    )

    print()

    # ---------------------------------------------------------------
    # Canonical source model inspection
    # ---------------------------------------------------------------

    corpus_fields = getattr(
        CorpusSource,
        "__dataclass_fields__",
        {},
    )

    print(
        "CorpusSource.local_path field:",
        "PASS"
        if "local_path" in corpus_fields
        else "MISSING",
    )

    manifest_fields = getattr(
        AcquisitionManifest,
        "__dataclass_fields__",
        {},
    )

    print(
        "AcquisitionManifest.source field:",
        "PASS"
        if "source" in manifest_fields
        else "MISSING",
    )

    print()

    # ---------------------------------------------------------------
    # Architectural conclusion
    # ---------------------------------------------------------------

    if (
        source_path_metadata_refs >= 2
        and len(source_local_path_refs) == 0
    ):
        print(
            "RESULT:"
        )
        print(
            "PASS — LocalFileImporter currently uses "
            "manifest.metadata['source_path'] as its "
            "effective local-source contract."
        )
        print()
        print(
            "RECOMMENDATION:"
        )
        print(
            "Introduce canonical resolution inside "
            "LocalFileImporter."
        )
        print()
        print(
            "Canonical precedence:"
        )
        print(
            "  1. manifest.source.local_path"
        )
        print(
            "  2. manifest.metadata['source_path'] "
            "(compatibility fallback)"
        )
        print(
            "  3. no local source"
        )
    else:
        print("RESULT:")
        print(
            "REVIEW — Current LocalFileImporter contract "
            "does not exactly match the expected "
            "metadata-only baseline."
        )

    print()
    print(
        "13R-8F-6 COMPLETE"
    )


if __name__ == "__main__":
    main()
