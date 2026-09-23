from __future__ import annotations

"""
13R-8F-8 — LocalFileImporter canonical source-path repair

Purpose
-------
Move local-source resolution into LocalFileImporter.

Canonical source:
    manifest.source.local_path

Compatibility fallback:
    manifest.metadata["source_path"]

Resolution precedence:
    1. manifest.source.local_path
    2. manifest.metadata["source_path"]
    3. None

Architectural ownership
-----------------------
LocalFileImporter owns local-source normalization.

This repair:
    - does NOT add source_path to AcquisitionManifest
    - does NOT modify CorpusSource
    - does NOT modify Amarakośa source declarations
    - does NOT create an Amarakośa-specific importer
    - preserves the public LocalFileImporter API
    - creates a production backup before modification
    - validates the complete candidate source BEFORE writing production

The repair is intentionally idempotent.

Important
---------
The previous repair script failed because it validated for
_resolve_source_path() without actually inserting that method.

This version explicitly inserts the resolver into the
LocalFileImporter class.
"""

from pathlib import Path
import ast
import shutil
import sys


REPO_ROOT = Path("/content/SanskritAI").resolve()

TARGET = (
    REPO_ROOT
    / "acquisition"
    / "downloaders"
    / "local_file_importer.py"
)

BACKUP = TARGET.with_name(
    TARGET.name + ".bak_13r8f8"
)


# ----------------------------------------------------------------------
# AST helpers
# ----------------------------------------------------------------------

def parse_source(source: str) -> ast.Module:
    return ast.parse(
        source,
        filename=str(TARGET),
    )


def find_class(
    tree: ast.Module,
    class_name: str,
) -> ast.ClassDef:
    for node in tree.body:
        if (
            isinstance(node, ast.ClassDef)
            and node.name == class_name
        ):
            return node

    raise RuntimeError(
        f"Class not found: {class_name}"
    )


def find_method(
    class_node: ast.ClassDef,
    method_name: str,
) -> ast.FunctionDef:
    for node in class_node.body:
        if (
            isinstance(node, ast.FunctionDef)
            and node.name == method_name
        ):
            return node

    raise RuntimeError(
        f"Method not found: {method_name}"
    )


def has_method(
    class_node: ast.ClassDef,
    method_name: str,
) -> bool:
    return any(
        isinstance(node, ast.FunctionDef)
        and node.name == method_name
        for node in class_node.body
    )


# ----------------------------------------------------------------------
# Candidate method bodies
# ----------------------------------------------------------------------

def build_resolver_method() -> str:
    return '''    def _resolve_source_path(
        self,
        manifest: AcquisitionManifest,
    ) -> Path | None:
        """
        Resolve the local source path for this importer.

        Canonical precedence
        --------------------
        1. manifest.source.local_path
        2. manifest.metadata["source_path"] compatibility fallback
        3. None

        The canonical source identity belongs to CorpusSource.
        LocalFileImporter owns the normalization required by
        local filesystem acquisition.
        """
        local_path = getattr(
            manifest.source,
            "local_path",
            None,
        )

        if local_path is not None:
            return Path(local_path)

        metadata_path = manifest.get_metadata(
            "source_path"
        )

        if metadata_path is not None:
            return Path(metadata_path)

        return None

'''


def build_supports_method() -> str:
    return '''    def supports(
        self,
        manifest: AcquisitionManifest,
    ) -> bool:
        """
        Returns True if the manifest specifies a local source.

        Canonical source:
            manifest.source.local_path

        Compatibility fallback:
            manifest.metadata["source_path"]
        """
        return self._resolve_source_path(
            manifest
        ) is not None

'''


