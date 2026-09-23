from __future__ import annotations

"""
13R-8F-13 — Local Registration Semantic Contract Audit

Purpose
-------
Determine the exact semantic contract required to repair local artifact
registration at the DefaultSourceAcquirer boundary.

This audit is READ-ONLY.

It does NOT modify:
    DefaultSourceAcquirer
    LocalFileImporter
    CorpusSource
    AcquisitionManifest
    SourceStatus

Architectural intent
--------------------
A canonical local artifact already registered through:

    CorpusSource.local_path

must not be physically copied onto itself.

The audit distinguishes:

    LOCAL REGISTRATION
        from
    LOCAL PHYSICAL ACQUISITION

Existing architecture
---------------------
CorpusSource.local_path
LocalFileImporter
DefaultSourceAcquirer
AcquisitionResult
SourceStatus

No new importer or SourceStatus should be introduced.
"""

# from __future__ import annotations

import ast
import hashlib
import inspect
import sys
import textwrap
from pathlib import Path
from dataclasses import replace


REPO_ROOT = Path("/content/SanskritAI").resolve()
WORKSPACE_ROOT = REPO_ROOT.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))


ACQUIRER_FILE = (
    REPO_ROOT
    / "acquisition"
    / "acquirers"
    / "default_source_acquirer.py"
)

IMPORTER_FILE = (
    REPO_ROOT
    / "acquisition"
    / "downloaders"
    / "local_file_importer.py"
)

SOURCE_FILE = (
    REPO_ROOT
    / "acquisition"
    / "models"
    / "corpus_source.py"
)

MANIFEST_FILE = (
    REPO_ROOT
    / "acquisition"
    / "models"
    / "acquisition_manifest.py"
)

RESULT_FILE = (
    REPO_ROOT
    / "acquisition"
    / "models"
    / "acquisition_result.py"
)

STATUS_FILE = (
    REPO_ROOT
    / "acquisition"
    / "models"
    / "source_status.py"
)

AMARAKOSHA_SOURCE_FILE = (
    REPO_ROOT
    / "acquisition"
    / "sources"
    / "amarakosha.py"
)

AMARAKOSHA_MANIFEST_FILE = (
    REPO_ROOT
    / "acquisition"
    / "sources"
    / "amarakosha_manifest.py"
)

ARTIFACT = REPO_ROOT / "amarakosha.txt"

EXPECTED_SIZE = 645456

EXPECTED_SHA256 = (
    "d82a5234e4bc15ef295b1b375a6548e02df9a10d6eb94e0f97223289c46c3190"
)


