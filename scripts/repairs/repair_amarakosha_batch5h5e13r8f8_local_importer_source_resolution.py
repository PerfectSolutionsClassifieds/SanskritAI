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
    - uses AST-aware validation
    - recognizes both direct and getattr-based canonical local_path access
    - bootstraps /content for runtime SanskritAI imports

The repair is intentionally idempotent.

Important
---------
The production repository is:

    /content/SanskritAI

The Python package import is:

    SanskritAI

Therefore runtime validation must have:

    /content

on sys.path, not merely:

    /content/SanskritAI
"""


from pathlib import Path
import ast
import shutil
import sys


# ----------------------------------------------------------------------
# Repository / workspace paths
# ----------------------------------------------------------------------

REPO_ROOT = Path(
    "/content/SanskritAI"
).resolve()

WORKSPACE_ROOT = REPO_ROOT.parent

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
# Runtime import bootstrap
# ----------------------------------------------------------------------

def bootstrap_runtime_import_path() -> None:
    """
    Make the SanskritAI package importable during direct script
    execution.

    Repository:
        /content/SanskritAI

    Python package:
        SanskritAI

    Required sys.path entry:
        /content
    """

    workspace = str(
        WORKSPACE_ROOT
    )

    if workspace not in sys.path:
        sys.path.insert(
            0,
            workspace,
        )

    if workspace not in sys.path:
        raise RuntimeError(
            "Failed to bootstrap workspace root "
            f"into sys.path: {workspace}"
        )


# ----------------------------------------------------------------------
# AST helpers
# ----------------------------------------------------------------------

def parse_source(
    source: str,
) -> ast.Module:
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
            isinstance(
                node,
                ast.ClassDef,
            )
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
            isinstance(
                node,
                ast.FunctionDef,
            )
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
        isinstance(
            node,
            ast.FunctionDef,
        )
        and node.name == method_name
        for node in class_node.body
    )


def executable_body(
    method_node: ast.FunctionDef,
) -> list[ast.stmt]:
    """
    Return executable statements while excluding a leading
    method docstring.
    """

    body = list(
        method_node.body
    )

    if (
        body
        and isinstance(
            body[0],
            ast.Expr,
        )
        and isinstance(
            body[0].value,
            ast.Constant,
        )
        and isinstance(
            body[0].value.value,
            str,
        )
    ):
        body = body[1:]

    return body


def executable_nodes(
    method_node: ast.FunctionDef,
):
    """
    Yield AST nodes from executable method statements only.
    """

    for statement in executable_body(
        method_node
    ):
        yield from ast.walk(
            statement
        )


# ----------------------------------------------------------------------
# Semantic AST predicates
# ----------------------------------------------------------------------

def is_manifest_source_expression(
    node: ast.AST,
) -> bool:
    """
    Return True when an AST node represents:

        manifest.source
    """

    return (
        isinstance(
            node,
            ast.Attribute,
        )
        and node.attr == "source"
        and isinstance(
            node.value,
            ast.Name,
        )
        and node.value.id == "manifest"
    )


def is_getattr_local_path_call(
    node: ast.AST,
) -> bool:
    """
    Return True when an AST Call represents:

        getattr(
            manifest.source,
            "local_path",
            ...
        )
    """

    if not isinstance(
        node,
        ast.Call,
    ):
        return False

    if not (
        isinstance(
            node.func,
            ast.Name,
        )
        and node.func.id == "getattr"
    ):
        return False

    if len(node.args) < 2:
        return False

    source_argument = node.args[0]

    local_path_argument = node.args[1]

    if not is_manifest_source_expression(
        source_argument
    ):
        return False

    return (
        isinstance(
            local_path_argument,
            ast.Constant,
        )
        and local_path_argument.value
        == "local_path"
    )


def canonical_local_path_resolution_exists(
    method_node: ast.FunctionDef,
) -> bool:
    """
    Detect either canonical executable form:

        manifest.source.local_path

    OR:

        getattr(
            manifest.source,
            "local_path",
            None,
        )
    """

    for node in executable_nodes(
        method_node
    ):
        if (
            isinstance(
                node,
                ast.Attribute,
            )
            and node.attr == "local_path"
            and is_manifest_source_expression(
                node.value
            )
        ):
            return True

        if is_getattr_local_path_call(
            node
        ):
            return True

    return False


def direct_local_path_access_exists(
    method_node: ast.FunctionDef,
) -> bool:
    """
    Detect direct executable:

        manifest.source.local_path

    Documentation strings are excluded.

    getattr(manifest.source, "local_path", None)
    is NOT considered direct access because it is the intended
    canonical resolver implementation.
    """

    for node in executable_nodes(
        method_node
    ):
        if (
            isinstance(
                node,
                ast.Attribute,
            )
            and node.attr == "local_path"
            and is_manifest_source_expression(
                node.value
            )
        ):
            return True

    return False


def direct_get_metadata_source_path_exists(
    method_node: ast.FunctionDef,
) -> bool:
    """
    Detect executable:

        manifest.get_metadata("source_path")

    Documentation strings are excluded.
    """

    for node in executable_nodes(
        method_node
    ):
        if not isinstance(
            node,
            ast.Call,
        ):
            continue

        if not isinstance(
            node.func,
            ast.Attribute,
        ):
            continue

        if node.func.attr != "get_metadata":
            continue

        if len(node.args) != 1:
            continue

        argument = node.args[0]

        if (
            isinstance(
                argument,
                ast.Constant,
            )
            and argument.value
            == "source_path"
        ):
            return True

    return False


def resolver_call_exists(
    method_node: ast.FunctionDef,
) -> bool:
    """
    Verify executable call to:

        self._resolve_source_path(manifest)
    """

    for node in executable_nodes(
        method_node
    ):
        if not isinstance(
            node,
            ast.Call,
        ):
            continue

        if not isinstance(
            node.func,
            ast.Attribute,
        ):
            continue

        if node.func.attr != "_resolve_source_path":
            continue

        return True

    return False


# ----------------------------------------------------------------------
# Candidate method source
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
# Candidate source construction
# ----------------------------------------------------------------------

def insert_resolver_method(
    source: str,
) -> str:
    """
    Insert _resolve_source_path() before the first existing
    method in LocalFileImporter.
    """

    tree = parse_source(
        source
    )

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

    insertion_index = (
        first_method.lineno - 1
    )

    lines[
        insertion_index:insertion_index
    ] = [
        build_resolver_method()
    ]

    return "".join(
        lines
    )


def replace_methods(
    source: str,
) -> str:
    """
    Replace supports() and download() using AST line boundaries.

    Replacements occur from bottom to top.
    """

    tree = parse_source(
        source
    )

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

    lines = source.splitlines(
        keepends=True
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

    for (
        start,
        end,
        replacement,
    ) in sorted(
        replacements,
        key=lambda item: item[0],
        reverse=True,
    ):
        if end is None:
            raise RuntimeError(
                "Cannot determine method end line."
            )

        lines[
            start:end
        ] = [
            replacement
        ]

    return "".join(
        lines
    )


def build_updated_source(
    original: str,
) -> str:
    """
    Build candidate production source.
    """

    updated = insert_resolver_method(
        original
    )

    updated = replace_methods(
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

    All behavioral checks are performed on executable AST nodes.
    """

    tree = parse_source(
        source
    )

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

    # --------------------------------------------------------------
    # Resolver canonical source
    # --------------------------------------------------------------

    if not canonical_local_path_resolution_exists(
        resolver
    ):
        raise RuntimeError(
            "_resolve_source_path() does not inspect "
            "CorpusSource.local_path."
        )

    print(
        "Resolver canonical CorpusSource.local_path access: PASS"
    )

    # --------------------------------------------------------------
    # Resolver compatibility fallback
    # --------------------------------------------------------------

    if not direct_get_metadata_source_path_exists(
        resolver
    ):
        raise RuntimeError(
            "_resolve_source_path() does not preserve "
            "manifest.metadata['source_path'] compatibility fallback."
        )

    print(
        "Resolver metadata['source_path'] compatibility fallback: PASS"
    )

    # --------------------------------------------------------------
    # supports()
    # --------------------------------------------------------------

    if not resolver_call_exists(
        supports
    ):
        raise RuntimeError(
            "supports() does not call "
            "_resolve_source_path()."
        )

    if direct_local_path_access_exists(
        supports
    ):
        raise RuntimeError(
            "supports() performs direct executable "
            "CorpusSource.local_path resolution instead "
            "of using _resolve_source_path()."
        )

    if direct_get_metadata_source_path_exists(
        supports
    ):
        raise RuntimeError(
            "supports() performs direct executable "
            "metadata source-path resolution instead "
            "of using _resolve_source_path()."
        )

    print(
        "supports() resolver delegation: PASS"
    )

    # --------------------------------------------------------------
    # download()
    # --------------------------------------------------------------

    if not resolver_call_exists(
        download
    ):
        raise RuntimeError(
            "download() does not call "
            "_resolve_source_path()."
        )

    if direct_local_path_access_exists(
        download
    ):
        raise RuntimeError(
            "download() performs direct executable "
            "CorpusSource.local_path resolution instead "
            "of using _resolve_source_path()."
        )

    if direct_get_metadata_source_path_exists(
        download
    ):
        raise RuntimeError(
            "download() performs direct executable "
            "metadata source-path resolution instead "
            "of using _resolve_source_path()."
        )

    print(
        "download() resolver delegation: PASS"
    )

    # --------------------------------------------------------------
    # Exactly one resolver
    # --------------------------------------------------------------

    resolver_count = sum(
        1
        for node in class_node.body
        if isinstance(
            node,
            ast.FunctionDef,
        )
        and node.name
        == "_resolve_source_path"
    )

    if resolver_count != 1:
        raise RuntimeError(
            "_resolve_source_path() count is "
            f"{resolver_count}; expected exactly 1."
        )

    print(
        "Exactly one _resolve_source_path(): PASS"
    )

    print(
        "Updated LocalFileImporter structural contract: PASS"
    )