def build_download_method() -> str:
    return '''    def download(
        self,
        manifest: AcquisitionManifest,
    ) -> AcquisitionResult:
        """
        Copies a local file or directory into the acquisition
        destination.
        """
        result = AcquisitionResult(
            source=manifest.source
        )

        source_path = self._resolve_source_path(
            manifest
        )

        if source_path is None:
            result.add_error(
                "Manifest does not contain a local source path."
            )
            return self.finalize_result(
                result
            )

        if not source_path.exists():
            result.add_error(
                f"Source does not exist: {source_path}"
            )
            return self.finalize_result(
                result
            )

        if manifest.destination_directory is None:
            result.add_error(
                "Manifest.destination_directory is not configured."
            )
            return self.finalize_result(
                result
            )

        self.validate_destination(
            manifest.destination_directory
        )

        try:
            if source_path.is_file():
                destination = self._copy_file(
                    source_path,
                    manifest,
                )

                result.add_downloaded_file(
                    destination
                )

                try:
                    result.bytes_downloaded = (
                        destination.stat().st_size
                    )
                except OSError:
                    pass

            elif source_path.is_dir():
                copied = self._copy_directory(
                    source_path,
                    manifest,
                )

                for file in copied:
                    result.add_downloaded_file(
                        file
                    )

                    try:
                        result.bytes_downloaded += (
                            file.stat().st_size
                        )
                    except OSError:
                        pass

            else:
                result.add_error(
                    f"Unsupported source: {source_path}"
                )

                return self.finalize_result(
                    result
                )

            result.message = (
                f"Imported local resource: {source_path}"
            )

        except Exception as exc:
            result.add_error(
                str(exc)
            )

        return self.finalize_result(
            result
        )

'''


# ----------------------------------------------------------------------
# Source manipulation
# ----------------------------------------------------------------------

def replace_method_source(
    source: str,
    method_node: ast.FunctionDef,
    replacement: str,
) -> str:
    """
    Replace exactly one method using AST line boundaries.
    """

    lines = source.splitlines(
        keepends=True
    )

    start = method_node.lineno - 1

    if method_node.end_lineno is None:
        raise RuntimeError(
            f"Cannot determine end line for {method_node.name}()."
        )

    end = method_node.end_lineno

    lines[start:end] = [
        replacement
    ]

    return "".join(lines)


def insert_resolver_method(
    source: str,
) -> str:
    """
    Insert _resolve_source_path() into LocalFileImporter.

    Insertion point:
        immediately before the first existing method in the class.

    This preserves the existing helper methods and keeps the
    resolver grouped with the public local-source contract.
    """

    tree = parse_source(source)

    class_node = find_class(
        tree,
        "LocalFileImporter",
    )

    if has_method(
        class_node,
        "_resolve_source_path",
    ):
        return source

    if not class_node.body:
        raise RuntimeError(
            "LocalFileImporter class has no body."
        )

    first_method = None

    for node in class_node.body:
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            first_method = node
            break

    if first_method is None:
        raise RuntimeError(
            "No method found inside LocalFileImporter "
            "for resolver insertion."
        )

    lines = source.splitlines(
        keepends=True
    )

    insertion_index = first_method.lineno - 1

    lines[insertion_index:insertion_index] = [
        build_resolver_method()
    ]

    return "".join(lines)


def replace_supports_and_download(
    source: str,
) -> str:
    """
    Replace supports() and download() after the resolver
    has been inserted.
    """

    tree = parse_source(source)

    class_node = find_class(
        tree,
        "LocalFileImporter",
    )

    supports_node = find_method(
        class_node,
        "supports",
    )

    download_node = find_method(
        class_node,
        "download",
    )

    replacements = [
        (
            supports_node.lineno - 1,
            supports_node.end_lineno,
            build_supports_method(),
        ),
        (
            download_node.lineno - 1,
            download_node.end_lineno,
            build_download_method(),
        ),
    ]

    lines = source.splitlines(
        keepends=True
    )

    for start, end, replacement in sorted(
        replacements,
        key=lambda item: item[0],
        reverse=True,
    ):
        if end is None:
            raise RuntimeError(
                "Cannot determine method end line."
            )

        lines[start:end] = [
            replacement
        ]

    return "".join(lines)


