from __future__ import annotations

from pathlib import Path
import json
import inspect
import re
import sys

REPO_ROOT = Path("/content/SanskritAI")

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

print("=" * 120)
print("BATCH 5H-5E-10 — AMARAKOSHA WORK REGISTRY → CORPUS SOURCE FACTORY RUNTIME BRIDGE")
print("=" * 120)

# ------------------------------------------------------------------
# 1. Import production components
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("1. PRODUCTION COMPONENT IMPORTS")
print("-" * 120)

components = {}

imports = {
    "WorkDefinition":
        "SanskritAI.acquisition.metadata.models.work_definition",
    "WorkRegistry":
        "SanskritAI.acquisition.metadata.registries.work_registry",
    "ResourceId":
        "SanskritAI.core.resources.resource_id",
    "CorpusSource":
        "SanskritAI.acquisition.models.corpus_source",
    "CorpusSourceFactory":
        "SanskritAI.acquisition.factories.corpus_source_factory",
}

for name, module_name in imports.items():
    try:
        module = __import__(
            module_name,
            fromlist=[name],
        )
        obj = getattr(module, name)
        components[name] = obj

        print(f"{name:<24}: PASS")
        print(f"  module: {module_name}")
        print(f"  object: {obj}")

    except Exception as exc:
        print(f"{name:<24}: FAIL")
        print(f"  error: {exc!r}")


# ------------------------------------------------------------------
# 2. Work registry metadata
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("2. WORK REGISTRY METADATA")
print("-" * 120)

registry_path = (
    REPO_ROOT
    / "resources"
    / "work_registry.json"
)

amarakosha_definition = None

if registry_path.exists():

    try:
        data = json.loads(
            registry_path.read_text(
                encoding="utf-8"
            )
        )

        works = data.get("works", [])

        for work in works:
            if (
                str(work.get("identifier", "")).lower()
                == "amarakosha"
            ):
                amarakosha_definition = work
                break

        if amarakosha_definition:

            print("IDENTIFIER :", amarakosha_definition.get("identifier"))
            print("TITLE      :", amarakosha_definition.get("title"))
            print("CORPUS TYPE:", amarakosha_definition.get("corpus_type"))
            print("LANGUAGE   :", amarakosha_definition.get("language"))
            print("SCRIPT     :", amarakosha_definition.get("script"))
            print("REPOSITORY :", amarakosha_definition.get("repository"))
            print("ALIASES    :", amarakosha_definition.get("aliases"))
            print("METADATA   :", amarakosha_definition.get("metadata"))

        else:
            print("Amarakośa entry: NOT FOUND")

    except Exception as exc:
        print("Registry read error:", repr(exc))


# ------------------------------------------------------------------
# 3. WorkRegistry runtime API
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("3. WORK REGISTRY RUNTIME API")
print("-" * 120)

WorkRegistry = components.get("WorkRegistry")

if WorkRegistry is None:
    print("WorkRegistry unavailable.")
else:

    print("CLASS:", WorkRegistry)

    try:
        print("SIGNATURE:", inspect.signature(WorkRegistry))
    except Exception as exc:
        print("SIGNATURE: unavailable:", repr(exc))

    public_members = [
        name
        for name in dir(WorkRegistry)
        if not name.startswith("_")
    ]

    print("PUBLIC MEMBERS:")

    for name in public_members:
        try:
            value = getattr(WorkRegistry, name)

            if callable(value):
                try:
                    signature = inspect.signature(value)
                except Exception:
                    signature = "(signature unavailable)"

                print(
                    f"  {name}{signature}"
                )

            else:
                print(
                    f"  {name}: {value!r}"
                )

        except Exception:
            print(f"  {name}")


# ------------------------------------------------------------------
# 4. Instantiate WorkRegistry
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("4. WORK REGISTRY INSTANTIATION")
print("-" * 120)

registry = None

if WorkRegistry is not None:

    try:
        registry = WorkRegistry()
        print("WorkRegistry(): PASS")
        print("INSTANCE:", registry)

    except Exception as exc:
        print("WorkRegistry(): FAIL")
        print("ERROR:", repr(exc))


# ------------------------------------------------------------------
# 5. Resolve Amarakośa through WorkRegistry
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("5. AMARAKOSHA WORK RESOLUTION")
print("-" * 120)

resolved_work = None

if registry is not None:

    candidates = (
        "get",
        "find",
        "resolve",
        "lookup",
        "by_identifier",
    )

    for method_name in candidates:

        method = getattr(
            registry,
            method_name,
            None,
        )

        if method is None:
            continue

        try:
            result = method("amarakosha")

            print(
                f"{method_name}('amarakosha'): "
                f"RETURNED {result!r}"
            )

            if result is not None:
                resolved_work = result
                break

        except Exception as exc:
            print(
                f"{method_name}('amarakosha'): "
                f"ERROR {exc!r}"
            )


if resolved_work is None:
    print("Resolved WorkDefinition: NOT ESTABLISHED")
else:
    print("Resolved WorkDefinition:", resolved_work)


# ------------------------------------------------------------------
# 6. WorkDefinition structure
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("6. RESOLVED WORK STRUCTURE")
print("-" * 120)

