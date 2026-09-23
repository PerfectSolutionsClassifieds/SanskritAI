
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path


ROOT = Path("/content/SanskritAI")
ACQUISITION_ROOT = ROOT / "acquisition"

PARENT = ROOT.parent

if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))


EXCLUDED_DIRS = {
    "__pycache__",
    "tests",
    ".git",
}

DUPLICATE_SUFFIX_RE = re.compile(
    r"(?:\d+|_G\d+)\.py$"
)


TARGET_SYMBOLS = {
    "AcquisitionManifest",
    "CorpusSource",
    "AcquisitionResult",
    "AcquisitionRequest",
    "AcquisitionResponse",
    "SourceAcquirer",
    "DefaultSourceAcquirer",
    "AcquisitionService",
    "DefaultAcquisitionService",
    "AcquisitionManager",
    "LocalFileImporter",
    "BaseDownloader",
    "HTTPDownloader",
}


def section(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def is_production_python(path: Path) -> bool:
    if path.suffix != ".py":
        return False

    if any(part in EXCLUDED_DIRS for part in path.parts):
        return False

    if DUPLICATE_SUFFIX_RE.search(path.name):
        return False

    return True


def production_files() -> list[Path]:
    if not ACQUISITION_ROOT.exists():
        return []

    return sorted(
        path
        for path in ACQUISITION_ROOT.rglob("*.py")
        if is_production_python(path)
    )


def safe_relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def parse_file(path: Path):
    try:
        text = path.read_text(
            encoding="utf-8",
            errors="replace",
        )
    except Exception:
        return None, None

    try:
        tree = ast.parse(
            text,
            filename=str(path),
        )
    except SyntaxError as exc:
        return text, exc

    return tree, None


def dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)

        if parent:
            return f"{parent}.{node.attr}"

        return node.attr

    return None


def collect_ast_references(path: Path):
    tree, error = parse_file(path)

    if tree is None:
        return [], error

    if isinstance(error, SyntaxError):
        return [], error

    references = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Name):
            if node.id in TARGET_SYMBOLS:
                references.append(
                    {
                        "symbol": node.id,
                        "kind": "Name",
                        "line": node.lineno,
                    }
                )

        elif isinstance(node, ast.Attribute):
            name = dotted_name(node)

            if name:
                terminal = name.rsplit(".", 1)[-1]

                if terminal in TARGET_SYMBOLS:
                    references.append(
                        {
                            "symbol": terminal,
                            "kind": "Attribute",
                            "line": node.lineno,
                            "name": name,
                        }
                    )

        elif isinstance(node, ast.ImportFrom):

            imported_names = {
                alias.name
                for alias in node.names
            }

            matches = (
                imported_names
                & TARGET_SYMBOLS
            )

            for symbol in sorted(matches):
                references.append(
                    {
                        "symbol": symbol,
                        "kind": "ImportFrom",
                        "line": node.lineno,
                        "module": node.module,
                    }
                )

    return references, None


def collect_text_evidence(
    path: Path,
    text: str,
):
    evidence = []

    interesting_patterns = {
        "manifest construction":
            r"AcquisitionManifest\s*\(",

        "manifest parameter":
            r"\bmanifest\b",

        "source parameter":
            r"\bsource\b",

        "local path":
            r"\blocal_path\b",

        "destination directory":
            r"\bdestination_directory\b",

        "acquisition result":
            r"\bAcquisitionResult\b",

        "local file importer":
            r"\bLocalFileImporter\b",

        "acquisition service":
            r"\bAcquisitionService\b",

        "source acquirer":
            r"\bSourceAcquirer\b",
    }

    lines = text.splitlines()

    for label, pattern in interesting_patterns.items():

        regex = re.compile(pattern)

        for number, line in enumerate(lines, start=1):

            if regex.search(line):

                evidence.append(
                    {
                        "label": label,
                        "line": number,
                        "text": line.strip(),
                    }
                )

    return evidence