def build_updated_source(
    original: str,
) -> str:
    """
    Build the complete candidate production source.

    Order is deliberate:

        original
          ↓
        insert resolver
          ↓
        replace supports/download
          ↓
        structural validation
          ↓
        write production
    """

    updated = insert_resolver_method(
        original
    )

    updated = replace_supports_and_download(
        updated
    )

    return updated


# ----------------------------------------------------------------------
# Structural validation
# ----------------------------------------------------------------------

def verify_updated_contract(
    source: str,
) -> None:
    """
    Verify the complete LocalFileImporter contract.
    """

    tree = parse_source(source)

    class_node = find_class(
        tree,
        "LocalFileImporter",
    )

    resolver = find_method(
        class_node,
        "_resolve_source_path",
    )

    supports = find_method(
        class_node,
        "supports",
    )

    download = find_method(
        class_node,
        "download",
    )

    resolver_source = ast.get_source_segment(
        source,
        resolver,
    )

    if resolver_source is None:
        raise RuntimeError(
            "Unable to inspect _resolve_source_path()."
        )

    # --------------------------------------------------------------
    # Resolver canonical path
    # --------------------------------------------------------------

    if "manifest.source" not in resolver_source:
        raise RuntimeError(
            "_resolve_source_path() does not inspect "
            "manifest.source."
        )

    if "local_path" not in resolver_source:
        raise RuntimeError(
            "_resolve_source_path() does not inspect "
            "CorpusSource.local_path."
        )

    # --------------------------------------------------------------
    # Resolver compatibility path
    # --------------------------------------------------------------

    if 'get_metadata(\n            "source_path"\n        )' not in resolver_source:
        if 'get_metadata("source_path")' not in resolver_source:
            raise RuntimeError(
                "_resolve_source_path() does not preserve "
                "metadata['source_path'] compatibility fallback."
            )

    # --------------------------------------------------------------
    # supports()
    # --------------------------------------------------------------

    supports_source = ast.get_source_segment(
        source,
        supports,
    )

    if supports_source is None:
        raise RuntimeError(
            "Unable to inspect supports()."
        )

    if "_resolve_source_path" not in supports_source:
        raise RuntimeError(
            "supports() does not use "
            "_resolve_source_path()."
        )

    if "get_metadata" in supports_source:
        raise RuntimeError(
            "supports() still performs direct metadata "
            "source-path resolution."
        )

    if ".local_path" in supports_source:
        raise RuntimeError(
            "supports() still performs direct CorpusSource "
            "local_path resolution instead of using the resolver."
        )

    # --------------------------------------------------------------
    # download()
    # --------------------------------------------------------------

    download_source = ast.get_source_segment(
        source,
        download,
    )

    if download_source is None:
        raise RuntimeError(
            "Unable to inspect download()."
        )

    if "_resolve_source_path" not in download_source:
        raise RuntimeError(
            "download() does not use "
            "_resolve_source_path()."
        )

    if "get_metadata" in download_source:
        raise RuntimeError(
            "download() still performs direct metadata "
            "source-path resolution."
        )

    if ".local_path" in download_source:
        raise RuntimeError(
            "download() still performs direct CorpusSource "
            "local_path resolution instead of using the resolver."
        )

    # --------------------------------------------------------------
    # No duplicate resolver
    # --------------------------------------------------------------

    resolver_count = sum(
        1
        for node in class_node.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "_resolve_source_path"
    )

    if resolver_count != 1:
        raise RuntimeError(
            "_resolve_source_path() count is "
            f"{resolver_count}; expected exactly 1."
        )

    print(
        "Updated LocalFileImporter structural contract: PASS"
    )


# ----------------------------------------------------------------------
# Runtime validation
# ----------------------------------------------------------------------