def banner(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def syntax_check(path: Path) -> bool:
    try:
        ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
        print(f"{path}: Python syntax PASS")
        return True
    except Exception as exc:
        print(f"{path}: Python syntax FAIL")
        print(f"  {type(exc).__name__}: {exc}")
        return False


def sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def parse_module(path: Path) -> ast.Module:
    return ast.parse(
        path.read_text(encoding="utf-8"),
        filename=str(path),
    )


def find_class(
    tree: ast.Module,
    class_name: str,
) -> ast.ClassDef | None:
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            if node.name == class_name:
                return node

    return None


def find_method(
    class_node: ast.ClassDef | None,
    method_name: str,
) -> ast.FunctionDef | ast.AsyncFunctionDef | None:

    if class_node is None:
        return None

    for node in class_node.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == method_name:
                return node

    return None


def source_segment(
    source: str,
    node: ast.AST,
) -> str:

    segment = ast.get_source_segment(source, node)

    if segment is None:
        return ""

    return textwrap.dedent(segment)


def call_names(node: ast.AST) -> list[str]:
    names: list[str] = []

    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue

        function = child.func

        if isinstance(function, ast.Name):
            names.append(function.id)

        elif isinstance(function, ast.Attribute):
            names.append(function.attr)

    return names


def attribute_names(node: ast.AST) -> list[str]:
    names: list[str] = []

    for child in ast.walk(node):
        if isinstance(child, ast.Attribute):
            names.append(child.attr)

    return names


def find_calls(
    method: ast.AST,
    target: str,
) -> list[tuple[int, str]]:

    matches: list[tuple[int, str]] = []

    for node in ast.walk(method):
        if not isinstance(node, ast.Call):
            continue

        function = node.func

        if isinstance(function, ast.Name):
            if function.id == target:
                matches.append(
                    (
                        node.lineno,
                        ast.unparse(node),
                    )
                )

        elif isinstance(function, ast.Attribute):
            if function.attr == target:
                matches.append(
                    (
                        node.lineno,
                        ast.unparse(node),
                    )
                )

    return sorted(matches)


def find_returns_of_call(
    method: ast.AST,
    target: str,
) -> list[tuple[int, str]]:

    matches: list[tuple[int, str]] = []

    for node in ast.walk(method):
        if not isinstance(node, ast.Return):
            continue

        value = node.value

        if isinstance(value, ast.Call):
            function = value.func

            if isinstance(function, ast.Attribute):
                if function.attr == target:
                    matches.append(
                        (
                            node.lineno,
                            ast.unparse(value),
                        )
                    )

            elif isinstance(function, ast.Name):
                if function.id == target:
                    matches.append(
                        (
                            node.lineno,
                            ast.unparse(value),
                        )
                    )

    return matches


def find_conditions_containing(
    method: ast.AST,
    marker: str,
) -> list[tuple[int, str]]:

    matches: list[tuple[int, str]] = []

    for node in ast.walk(method):
        if not isinstance(node, ast.If):
            continue

        condition = ast.unparse(node.test)

        if marker in condition:
            matches.append(
                (
                    node.lineno,
                    condition,
                )
            )

    return sorted(matches)


def print_method_contract(
    path: Path,
    class_name: str,
    method_name: str,
) -> ast.FunctionDef | ast.AsyncFunctionDef | None:

    tree = parse_module(path)

    class_node = find_class(tree, class_name)

    method = find_method(
        class_node,
        method_name,
    )

    print()
    print(f"{class_name}.{method_name}:")

    if method is None:
        print("  ABSENT")
        return None

    print(
        f"  lines: {method.lineno}-{method.end_lineno}"
    )

    source = path.read_text(encoding="utf-8")

    segment = source_segment(source, method)

    print()
    print("  Calls:")

    calls = call_names(method)

    for name in sorted(set(calls)):
        print(f"    {name}")

    print()
    print("  Attributes:")

    attrs = attribute_names(method)

    for name in sorted(set(attrs)):
        print(f"    {name}")

    print()
    print("  Return paths:")

    for node in ast.walk(method):
        if isinstance(node, ast.Return):
            value = (
                ast.unparse(node.value)
                if node.value is not None
                else "None"
            )

            print(
                f"    line {node.lineno}: return {value}"
            )

    return method


def runtime_objects():
    from SanskritAI.acquisition.models.acquisition_result import (
        AcquisitionResult,
    )
    from SanskritAI.acquisition.models.source_status import (
        SourceStatus,
    )
    from SanskritAI.acquisition.sources.amarakosha import (
        create_amarakosha_source,
    )
    from SanskritAI.acquisition.sources.amarakosha_manifest import (
        create_amarakosha_manifest,
    )

    source = create_amarakosha_source()
    manifest = create_amarakosha_manifest()

    return (
        source,
        manifest,
        AcquisitionResult,
        SourceStatus,
    )


def runtime_local_importer(manifest):
    from SanskritAI.acquisition.downloaders.local_file_importer import (
        LocalFileImporter,
    )

    importer = LocalFileImporter()

    return importer


def main() -> int:

    banner("13R-8F-13 — Local Registration Semantic Contract Audit")

    print(f"Repository root : {REPO_ROOT}")
    print(f"Workspace root  : {WORKSPACE_ROOT}")

    banner("1. Production syntax")

    production_files = [
        ACQUIRER_FILE,
        IMPORTER_FILE,
        SOURCE_FILE,
        MANIFEST_FILE,
        RESULT_FILE,
        STATUS_FILE,
        AMARAKOSHA_SOURCE_FILE,
        AMARAKOSHA_MANIFEST_FILE,
    ]

    for path in production_files:
        if not syntax_check(path):
            return 1

    banner("2. DefaultSourceAcquirer.acquire() contract")

    acquirer_source = ACQUIRER_FILE.read_text(
        encoding="utf-8"
    )

    acquirer_tree = parse_module(ACQUIRER_FILE)

    acquirer_class = find_class(
        acquirer_tree,
        "DefaultSourceAcquirer",
    )

    acquire = find_method(
        acquirer_class,
        "acquire",
    )

    if acquire is None:
        print("DefaultSourceAcquirer.acquire(): FAIL")
        return 1

    print(
        f"acquire() lines: "
        f"{acquire.lineno}-{acquire.end_lineno}"
    )

    local_supports = find_calls(
        acquire,
        "supports",
    )

    local_download = find_calls(
        acquire,
        "download",
    )

    direct_local_return = find_returns_of_call(
        acquire,
        "download",
    )

    print()
    print("supports() calls:")

    for line, expression in local_supports:
        print(
            f"  line {line}: {expression}"
        )

    print()
    print("download() calls:")

    for line, expression in local_download:
        print(
            f"  line {line}: {expression}"
        )

    print()
    print(
        "Direct return of download() result:"
    )

    for line, expression in direct_local_return:
        print(
            f"  line {line}: return {expression}"
        )

    if direct_local_return:
        print(
            "  DIRECT LOCAL RETURN: PRESENT"
        )
    else:
        print(
            "  DIRECT LOCAL RETURN: ABSENT"
        )

    banner("3. LocalFileImporter contract")

    importer_source = IMPORTER_FILE.read_text(
        encoding="utf-8"
    )

    importer_tree = parse_module(
        IMPORTER_FILE
    )

    importer_class = find_class(
        importer_tree,
        "LocalFileImporter",
    )

    resolver = find_method(
        importer_class,
        "_resolve_source_path",
    )

    supports = find_method(
        importer_class,
        "supports",
    )

    download = find_method(
        importer_class,
        "download",
    )

    print(
        "LocalFileImporter._resolve_source_path(): "
        + (
            "PRESENT"
            if resolver is not None
            else "ABSENT"
        )
    )

    print(
        "LocalFileImporter.supports(): "
        + (
            "PRESENT"
            if supports is not None
            else "ABSENT"
        )
    )

    print(
        "LocalFileImporter.download(): "
        + (
            "PRESENT"
            if download is not None
            else "ABSENT"
        )
    )

    if resolver is not None:
        print()
        print(
            "Resolver return/candidate references:"
        )

        resolver_text = source_segment(
            importer_source,
            resolver,
        )

        for marker in [
            "manifest.source.local_path",
            "source.local_path",
            "metadata",
            "source_path",
        ]:
            print(
                f"  {marker:32s}: "
                + (
                    "PRESENT"
                    if marker in resolver_text
                    else "ABSENT"
                )
            )

    banner("4. Canonical runtime objects")

    try:
        (
            source,
            manifest,
            AcquisitionResult,
            SourceStatus,
        ) = runtime_objects()

    except Exception as exc:
        print(
            "Runtime construction FAIL:"
        )
        print(
            f"  {type(exc).__name__}: {exc}"
        )
        return 1

    print(
        f"source_id        : {source.source_id}"
    )
    print(
        f"source.status    : {source.status.value}"
    )
    print(
        f"source.local_path: {source.local_path}"
    )
    print(
        f"source.is_downloaded: "
        f"{source.is_downloaded}"
    )

    print()
    print(
        f"manifest_id      : {manifest.manifest_id}"
    )
    print(
        f"manifest.urls    : {manifest.urls}"
    )
    print(
        f"manifest.mirrors : {manifest.mirrors}"
    )
    print(
        f"manifest.destination: "
        f"{manifest.destination_directory}"
    )
    print(
        f"manifest.filename: "
        f"{manifest.expected_filename}"
    )

    banner("5. LocalFileImporter runtime semantics")

    try:
        importer = runtime_local_importer(
            manifest
        )

        supports_result = importer.supports(
            manifest
        )

        print(
            "LocalFileImporter.supports(manifest): "
            f"{supports_result}"
        )

        print(
            "Canonical source path used: "
            f"{source.local_path}"
        )

        print(
            "Importer can discover canonical "
            "local_path: "
            + (
                "PASS"
                if supports_result
                else "FAIL"
            )
        )

    except Exception as exc:
        print(
            "LocalFileImporter runtime FAIL:"
        )
        print(
            f"  {type(exc).__name__}: {exc}"
        )
        return 1

    banner("6. Destination collision semantics")

    source_path = Path(source.local_path).resolve()

    destination_root = Path(
        manifest.destination_directory
    ).resolve()

    expected_destination = (
        destination_root
        / manifest.expected_filename
    ).resolve()

    print(
        f"source.local_path      : {source_path}"
    )
    print(
        f"manifest destination   : {destination_root}"
    )
    print(
        f"manifest expected file : {expected_destination}"
    )

    print(
        "source exists: "
        + (
            "PASS"
            if source_path.is_file()
            else "FAIL"
        )
    )

    print(
        "expected destination exists: "
        + (
            "PASS"
            if expected_destination.is_file()
            else "FAIL"
        )
    )

    same_path = (
        source_path == expected_destination
    )

    same_file = False

    if (
        source_path.exists()
        and expected_destination.exists()
    ):
        try:
            same_file = (
                source_path.samefile(
                    expected_destination
                )
            )
        except OSError:
            same_file = False

    print(
        f"same resolved path: {same_path}"
    )

    print(
        f"same physical file: {same_file}"
    )

    if same_path or same_file:
        print(
            "LOCAL REGISTRATION COLLISION: CONFIRMED"
        )
    else:
        print(
            "LOCAL REGISTRATION COLLISION: ABSENT"
        )

    banner("7. AcquisitionResult semantics")

    result = AcquisitionResult(
        source=source
    )

    print(
        f"success              : {result.success}"
    )
    print(
        f"message              : {result.message!r}"
    )
    print(
        f"downloaded_files     : "
        f"{result.downloaded_files}"
    )
    print(
        f"bytes_downloaded     : "
        f"{result.bytes_downloaded}"
    )
    print(
        f"checksum_verified    : "
        f"{result.checksum_verified}"
    )
    print(
        f"normalized           : "
        f"{result.normalized}"
    )
    print(
        f"imported             : "
        f"{result.imported}"
    )
    print(
        f"warnings             : "
        f"{result.warnings}"
    )
    print(
        f"errors               : "
        f"{result.errors}"
    )

    print()
    print(
        "AcquisitionResult registration "
        "capability:"
    )

    for name in [
        "mark_success",
        "add_warning",
        "add_error",
        "add_downloaded_file",
        "finalize",
    ]:
        print(
            f"  {name:24s}: "
            + (
                "PRESENT"
                if hasattr(result, name)
                else "ABSENT"
            )
        )

    banner("8. SourceStatus semantics")

    required_statuses = [
        "REGISTERED",
        "SKIPPED",
        "PENDING_DOWNLOAD",
        "DOWNLOADING",
        "DOWNLOADED",
        "VALIDATING",
        "VALIDATED",
        "FAILED",
    ]

    for name in required_statuses:
        present = hasattr(
            SourceStatus,
            name,
        )

        print(
            f"{name:20s}: "
            + (
                "PRESENT"
                if present
                else "ABSENT"
            )
        )

    banner("9. Existing SKIPPED semantics")

    skipped_references = find_calls(
        acquire,
        "update_status",
    )

    skipped_line = None

    for line, expression in skipped_references:
        if "SKIPPED" in expression:
            skipped_line = line

            print(
                f"SKIPPED transition: "
                f"line {line}"
            )

            print(
                f"expression: {expression}"
            )

    if skipped_line is not None:
        print(
            "Existing SKIPPED transition is "
            "associated with an explicit condition."
        )

        for node in ast.walk(acquire):
            if not isinstance(node, ast.If):
                continue

            condition = ast.unparse(node.test)

            if "enabled" in condition:
                print(
                    "SKIPPED condition:"
                )
                print(
                    f"  {condition}"
                )
                break

    banner("10. Existing local branch semantics")

    local_conditions = []

    for node in ast.walk(acquire):
        if not isinstance(node, ast.If):
            continue

        condition = ast.unparse(node.test)

        if (
            "local_importer" in condition
            or "source.local_path" in condition
            or "is_downloaded" in condition
        ):
            local_conditions.append(
                (
                    node.lineno,
                    condition,
                    call_names(node),
                )
            )

    for line, condition, calls in sorted(
        local_conditions
    ):
        print()
        print(
            f"line {line}:"
        )
        print(
            f"  condition: {condition}"
        )
        print(
            f"  calls    : {calls}"
        )

    if not local_conditions:
        print(
            "No local-specific branch detected."
        )

    banner("11. Registration-vs-copy distinction")

    print(
        "LOCAL REGISTRATION means:"
    )
    print(
        "  canonical local artifact already exists"
    )
    print(
        "  source.local_path is authoritative"
    )
    print(
        "  no physical copy is required"
    )
    print(
        "  existing artifact identity may be validated"
    )
    print(
        "  AcquisitionResult can report successful "
        "registration"
    )

    print()
    print(
        "LOCAL PHYSICAL ACQUISITION means:"
    )
    print(
        "  a source path must be copied into a "
        "different destination"
    )
    print(
        "  LocalFileImporter performs filesystem copy"
    )

    print()
    print(
        "Current Amarakośa manifest:"
    )
    print(
        "  source.local_path == destination file: "
        f"{same_path or same_file}"
    )

    banner("12. Production artifact integrity")

    if not ARTIFACT.is_file():
        print(
            f"Artifact missing: {ARTIFACT}"
        )
        return 1

    actual_size = ARTIFACT.stat().st_size
    actual_hash = sha256(ARTIFACT)

    print(
        f"size   : {actual_size}"
    )
    print(
        f"sha256 : {actual_hash}"
    )

    print(
        "size integrity: "
        + (
            "PASS"
            if actual_size == EXPECTED_SIZE
            else "FAIL"
        )
    )

    print(
        "hash integrity: "
        + (
            "PASS"
            if actual_hash == EXPECTED_SHA256
            else "FAIL"
        )
    )

    banner("13. Design contract conclusion")

    print(
        "The audit must NOT create a new importer."
    )
    print(
        "The audit must NOT change CorpusSource.local_path."
    )
    print(
        "The audit must NOT change LocalFileImporter."
    )

    print()

    if same_path or same_file:
        print(
            "CONFIRMED:"
        )
        print(
            "  The canonical artifact and physical "
            "destination collide."
        )

        print()
        print(
            "REQUIRED GENERIC CAPABILITY:"
        )
        print(
            "  DefaultSourceAcquirer must recognize "
            "an already-local canonical artifact "
            "before physical-copy acquisition."
        )

        print()
        print(
            "REGISTRATION BRANCH SHOULD:"
        )
        print(
            "  preserve source.local_path"
        )
        print(
            "  avoid LocalFileImporter.download()"
        )
        print(
            "  avoid self-copy"
        )
        print(
            "  avoid overwriting the canonical artifact"
        )
        print(
            "  return an AcquisitionResult"
        )
        print(
            "  leave checksum/normalization/import "
            "flags to their lifecycle stages"
        )

        print()
        print(
            "STATUS DECISION:"
        )
        print(
            "  Do NOT assume SKIPPED means registration "
            "success."
        )
        print(
            "  Existing SKIPPED is currently tied to "
            "disabled manifests."
        )
        print(
            "  Registration status must therefore be "
            "derived from existing lifecycle semantics."
        )

    else:
        print(
            "No source/destination collision detected."
        )

    banner("14. Read-only guarantee")

    print(
        "Production files modified: NO"
    )
    print(
        "Canonical artifact modified: NO"
    )

    banner("13R-8F-13 RESULT")

    if same_path or same_file:
        print(
            "13R-8F-13 COMPLETE"
        )
        print()
        print(
            "SEMANTIC FINDING"
        )
        print(
            "The missing capability is local "
            "artifact registration, not local "
            "filesystem import."
        )
        print()
        print(
            "REPAIR TARGET"
        )
        print(
            "DefaultSourceAcquirer.acquire()"
        )
        print()
        print(
            "REPAIR CONSTRAINTS"
        )
        print(
            "1. Generic acquisition-boundary repair."
        )
        print(
            "2. No new importer."
        )
        print(
            "3. No new SourceStatus."
        )
        print(
            "4. No CorpusSource.local_path change."
        )
        print(
            "5. No LocalFileImporter change."
        )
        print(
            "6. No self-copy."
        )
        print(
            "7. Preserve existing remote/physical "
            "acquisition behavior."
        )
        print()
        print(
            "NEXT STEP"
        )
        print(
            "13R-8F-14 — minimal production repair "
            "with backup, AST validation, isolated "
            "runtime validation, and regression tests."
        )

    else:
        print(
            "13R-8F-13 COMPLETE"
        )
        print(
            "No production repair is justified "
            "from the current collision evidence."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
