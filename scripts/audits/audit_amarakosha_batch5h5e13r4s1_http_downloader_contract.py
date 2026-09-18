
from __future__ import annotations

"""
BATCH 5H-5E-13R-4S-1
====================

HTTP DOWNLOADER CONTRACT AUDIT

Purpose
-------
Audit the actual downloader class and every production caller before
performing any compatibility repair.

Important
---------
This is READ-ONLY.

Excluded from production conclusions:
    * tests
    * audit scripts
    * repair scripts
    * __pycache__
    * historical numbered Python files
    * *_G<number>.py

No production files are modified.
"""

from pathlib import Path
import inspect
import re
import sys

PROJECT_ROOT = Path("/content/SanskritAI")


def section(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def is_historical_python(path: Path) -> bool:
    stem = path.stem

    if re.search(r"\d+$", stem):
        return True

    if re.search(r"_G\d+$", stem):
        return True

    return False


def classify(path: Path) -> str:
    relative = path.relative_to(PROJECT_ROOT)
    parts = set(relative.parts)

    if "__pycache__" in parts:
        return "cache"

    if "tests" in parts:
        return "test"

    if "scripts" in parts:
        if "audits" in parts:
            return "audit"

        if "repairs" in parts or "repair" in parts:
            return "repair"

        return "script"

    return "production"


def production_files() -> list[Path]:
    files = []

    for path in PROJECT_ROOT.rglob("*.py"):

        if is_historical_python(path):
            continue

        if classify(path) != "production":
            continue

        files.append(path)

    return sorted(files)


def find_exact(token: str, files: list[Path]):
    results = []

    for path in files:

        try:
            text = path.read_text(
                encoding="utf-8"
            )
        except Exception:
            continue

        for number, line in enumerate(
            text.splitlines(),
            start=1,
        ):

            if token in line:

                results.append(
                    (
                        str(
                            path.relative_to(
                                PROJECT_ROOT
                            )
                        ),
                        number,
                        line.strip(),
                    )
                )

    return results


def print_matches(
    title: str,
    token: str,
    files: list[Path],
) -> None:

    results = find_exact(
        token,
        files,
    )

    print()
    print(title)
    print(f"Token   : {token!r}")
    print(f"Matches : {len(results)}")

    for path, line, text in results:
        print(
            f"  {path}:{line}: {text}"
        )


def main() -> None:

    section(
        "BATCH 5H-5E-13R-4S-1 — "
        "HTTP DOWNLOADER CONTRACT AUDIT"
    )

    if not PROJECT_ROOT.exists():
        raise RuntimeError(
            f"Project root does not exist: "
            f"{PROJECT_ROOT}"
        )

    parent = str(
        PROJECT_ROOT.parent
    )

    if parent not in sys.path:
        sys.path.insert(
            0,
            parent,
        )

    import SanskritAI

    print(
        "SanskritAI import : PASS"
    )

    production = production_files()

    print(
        f"Production Python files : "
        f"{len(production)}"
    )

    section(
        "1. ACTUAL HTTP DOWNLOADER MODULE"
    )

    module = __import__(
        "SanskritAI.acquisition.downloaders.http_downloader",
        fromlist=["*"],
    )

    print(
        f"Module : {module.__name__}"
    )

    classes = []

    for name, value in inspect.getmembers(
        module,
        inspect.isclass,
    ):

        if value.__module__ != module.__name__:
            continue

        classes.append(value)

        print()
        print(
            f"Class : {name}"
        )

        print(
            f"Abstract : "
            f"{inspect.isabstract(value)}"
        )

        try:
            print(
                f"Constructor : "
                f"{inspect.signature(value)}"
            )
        except Exception:
            print(
                "Constructor : <unavailable>"
            )

        print(
            f"Docstring : "
            f"{inspect.getdoc(value) or '<none>'}"
        )

        for method_name, method in inspect.getmembers(
            value,
            inspect.isfunction,
        ):

            if method_name.startswith("_"):
                continue

            try:
                signature = inspect.signature(
                    method
                )
            except Exception:
                signature = "<unavailable>"

            print(
                f"  method {method_name}{signature}"
            )

    section(
        "2. DOWNLOADER PACKAGE EXPORTS"
    )

    package = __import__(
        "SanskritAI.acquisition.downloaders",
        fromlist=["*"],
    )

    print(
        f"Package : {package.__name__}"
    )

    for name in (
        "HTTPDownloader",
        "HttpDownloader",
        "BaseDownloader",
        "LocalFileImporter",
    ):

        print(
            f"  {name} exported : "
            f"{hasattr(package, name)}"
        )

    section(
        "3. MODULE EXPORTS"
    )

    for name in (
        "HTTPDownloader",
        "HttpDownloader",
    ):

        print(
            f"  {name} in module : "
            f"{hasattr(module, name)}"
        )

    section(
        "4. PRODUCTION REFERENCES"
    )

    for token in (
        "HttpDownloader",
        "HTTPDownloader",
        "from SanskritAI.acquisition.downloaders.http_downloader import HttpDownloader",
        "from SanskritAI.acquisition.downloaders.http_downloader import HTTPDownloader",
        "from .http_downloader import HttpDownloader",
        "from .http_downloader import HTTPDownloader",
    ):

        print_matches(
            "Production reference",
            token,
            production,
        )

    section(
        "5. SPECIFIC FAILING IMPORTS"
    )

    failing_modules = (
        "cologne_provider",
        "github_provider",
        "gretil_provider",
        "internet_archive_provider",
        "sanskritdocuments_provider",
        "sarit_provider",
        "xml_corpus_provider",
        "base_repository_client",
        "acquisition_manager",
    )

    import importlib

    for module_name in failing_modules:

        if module_name == "base_repository_client":

            module_path = (
                "SanskritAI.acquisition.repositories."
                "base_repository_client"
            )

        elif module_name == "acquisition_manager":

            module_path = (
                "SanskritAI.acquisition."
                "acquisition_manager"
            )

        else:

            module_path = (
                "SanskritAI.acquisition.providers."
                + module_name
            )

        print()
        print(
            f"{module_name}"
        )
        print(
            f"  import path : {module_path}"
        )

        try:

            importlib.import_module(
                module_path
            )

            print(
                "  import : PASS"
            )

        except Exception as exc:

            print(
                "  import : FAIL"
            )

            print(
                f"  error : {exc!r}"
            )

    section(
        "6. COMPATIBILITY INTERPRETATION"
    )

    print(
        "Actual concrete class discovered : "
        f"{[cls.__name__ for cls in classes]}"
    )

    print()

    print(
        "This audit does not rename or alias anything."
    )

    print(
        "The purpose is to determine the canonical "
        "class name and the exact stale caller surface."
    )

    section(
        "7. FINAL RESULT"
    )

    print(
        "BATCH 5H-5E-13R-4S-1 — RESULT: "
        "AUDIT COMPLETE"
    )


if __name__ == "__main__":
    main()