def runtime_contract_check() -> None:
    """
    Import the modified production class and verify that
    the canonical resolver exists at runtime.
    """

    module_name = (
        "SanskritAI.acquisition.downloaders.local_file_importer"
    )

    sys.modules.pop(
        module_name,
        None,
    )

    from SanskritAI.acquisition.downloaders.local_file_importer import (
        LocalFileImporter,
    )

    if not hasattr(
        LocalFileImporter,
        "_resolve_source_path",
    ):
        raise RuntimeError(
            "Runtime LocalFileImporter does not expose "
            "_resolve_source_path()."
        )

    print(
        "Runtime LocalFileImporter import: PASS"
    )

    print(
        "Runtime canonical resolver: PASS"
    )


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> None:
    print("=" * 72)
    print(
        "13R-8F-8 — LocalFileImporter canonical path repair"
    )
    print("=" * 72)

    if not TARGET.exists():
        raise FileNotFoundError(
            f"Production target not found: {TARGET}"
        )

    original = TARGET.read_text(
        encoding="utf-8"
    )

    # --------------------------------------------------------------
    # Existing syntax
    # --------------------------------------------------------------

    parse_source(original)

    print(
        "Existing production Python syntax: PASS"
    )

    # --------------------------------------------------------------
    # Idempotent already-repaired path
    # --------------------------------------------------------------

    tree = parse_source(original)

    class_node = find_class(
        tree,
        "LocalFileImporter",
    )

    if has_method(
        class_node,
        "_resolve_source_path",
    ):
        print()
        print(
            "Canonical resolver already exists."
        )
        print(
            "Running structural validation instead of "
            "modifying production."
        )

        verify_updated_contract(
            original
        )

        runtime_contract_check()

        print()
        print(
            "13R-8F-8 COMPLETE — already repaired"
        )

        return

    # --------------------------------------------------------------
    # Backup
    # --------------------------------------------------------------

    if BACKUP.exists():
        print(
            f"Backup already exists: {BACKUP}"
        )
    else:
        shutil.copy2(
            TARGET,
            BACKUP,
        )

        print(
            f"Production backup created: {BACKUP}"
        )

    # --------------------------------------------------------------
    # Build candidate
    # --------------------------------------------------------------

    updated = build_updated_source(
        original
    )

    # --------------------------------------------------------------
    # Candidate syntax validation
    # --------------------------------------------------------------

    parse_source(updated)

    print(
        "Candidate source Python syntax: PASS"
    )

    # --------------------------------------------------------------
    # Candidate structural validation
    # --------------------------------------------------------------

    verify_updated_contract(
        updated
    )

    # --------------------------------------------------------------
    # Write production only after all validation passes
    # --------------------------------------------------------------

    TARGET.write_text(
        updated,
        encoding="utf-8",
    )

    print()
    print(
        "Production file updated:"
    )
    print(
        f"  {TARGET}"
    )

    # --------------------------------------------------------------
    # Validate actual written production file
    # --------------------------------------------------------------

    written = TARGET.read_text(
        encoding="utf-8"
    )

    parse_source(written)

    print(
        "Written-file Python syntax: PASS"
    )

    verify_updated_contract(
        written
    )

    # --------------------------------------------------------------
    # Runtime validation
    # --------------------------------------------------------------

    runtime_contract_check()

    # --------------------------------------------------------------
    # Architectural report
    # --------------------------------------------------------------

    print()
    print(
        "Canonical local-source resolution:"
    )
    print(
        "  1. manifest.source.local_path"
    )
    print(
        "  2. manifest.metadata['source_path']"
    )
    print(
        "  3. None"
    )

    print()
    print(
        "Normalization owner: LocalFileImporter"
    )
    print(
        "AcquisitionManifest schema changed: NO"
    )
    print(
        "CorpusSource schema changed: NO"
    )
    print(
        "Amarakośa-specific importer created: NO"
    )
    print(
        "DefaultSourceAcquirer path-resolution logic added: NO"
    )

    print()
    print(
        "13R-8F-8 COMPLETE"
    )


if __name__ == "__main__":
    main()
