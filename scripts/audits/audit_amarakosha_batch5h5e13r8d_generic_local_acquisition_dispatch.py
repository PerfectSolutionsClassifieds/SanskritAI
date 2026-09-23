from __future__ import annotations

"""
13R-8D — Generic local-acquisition dispatch audit

Purpose
-------
Determine whether the existing generic acquisition architecture already
contains a production integration/dispatch point for LocalFileImporter.

This audit is READ-ONLY.

It must:
1. Inspect production acquisition Python files.
2. Ignore historical/duplicate numbered scripts and _G<number>.py files.
3. Inspect LocalFileImporter references.
4. Inspect BaseDownloader / downloader dispatch.
5. Inspect SourceAcquirer / DefaultSourceAcquirer dispatch.
6. Inspect AcquisitionPipeline / AcquisitionService dispatch.
7. Inspect registries/factories that could select an importer.
8. Determine whether LocalFileImporter is actually reachable from the
   current generic acquisition flow.
9. Do NOT modify production files.
10. Do NOT execute any local acquisition.

No Amarakośa-specific acquisition class should be created here.
"""

from pathlib import Path
import ast
import re
import inspect


ROOT = Path("/content/SanskritAI")
ACQUISITION = ROOT / "acquisition"


print("=" * 72)
print("13R-8D — Generic local-acquisition dispatch audit")
print("=" * 72)
print(f"Repository root : {ROOT}")


# ---------------------------------------------------------------------
# Production-file filter
# ---------------------------------------------------------------------

DUPLICATE_RE = re.compile(
    r"(?:\d+|_G\d+)\.py$",
    re.IGNORECASE,
)


def is_production_python(path: Path) -> bool:
    if not path.name.endswith(".py"):
        return False

    if DUPLICATE_RE.search(path.name):
        return False

    if "__pycache__" in path.parts:
        return False

    return True


production_files = sorted(
    p
    for p in ACQUISITION.rglob("*.py")
    if is_production_python(p)
)


print("\n" + "-" * 72)
print("Production acquisition scope")
print("-" * 72)
print(f"Production Python files : {len(production_files)}")


# ---------------------------------------------------------------------
# AST parse
# ---------------------------------------------------------------------

parse_failures = []

for path in production_files:
    try:
        ast.parse(
            path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        )
    except Exception as exc:
        parse_failures.append(
            (path.relative_to(ROOT), str(exc))
        )


print(f"AST parse failures      : {len(parse_failures)}")

if parse_failures:
    for path, error in parse_failures:
        print(f"  FAIL {path}: {error}")

    raise SystemExit(
        "ABORT — production acquisition scope contains AST parse failures."
    )


print("AST parsing             : PASS")


# ---------------------------------------------------------------------
# Text-reference search
# ---------------------------------------------------------------------

TARGETS = [
    "LocalFileImporter",
    "BaseDownloader",
    "HTTPDownloader",
    "SourceAcquirer",
    "DefaultSourceAcquirer",
    "AcquisitionPipeline",
    "AcquisitionService",
    "DefaultAcquisitionService",
    "ProviderRegistry",
    "ImporterRegistry",
    "DownloaderRegistry",
    "register",
    "supports(",
]


def search_text(term: str):
    matches = []

    for path in production_files:
        text = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        for lineno, line in enumerate(
            text.splitlines(),
            start=1,
        ):
            if term in line:
                matches.append(
                    (
                        path.relative_to(ROOT),
                        lineno,
                        line.strip(),
                    )
                )

    return matches


print("\n" + "-" * 72)
print("Production reference inventory")
print("-" * 72)

reference_map = {}

for target in TARGETS:
    matches = search_text(target)
    reference_map[target] = matches

    print(
        f"{target:<28}: {len(matches)}"
    )


# ---------------------------------------------------------------------
# LocalFileImporter detailed references
# ---------------------------------------------------------------------

print("\n" + "-" * 72)
print("LocalFileImporter references")
print("-" * 72)

local_refs = reference_map["LocalFileImporter"]

for path, lineno, line in local_refs:
    print(
        f"{path}:{lineno}: {line}"
    )


# ---------------------------------------------------------------------
# Inspect LocalFileImporter class
# ---------------------------------------------------------------------

print("\n" + "-" * 72)
print("LocalFileImporter implementation")
print("-" * 72)

try:
    from SanskritAI.acquisition.downloaders.local_file_importer import (
        LocalFileImporter,
    )

    print(
        inspect.getsource(LocalFileImporter)
    )

except Exception as exc:
    print(
        f"LocalFileImporter import failed: {exc}"
    )