if resolved_work is not None:

    print("TYPE:", type(resolved_work))

    for name in (
        "identifier",
        "title",
        "corpus_type",
        "language",
        "script",
        "repository",
        "aliases",
        "metadata",
    ):

        try:
            print(
                f"{name:<18}: "
                f"{getattr(resolved_work, name)!r}"
            )

        except Exception:
            pass


# ------------------------------------------------------------------
# 7. CorpusSourceFactory runtime API
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("7. CORPUS SOURCE FACTORY RUNTIME API")
print("-" * 120)

Factory = components.get("CorpusSourceFactory")

factory = None

if Factory is not None:

    print("CLASS:", Factory)

    try:
        print("SIGNATURE:", inspect.signature(Factory))
    except Exception as exc:
        print("SIGNATURE unavailable:", repr(exc))

    try:
        factory = Factory()
        print("CorpusSourceFactory(): PASS")
        print("INSTANCE:", factory)

    except Exception as exc:
        print("CorpusSourceFactory(): FAIL")
        print("ERROR:", repr(exc))

    for name in (
        "from_file",
        "from_url",
        "from_metadata",
        "is_supported",
    ):

        method = getattr(
            Factory,
            name,
            None,
        )

        if method is not None:

            try:
                print(
                    f"{name}{inspect.signature(method)}"
                )
            except Exception:
                print(name)


# ------------------------------------------------------------------
# 8. Attempt metadata → CorpusSource
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("8. WORK METADATA → CORPUS SOURCE")
print("-" * 120)

source = None

if (
    factory is not None
    and resolved_work is not None
):

    from_metadata = getattr(
        factory,
        "from_metadata",
        None,
    )

    if from_metadata is not None:

        metadata_candidates = [
            amarakosha_definition or {},
            {
                "identifier": "amarakosha",
                "name": "Amarakosha",
                "corpus_type": "dictionary",
                "language": "sanskrit",
            },
        ]

        for metadata in metadata_candidates:

            try:

                print(
                    "TRYING METADATA:",
                    metadata,
                )

                source = from_metadata(
                    metadata
                )

                print(
                    "from_metadata(): PASS"
                )

                print(
                    "CORPUS SOURCE:",
                    source,
                )

                break

            except Exception as exc:

                print(
                    "from_metadata(): ERROR"
                )

                print(
                    "ERROR:",
                    repr(exc),
                )

else:
    print(
        "Metadata → CorpusSource test "
        "could not be attempted."
    )


# ------------------------------------------------------------------
# 9. Inspect resulting CorpusSource
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("9. CORPUS SOURCE RESULT")
print("-" * 120)

if source is not None:

    print("TYPE:", type(source))

    for name in (
        "source_id",
        "name",
        "source_type",
        "source_format",
        "license",
        "version",
        "status",
        "download_urls",
        "local_path",
        "cache_directory",
    ):

        try:
            print(
                f"{name:<20}: "
                f"{getattr(source, name)!r}"
            )

        except Exception:
            pass

else:
    print(
        "No CorpusSource was produced."
    )


# ------------------------------------------------------------------
# 10. Check for actual acquisition URL
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("10. AMARAKOSHA ACQUISITION URL EVIDENCE")
print("-" * 120)

if source is not None:

    urls = []

    for attr in (
        "download_urls",
        "urls",
        "download_url",
    ):

        try:
            value = getattr(source, attr)

            if isinstance(value, str):
                urls.append(value)

            elif value:
                urls.extend(list(value))

        except Exception:
            pass

    urls = [
        str(url)
        for url in urls
        if str(url).strip()
    ]

    if urls:
        for url in urls:
            print(url)
    else:
        print(
            "CorpusSource contains no acquisition URL."
        )

else:
    print(
        "URL evidence unavailable because "
        "CorpusSource was not produced."
    )


# ------------------------------------------------------------------
# 11. Architectural gate
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("11. ARCHITECTURAL GATE")
print("-" * 120)

print(
    "WorkRegistry reused                    : "
    + ("YES" if registry is not None else "NO")
)

print(
    "Amarakośa WorkDefinition resolved       : "
    + ("YES" if resolved_work is not None else "NO")
)

print(
    "CorpusSourceFactory reused              : "
    + ("YES" if factory is not None else "NO")
)

print(
    "Work → CorpusSource runtime bridge      : "
    + ("YES" if source is not None else "NO")
)

print(
    "Actual Amarakośa acquisition URL        : "
    + (
        "YES"
        if source is not None
        and any(
            getattr(source, attr, None)
            for attr in (
                "download_urls",
                "download_url",
            )
        )
        else "NO"
    )
)

print(
    "New Amarakośa source class              : NOT JUSTIFIED"
)

print(
    "New Amarakośa provider                  : NOT JUSTIFIED"
)

print(
    "Parser grammar                           : DEFER"
)


# ------------------------------------------------------------------
# 12. Final decision
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("12. FINAL DECISION")
print("-" * 120)

if (
    resolved_work is not None
    and source is not None
):
    print(
        "WORK → CORPUS SOURCE RUNTIME BRIDGE : VERIFIED"
    )
else:
    print(
        "WORK → CORPUS SOURCE RUNTIME BRIDGE : NOT VERIFIED"
    )

print(
    "BATCH 5H-5E-10 STATUS: AUDIT COMPLETE"
)

print("=" * 120)