def main() -> int:

    section(
        "13R-8 — Amarakośa runtime entry-point discovery"
    )

    print(f"Repository root : {ROOT}")
    print(
        f"Acquisition root: {ACQUISITION_ROOT}"
    )

    # ------------------------------------------------------------------
    # Bootstrap
    # ------------------------------------------------------------------

    section("Production scope")

    if not ROOT.exists():
        print("Repository root : FAIL")
        return 1

    if not ACQUISITION_ROOT.exists():
        print("Acquisition root : FAIL")
        return 1

    print("Repository root : PASS")
    print("Acquisition root : PASS")

    files = production_files()

    print()
    print(
        f"Production acquisition Python files : "
        f"{len(files)}"
    )

    if not files:
        print(
            "RESULT: FAIL — no production acquisition "
            "files discovered."
        )
        return 1

    # ------------------------------------------------------------------
    # AST references
    # ------------------------------------------------------------------

    section(
        "Acquisition runtime symbol references"
    )

    all_references = []

    syntax_failures = []

    for path in files:

        references, error = collect_ast_references(path)

        if isinstance(error, SyntaxError):

            syntax_failures.append(
                (
                    path,
                    error,
                )
            )

        for reference in references:

            reference["path"] = path

            all_references.append(
                reference
            )

    if syntax_failures:

        print(
            f"AST syntax failures : "
            f"{len(syntax_failures)}"
        )

        for path, error in syntax_failures:

            print(
                f"  {safe_relative(path)}"
                f" : line {error.lineno}"
                f" : {error.msg}"
            )

    else:

        print(
            "AST parse across production acquisition "
            "files : PASS"
        )

    # ------------------------------------------------------------------
    # Group references by symbol
    # ------------------------------------------------------------------

    section(
        "Reference map"
    )

    for symbol in sorted(TARGET_SYMBOLS):

        matches = [
            reference
            for reference in all_references
            if reference["symbol"] == symbol
        ]

        print()
        print(
            f"{symbol} : {len(matches)} reference(s)"
        )

        for reference in matches:

            path = reference["path"]

            print(
                f"  {safe_relative(path)}:"
                f"{reference['line']}"
                f" [{reference['kind']}]"
            )

            if "module" in reference:
                print(
                    f"      module = "
                    f"{reference['module']}"
                )

            if "name" in reference:
                print(
                    f"      name   = "
                    f"{reference['name']}"
                )

    # ------------------------------------------------------------------
    # Detailed text evidence for manifest flow
    # ------------------------------------------------------------------

    section(
        "Manifest flow evidence"
    )

    manifest_files = []

    for path in files:

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except Exception:
            continue

        evidence = collect_text_evidence(
            path,
            text,
        )

        manifest_evidence = [
            item
            for item in evidence
            if item["label"]
            in {
                "manifest construction",
                "manifest parameter",
                "destination directory",
                "local path",
                "acquisition result",
                "local file importer",
            }
        ]

        if manifest_evidence:

            manifest_files.append(
                (
                    path,
                    manifest_evidence,
                )
            )

    print(
        f"Files with manifest/runtime evidence : "
        f"{len(manifest_files)}"
    )

    for path, evidence in manifest_files:

        print()
        print(
            safe_relative(path)
        )

        for item in evidence:

            print(
                f"  L{item['line']}: "
                f"{item['text']}"
            )

    # ------------------------------------------------------------------
    # Candidate orchestration files
    # ------------------------------------------------------------------

    section(
        "Candidate runtime orchestration files"
    )

    orchestration_keywords = (
        "acquire",
        "acquisition",
        "service",
        "manager",
        "acquirer",
        "importer",
        "repository",
    )

    candidates = []

    for path in files:

        lower_name = path.name.lower()

        if any(
            keyword in lower_name
            for keyword in orchestration_keywords
        ):
            candidates.append(path)

    print(
        f"Candidate files : {len(candidates)}"
    )

    for path in candidates:
        print(
            f"  {safe_relative(path)}"
        )

    # ------------------------------------------------------------------
    # Specific local-artifact runtime evidence
    # ------------------------------------------------------------------

    section(
        "Local artifact execution evidence"
    )

    local_evidence = []

    for path in files:

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except Exception:
            continue

        patterns = (
            r"local_path",
            r"LocalFileImporter",
            r"copy",
            r"shutil",
            r"destination_directory",
            r"validate_checksum",
            r"requires_download",
            r"requires_checksum_validation",
        )

        matching_lines = []

        lines = text.splitlines()

        for number, line in enumerate(
            lines,
            start=1,
        ):

            if any(
                re.search(pattern, line)
                for pattern in patterns
            ):

                matching_lines.append(
                    (
                        number,
                        line.strip(),
                    )
                )

        if matching_lines:

            local_evidence.append(
                (
                    path,
                    matching_lines,
                )
            )

    print(
        f"Files with local-acquisition evidence : "
        f"{len(local_evidence)}"
    )

    for path, lines in local_evidence:

        print()
        print(
            safe_relative(path)
        )

        for number, line in lines[:30]:

            print(
                f"  L{number}: {line}"
            )

        if len(lines) > 30:

            print(
                f"  ... "
                f"{len(lines) - 30} additional matches"
            )

    # ------------------------------------------------------------------
    # Decision
    # ------------------------------------------------------------------

    section(
        "13R-8 runtime discovery decision"
    )

    manifest_references = [
        reference
        for reference in all_references
        if reference["symbol"]
        == "AcquisitionManifest"
    ]

    result_references = [
        reference
        for reference in all_references
        if reference["symbol"]
        == "AcquisitionResult"
    ]

    importer_references = [
        reference
        for reference in all_references
        if reference["symbol"]
        == "LocalFileImporter"
    ]

    service_references = [
        reference
        for reference in all_references
        if reference["symbol"]
        in {
            "AcquisitionService",
            "DefaultAcquisitionService",
            "AcquisitionManager",
            "SourceAcquirer",
            "DefaultSourceAcquirer",
        }
    ]

    print(
        "AcquisitionManifest references : "
        f"{len(manifest_references)}"
    )

    print(
        "AcquisitionResult references   : "
        f"{len(result_references)}"
    )

    print(
        "LocalFileImporter references   : "
        f"{len(importer_references)}"
    )

    print(
        "Acquisition orchestration refs : "
        f"{len(service_references)}"
    )

    print()

    if manifest_references:

        print(
            "Manifest consumption exists "
            "somewhere in production."
        )

    else:

        print(
            "No production AcquisitionManifest "
            "consumer was established."
        )

    if result_references:

        print(
            "AcquisitionResult production "
            "boundary exists."
        )

    else:

        print(
            "No AcquisitionResult production "
            "consumer was established."
        )

    if importer_references:

        print(
            "LocalFileImporter production "
            "boundary exists."
        )

    else:

        print(
            "No LocalFileImporter production "
            "consumer was established."
        )

    print()
    print(
        "IMPORTANT:"
    )
    print(
        "This audit is read-only."
    )
    print(
        "It does not create an Amarakośa-specific "
        "acquirer, provider, downloader, or service."
    )

    print()
    print(
        "RESULT: PASS — existing runtime entry-point "
        "evidence collected."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
