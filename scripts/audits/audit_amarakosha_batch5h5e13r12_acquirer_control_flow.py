from __future__ import annotations

"""
13R-8F-12 — DefaultSourceAcquirer Control-Flow Audit

Purpose
-------
Read-only audit of the generic DefaultSourceAcquirer acquisition boundary.

This audit determines the exact control-flow insertion point for a future
generic LOCAL REGISTRATION branch.

It does NOT modify production files.

Architectural rule
------------------
Do not repair LocalFileImporter.

Do not create:
    LocalRegistrationImporter
    AlreadyLocalImporter
    new LOCAL SourceStatus

Canonical local source identity is:
    CorpusSource.local_path

Actual filesystem copying remains:
    LocalFileImporter

This audit only determines whether DefaultSourceAcquirer.acquire()
contains an explicit local-registration path and where a minimal
generic registration branch should be inserted.

Excluded
--------
Historical/duplicate production copies are ignored.
"""

from pathlib import Path
import ast
import hashlib
import inspect
import sys
import textwrap
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

SOURCE_FILE = (
    REPO_ROOT
    / "acquisition"
    / "sources"
    / "amarakosha.py"
)

MANIFEST_FILE = (
    REPO_ROOT
    / "acquisition"
    / "sources"
    / "amarakosha_manifest.py"
)

ARTIFACT = REPO_ROOT / "amarakosha.txt"

EXPECTED_SHA256 = (
    "d82a5234e4bc15ef295b1b375a6548e02df9a10d6eb94e0f97223289c46c3190"
)

EXPECTED_SIZE = 645456