# ----------------------------------------------------------------------
# Runtime validation
# ----------------------------------------------------------------------

def runtime_contract_check() -> None:
    """
    Import the modified production class.

    Direct script execution does not automatically place
    /content on sys.path. The SanskritAI package lives at:

        /content/SanskritAI

    Therefore Python must search:

        /content

    for:

        SanskritAI
    """

    # --------------------------------------------------------------
    # Bootstrap package import root
    # --------------------------------------------------------------

    bootstrap_runtime_import_path()

    print(
        "Runtime workspace import path bootstrap: PASS"
    )

    print(
        f"  workspace root: {WORKSPACE_ROOT}"
    )

    print(
        f"  package root:   {REPO_ROOT}"
    )

    # --------------------------------------------------------------
    # Remove cached module
    # --------------------------------------------------------------

    module_name = (
        "SanskritAI.acquisition.downloaders.local_file_importer"
    )

    sys.modules.pop(
        module_name,
        None,
    )

    # --------------------------------------------------------------
    # Runtime import
    # --------------------------------------------------------------

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

    parse_source(
        original
    )

    print(
        "Existing production Python syntax: PASS"
    )

    # --------------------------------------------------------------
    # Idempotency
    # --------------------------------------------------------------

    original_tree = parse_source(
        original
    )

    original_class = find_class(
        original_tree,
        "LocalFileImporter",
    )

    if has_method(
        original_class,
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
    # Candidate construction
    # --------------------------------------------------------------

    updated = build_updated_source(
        original
    )

    # --------------------------------------------------------------
    # Candidate syntax
    # --------------------------------------------------------------

    parse_source(
        updated
    )

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
    # Write only after validation
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
    # Written-file validation
    # --------------------------------------------------------------

    written = TARGET.read_text(
        encoding="utf-8"
    )

    parse_source(
        written
    )

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