# ---------------------------------------------------------------------
# Inspect acquisition pipeline
# ---------------------------------------------------------------------

print("\n" + "-" * 72)
print("AcquisitionPipeline implementation")
print("-" * 72)

try:
    from SanskritAI.acquisition.pipelines.acquisition_pipeline import (
        AcquisitionPipeline,
    )

    print(
        inspect.getsource(AcquisitionPipeline)
    )

except Exception as exc:
    print(
        f"AcquisitionPipeline import failed: {exc}"
    )


# ---------------------------------------------------------------------
# Inspect DefaultSourceAcquirer
# ---------------------------------------------------------------------

print("\n" + "-" * 72)
print("DefaultSourceAcquirer implementation")
print("-" * 72)

try:
    from SanskritAI.acquisition.acquirers.default_source_acquirer import (
        DefaultSourceAcquirer,
    )

    print(
        inspect.getsource(DefaultSourceAcquirer)
    )

except Exception as exc:
    print(
        f"DefaultSourceAcquirer import failed: {exc}"
    )


# ---------------------------------------------------------------------
# Inspect BaseDownloader
# ---------------------------------------------------------------------

print("\n" + "-" * 72)
print("BaseDownloader implementation")
print("-" * 72)

try:
    from SanskritAI.acquisition.downloaders.base_downloader import (
        BaseDownloader,
    )

    print(
        inspect.getsource(BaseDownloader)
    )

except Exception as exc:
    print(
        f"BaseDownloader import failed: {exc}"
    )


# ---------------------------------------------------------------------
# Search for actual dispatch constructs
# ---------------------------------------------------------------------

print("\n" + "-" * 72)
print("Potential dispatch / selection evidence")
print("-" * 72)

dispatch_terms = [
    "isinstance(",
    ".supports(",
    "supports(manifest",
    "downloaders",
    "importers",
    "registry",
    "register(",
    "get_importer",
    "get_downloader",
    "select",
    "resolve",
    "source_path",
    "file://",
]


dispatch_evidence = []

for term in dispatch_terms:
    for path, lineno, line in search_text(term):
        dispatch_evidence.append(
            (
                str(path),
                lineno,
                term,
                line,
            )
        )


for path, lineno, term, line in dispatch_evidence:
    print(
        f"{path}:{lineno} [{term}] {line}"
    )


# ---------------------------------------------------------------------
# Specific source-path usage
# ---------------------------------------------------------------------

print("\n" + "-" * 72)
print("source_path integration evidence")
print("-" * 72)

source_path_matches = search_text("source_path")

for path, lineno, line in source_path_matches:
    print(
        f"{path}:{lineno}: {line}"
    )


# ---------------------------------------------------------------------
# Runtime construction probes
# ---------------------------------------------------------------------

print("\n" + "-" * 72)
print("Runtime construction probes")
print("-" * 72)

try:
    from SanskritAI.acquisition.downloaders.local_file_importer import (
        LocalFileImporter,
    )

    importer = LocalFileImporter()

    print(
        f"LocalFileImporter() : PASS ({type(importer).__name__})"
    )

except Exception as exc:
    print(
        f"LocalFileImporter() : FAIL ({exc})"
    )


try:
    from SanskritAI.acquisition.acquirers.default_source_acquirer import (
        DefaultSourceAcquirer,
    )

    acquirer = DefaultSourceAcquirer()

    print(
        f"DefaultSourceAcquirer() : PASS ({type(acquirer).__name__})"
    )

except Exception as exc:
    print(
        f"DefaultSourceAcquirer() : FAIL ({exc})"
    )


# ---------------------------------------------------------------------
# Decision
# ---------------------------------------------------------------------

print("\n" + "=" * 72)
print("13R-8D decision")
print("=" * 72)

print(
    """
Interpretation rules:

A. If LocalFileImporter is already selected by the generic runtime:
   -> no production repair is required.
   -> proceed to 13R-8E runtime probe using a SAFE TEMPORARY COPY.

B. If LocalFileImporter exists but is not selected:
   -> identify the smallest existing generic dispatch boundary.
   -> do NOT create Amarakośa-specific acquisition code.
   -> next step is a minimal generic local-acquisition integration repair.

C. If no generic dispatch boundary exists:
   -> stop implementation.
   -> design the smallest generic acquisition abstraction only after
      documenting the existing contracts.

D. Never execute the current Amarakośa manifest directly because its
   source and destination are the same physical file.

E. No production files are modified by this audit.
"""
)

print(
    "RESULT: PASS — generic local-acquisition dispatch audit completed."
)