def banner(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def syntax_check(path: Path) -> bool:
    try:
        ast.parse(path.read_text(encoding="utf-8"))
        print(f"{path}: Python syntax PASS")
        return True
    except Exception as exc:
        print(f"{path}: Python syntax FAIL")
        print(f"  {exc}")
        return False


def sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def production_ast() -> ast.Module:
    return ast.parse(
        ACQUIRER_FILE.read_text(encoding="utf-8"),
        filename=str(ACQUIRER_FILE),
    )


def find_method(tree: ast.Module, name: str) -> ast.FunctionDef | None:
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            if node.name != "DefaultSourceAcquirer":
                continue

            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if child.name == name:
                        return child

    return None


def source_segment(source: str, node: ast.AST) -> str:
    segment = ast.get_source_segment(source, node)

    if segment is None:
        return ""

    return textwrap.dedent(segment)


def call_names(node: ast.AST) -> list[str]:
    names: list[str] = []

    for child in ast.walk(node):
        if isinstance(child, ast.Call):
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


def string_constants(node: ast.AST) -> list[str]:
    values: list[str] = []

    for child in ast.walk(node):
        if isinstance(child, ast.Constant):
            if isinstance(child.value, str):
                values.append(child.value)

    return values


def statement_labels(method: ast.FunctionDef) -> list[str]:
    labels: list[str] = []

    for index, node in enumerate(method.body, start=1):
        if isinstance(node, ast.If):
            labels.append(f"IF[{index}]")
        elif isinstance(node, ast.Try):
            labels.append(f"TRY[{index}]")
        elif isinstance(node, ast.Return):
            labels.append(f"RETURN[{index}]")
        elif isinstance(node, ast.Assign):
            labels.append(f"ASSIGN[{index}]")
        elif isinstance(node, ast.Expr):
            labels.append(f"EXPR[{index}]")
        else:
            labels.append(f"{type(node).__name__.upper()}[{index}]")

    return labels


def describe_if_conditions(method: ast.FunctionDef, source: str) -> None:
    print()
    print("IF / branch conditions in acquire():")

    found = False

    for node in ast.walk(method):
        if isinstance(node, ast.If):
            found = True

            condition = ast.get_source_segment(source, node.test)
            condition = textwrap.dedent(condition or "").strip()

            print()
            print(f"  line {node.lineno}:")
            print(f"    condition: {condition}")

            body_calls = call_names(node)
            body_attrs = attribute_names(node)

            if body_calls:
                print(f"    calls   : {body_calls}")

            if body_attrs:
                print(f"    attrs   : {body_attrs}")

    if not found:
        print("  NONE")


def locate_call(method: ast.FunctionDef, name: str) -> list[int]:
    lines: list[int] = []

    for node in ast.walk(method):
        if isinstance(node, ast.Call):
            function = node.func

            if isinstance(function, ast.Name):
                if function.id == name:
                    lines.append(node.lineno)

            elif isinstance(function, ast.Attribute):
                if function.attr == name:
                    lines.append(node.lineno)

    return sorted(set(lines))


def locate_attribute(method: ast.FunctionDef, name: str) -> list[int]:
    lines: list[int] = []

    for node in ast.walk(method):
        if isinstance(node, ast.Attribute):
            if node.attr == name:
                lines.append(node.lineno)

    return sorted(set(lines))


def analyze_order(method: ast.FunctionDef, source: str) -> None:
    interesting = [
        "_validate_manifest",
        "_prepare_destination",
        "_download_from_sources",
        "mark_success",
        "finalize",
        "update_status",
        "set_local_path",
    ]

    locations: list[tuple[int, str]] = []

    for name in interesting:
        for line in locate_call(method, name):
            locations.append((line, f"call:{name}"))

    for name in ["local_path"]:
        for line in locate_attribute(method, name):
            locations.append((line, f"attribute:{name}"))

    locations.sort()

    print()
    print("Ordered lifecycle references:")
    if not locations:
        print("  NONE")
        return

    for line, label in locations:
        print(f"  line {line:4d} : {label}")

    print()
    print("Relative ordering:")

    positions = {}

    for line, label in locations:
        positions.setdefault(label, []).append(line)

    for name in interesting:
        key = f"call:{name}"
        if key in positions:
            print(f"  {key:32s}: {positions[key]}")

    if "attribute:local_path" in positions:
        print(
            f"  {'attribute:local_path':32s}: "
            f"{positions['attribute:local_path']}"
        )


def inspect_local_conditions(method: ast.FunctionDef, source: str) -> None:
    print()
    print("Local-registration condition analysis:")

    local_markers = [
        "local_path",
        "SKIPPED",
        "source.local_path",
        "manifest.source.local_path",
        "source_path",
        "LocalFileImporter",
        "is_downloaded",
    ]

    full_text = source_segment(source, method)

    for marker in local_markers:
        lines = [
            index + method.lineno - 1
            for index, line in enumerate(full_text.splitlines())
            if marker in line
        ]

        if lines:
            print(f"  {marker:32s}: PRESENT")
        else:
            print(f"  {marker:32s}: ABSENT")


def inspect_status_transitions(method: ast.FunctionDef, source: str) -> None:
    print()
    print("SourceStatus transitions inside acquire():")

    found = False

    for node in ast.walk(method):
        if isinstance(node, ast.Call):
            function = node.func

            if not isinstance(function, ast.Attribute):
                continue

            if function.attr != "update_status":
                continue

            found = True

            args = []
            for arg in node.args:
                segment = ast.get_source_segment(source, arg)
                if segment:
                    args.append(textwrap.dedent(segment).strip())

            print(f"  line {node.lineno}: update_status({', '.join(args)})")

    if not found:
        print("  NONE")


def inspect_returns(method: ast.FunctionDef, source: str) -> None:
    print()
    print("Return paths in acquire():")

    found = False

    for node in ast.walk(method):
        if isinstance(node, ast.Return):
            found = True

            value = ast.get_source_segment(source, node.value)

            print(f"  line {node.lineno}: return")

            if value:
                print(
                    "    expression: "
                    + textwrap.dedent(value).strip()
                )

    if not found:
        print("  NONE")


def inspect_try_structure(method: ast.FunctionDef) -> None:
    print()
    print("Exception/finalization structure:")

    for node in method.body:
        if isinstance(node, ast.Try):
            print(f"  TRY starts at line {node.lineno}")

            print(
                f"    body statements    : {len(node.body)}"
            )
            print(
                f"    except handlers    : {len(node.handlers)}"
            )
            print(
                f"    finally statements : {len(node.finalbody)}"
            )

            if node.finalbody:
                final_calls = call_names(
                    ast.Module(
                        body=node.finalbody,
                        type_ignores=[],
                    )
                )

                print(f"    finally calls      : {final_calls}")


def inspect_disabled_guard(method: ast.FunctionDef, source: str) -> None:
    print()
    print("Disabled-manifest guard:")

    for node in ast.walk(method):
        if not isinstance(node, ast.If):
            continue

        condition = ast.get_source_segment(source, node.test) or ""

        if "enabled" in condition:
            print(f"  line {node.lineno}: {textwrap.dedent(condition).strip()}")

            calls = call_names(node)
            attrs = attribute_names(node)

            print(f"  calls: {calls}")
            print(f"  attrs: {attrs}")

            return

    print("  No explicit enabled guard detected.")


def runtime_contract():
    from SanskritAI.acquisition.models.acquisition_manifest import (
        AcquisitionManifest,
    )
    from SanskritAI.acquisition.models.source_status import SourceStatus
    from SanskritAI.acquisition.sources.amarakosha import (
        create_amarakosha_source,
    )
    from SanskritAI.acquisition.sources.amarakosha_manifest import (
        create_amarakosha_manifest,
    )

    source = create_amarakosha_source()
    manifest = create_amarakosha_manifest()

    return source, manifest, AcquisitionManifest, SourceStatus


def main() -> int:
    banner("13R-8F-12 — DefaultSourceAcquirer Control-Flow Audit")

    print(f"Repository root : {REPO_ROOT}")
    print(f"Workspace root  : {WORKSPACE_ROOT}")
    print(f"Target          : {ACQUIRER_FILE}")

    banner("1. Production syntax")

    if not syntax_check(ACQUIRER_FILE):
        return 1

    if not syntax_check(SOURCE_FILE):
        return 1

    if not syntax_check(MANIFEST_FILE):
        return 1

    banner("2. Production source inspection")

    source_text = ACQUIRER_FILE.read_text(encoding="utf-8")
    tree = production_ast()

    acquire = find_method(tree, "acquire")

    if acquire is None:
        print("DefaultSourceAcquirer.acquire(): FAIL")
        return 1

    print(
        "DefaultSourceAcquirer.acquire(): "
        f"lines {acquire.lineno}-{acquire.end_lineno}"
    )

    print()
    print("Top-level acquire() statements:")
    for label in statement_labels(acquire):
        print(f"  {label}")

    banner("3. Disabled-manifest control flow")

    inspect_disabled_guard(acquire, source_text)

    banner("4. Branch condition analysis")

    describe_if_conditions(acquire, source_text)

    banner("5. Lifecycle ordering")

    analyze_order(acquire, source_text)

    banner("6. Local-registration markers")

    inspect_local_conditions(acquire, source_text)

    banner("7. SourceStatus transitions")

    inspect_status_transitions(acquire, source_text)

    banner("8. Return paths")

    inspect_returns(acquire, source_text)

    banner("9. Exception/finalization structure")

    inspect_try_structure(acquire)

    banner("10. Canonical runtime objects")

    try:
        source, manifest, AcquisitionManifest, SourceStatus = (
            runtime_contract()
        )

        print(f"source_id        : {source.source_id}")
        print(f"source.status    : {source.status.value}")
        print(f"source.local_path: {source.local_path}")
        print(f"is_downloaded    : {source.is_downloaded}")

        print()
        print(f"manifest_id      : {manifest.manifest_id}")
        print(f"manifest.urls    : {manifest.urls}")
        print(f"manifest.mirrors : {manifest.mirrors}")
        print(
            "manifest.destination: "
            f"{manifest.destination_directory}"
        )
        print(
            "manifest.filename   : "
            f"{manifest.expected_filename}"
        )

        print()
        print(
            "SourceStatus.SKIPPED: "
            f"{SourceStatus.SKIPPED.value}"
        )
        print(
            "SourceStatus.REGISTERED: "
            f"{SourceStatus.REGISTERED.value}"
        )
        print(
            "SourceStatus.DOWNLOADED: "
            f"{SourceStatus.DOWNLOADED.value}"
        )

    except Exception as exc:
        print("Runtime object construction: FAIL")
        print(f"  {type(exc).__name__}: {exc}")
        return 1

    banner("11. Canonical artifact")

    if not ARTIFACT.is_file():
        print(f"Artifact missing: {ARTIFACT}")
        return 1

    actual_size = ARTIFACT.stat().st_size
    actual_hash = sha256(ARTIFACT)

    print(f"artifact : {ARTIFACT}")
    print(f"size     : {actual_size}")
    print(f"sha256   : {actual_hash}")

    print(
        "size integrity: "
        + ("PASS" if actual_size == EXPECTED_SIZE else "FAIL")
    )

    print(
        "hash integrity: "
        + ("PASS" if actual_hash == EXPECTED_SHA256 else "FAIL")
    )

    banner("12. Control-flow conclusion")

    call_validate = locate_call(acquire, "_validate_manifest")
    call_prepare = locate_call(acquire, "_prepare_destination")
    call_download = locate_call(acquire, "_download_from_sources")
    call_finalize = locate_call(acquire, "finalize")
    local_path_lines = locate_attribute(acquire, "local_path")

    print("Required lifecycle calls:")
    print(f"  _validate_manifest()    : {call_validate}")
    print(f"  _prepare_destination()  : {call_prepare}")
    print(f"  _download_from_sources(): {call_download}")
    print(f"  result.finalize()       : {call_finalize}")
    print(f"  source.local_path refs  : {local_path_lines}")

    explicit_registration = False

    for node in ast.walk(acquire):
        if not isinstance(node, ast.If):
            continue

        condition = ast.get_source_segment(source_text, node.test) or ""
        condition = condition.lower()

        has_local = (
            "local_path" in condition
            or "is_downloaded" in condition
            or "source_path" in condition
        )

        has_registration = (
            "registered" in condition
            or "skipped" in condition
        )

        if has_local and has_registration:
            explicit_registration = True
            break

    print()
    print(
        "Explicit local-registration branch: "
        + ("PRESENT" if explicit_registration else "ABSENT")
    )

    print()
    print("Architectural conclusion:")

    if explicit_registration:
        print(
            "  A local-registration branch already exists."
        )
        print(
            "  Do NOT modify production from this audit."
        )
        print(
            "  Next step should be a semantic/runtime audit of "
            "that branch."
        )
    else:
        print(
            "  No explicit local-registration branch was detected."
        )
        print(
            "  The likely repair target is "
            "DefaultSourceAcquirer.acquire()."
        )
        print(
            "  LocalFileImporter should remain unchanged."
        )
        print(
            "  CorpusSource.local_path should remain canonical."
        )
        print(
            "  No new SourceStatus should be introduced."
        )

    banner("13. Production immutability")

    print("Read-only audit: PASS")
    print("No production files modified by this audit.")

    banner("13R-8F-12 RESULT")

    if explicit_registration:
        print("13R-8F-12 COMPLETE")
        print()
        print(
            "CONTROL-FLOW FINDING"
        )
        print(
            "An explicit local-registration branch exists."
        )
        print(
            "Do not perform a blind generic repair."
        )
        print(
            "Next step: semantic/runtime audit of the existing branch."
        )
        return 0

    print("13R-8F-12 COMPLETE")
    print()
    print("CONTROL-FLOW FINDING")
    print(
        "DefaultSourceAcquirer.acquire() does not contain "
        "an explicit local-registration branch."
    )
    print()
    print("CONFIRMED REPAIR DIRECTION")
    print(
        "The generic acquisition boundary is the correct repair point."
    )
    print()
    print("DO NOT:")
    print("  create LocalRegistrationImporter")
    print("  create AlreadyLocalImporter")
    print("  create a new LOCAL SourceStatus")
    print("  modify CorpusSource.local_path")
    print("  modify LocalFileImporter")
    print()
    print("NEXT STEP:")
    print(
        "13R-8F-13 — minimal generic local-registration "
        "repair design + runtime contract."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
