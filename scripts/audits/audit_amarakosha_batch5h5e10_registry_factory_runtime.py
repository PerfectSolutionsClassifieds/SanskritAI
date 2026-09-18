from __future__ import annotations

from pathlib import Path
import inspect
import json
import sys

REPO_ROOT = Path("/content/SanskritAI")

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

print("=" * 120)
print(
    "BATCH 5H-5E-10R — "
    "AMARAKOSHA WORK REGISTRY → CORPUS SOURCE FACTORY RUNTIME BRIDGE"
)
print("=" * 120)


# ------------------------------------------------------------------
# 1. Production imports
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("1. PRODUCTION COMPONENT IMPORTS")
print("-" * 120)

components = {}

IMPORTS = {
    "WorkDefinition": (
        "acquisition.metadata.models.work_definition",
        "WorkDefinition",
    ),
    "WorkRegistry": (
        "acquisition.metadata.registries.work_registry",
        "WorkRegistry",
    ),
    "ResourceId": (
        "core.resources.resource_id",
        "ResourceId",
    ),
    "CorpusSource": (
        "acquisition.models.corpus_source",
        "CorpusSource",
    ),
    "CorpusSourceFactory": (
        "acquisition.factories.corpus_source_factory",
        "CorpusSourceFactory",
    ),
}


for name, (module_name, object_name) in IMPORTS.items():

    try:
        module = __import__(
            module_name,
            fromlist=[object_name],
        )

        obj = getattr(
            module,
            object_name,
        )

        components[name] = obj

        print(f"{name:<24}: PASS")
        print(f"  module: {module_name}")
        print(f"  object: {obj}")

    except Exception as exc:

        print(f"{name:<24}: FAIL")
        print(f"  module: {module_name}")
        print(f"  error : {exc!r}")


# ------------------------------------------------------------------
# 2. Work registry artifact
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("2. AMARAKOSHA WORK REGISTRY ARTIFACT")
print("-" * 120)

registry_path = (
    REPO_ROOT
    / "resources"
    / "work_registry.json"
)

amarakosha_definition = None

if not registry_path.exists():

    print(
        "STATUS: work_registry.json NOT FOUND"
    )

else:

    try:

        data = json.loads(
            registry_path.read_text(
                encoding="utf-8"
            )
        )

        works = data.get(
            "works",
            []
        )

        for work in works:

            if (
                str(
                    work.get(
                        "identifier",
                        ""
                    )
                ).lower()
                == "amarakosha"
            ):

                amarakosha_definition = work
                break

        if amarakosha_definition:

            print(
                "IDENTIFIER :",
                amarakosha_definition.get("identifier")
            )

            print(
                "TITLE      :",
                amarakosha_definition.get("title")
            )

            print(
                "CORPUS TYPE:",
                amarakosha_definition.get("corpus_type")
            )

            print(
                "LANGUAGE   :",
                amarakosha_definition.get("language")
            )

            print(
                "SCRIPT     :",
                amarakosha_definition.get("script")
            )

            print(
                "REPOSITORY :",
                amarakosha_definition.get("repository")
            )

            print(
                "ALIASES    :",
                amarakosha_definition.get("aliases")
            )

            print(
                "METADATA   :",
                amarakosha_definition.get("metadata")
            )

        else:

            print(
                "Amarakośa registry entry: NOT FOUND"
            )

    except Exception as exc:

        print(
            "Registry error:",
            repr(exc)
        )


# ------------------------------------------------------------------
# 3. WorkRegistry API
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("3. WORK REGISTRY RUNTIME API")
print("-" * 120)

WorkRegistry = components.get(
    "WorkRegistry"
)

registry = None

if WorkRegistry is None:

    print(
        "WorkRegistry unavailable."
    )

else:

    print(
        "CLASS:",
        WorkRegistry
    )

    try:

        print(
            "CLASS SIGNATURE:",
            inspect.signature(WorkRegistry)
        )

    except Exception as exc:

        print(
            "CLASS SIGNATURE: unavailable:",
            repr(exc)
        )

    print(
        "PUBLIC MEMBERS:"
    )

    for name in dir(WorkRegistry):

        if name.startswith("_"):
            continue

        try:

            value = getattr(
                WorkRegistry,
                name
            )

            if callable(value):

                try:
                    signature = inspect.signature(
                        value
                    )
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

            print(
                f"  {name}"
            )

    # Try normal construction.
    try:

        registry = WorkRegistry()

        print(
            "WorkRegistry(): PASS"
        )

        print(
            "INSTANCE:",
            registry
        )

    except Exception as exc:

        print(
            "WorkRegistry(): FAIL"
        )

        print(
            "ERROR:",
            repr(exc)
        )


# ------------------------------------------------------------------
# 4. Resolve Amarakośa through WorkRegistry
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("4. AMARAKOSHA WORK RESOLUTION")
print("-" * 120)

resolved_work = None
resolution_method = None

if registry is not None:

    candidate_methods = (
        "get",
        "find",
        "resolve",
        "lookup",
        "by_identifier",
    )

    for method_name in candidate_methods:

        method = getattr(
            registry,
            method_name,
            None
        )

        if method is None:
            continue

        try:

            result = method(
                "amarakosha"
            )

            print(
                f"{method_name}('amarakosha') "
                f"→ {result!r}"
            )

            if result is not None:

                resolved_work = result
                resolution_method = method_name
                break

        except Exception as exc:

            print(
                f"{method_name}('amarakosha') "
                f"→ ERROR {exc!r}"
            )


if resolved_work is None:

    print(
        "Resolved WorkDefinition: NOT ESTABLISHED"
    )

else:

    print(
        "Resolved WorkDefinition: ESTABLISHED"
    )

    print(
        "Resolution method:",
        resolution_method
    )

    print(
        "TYPE:",
        type(resolved_work)
    )


# ------------------------------------------------------------------
# 5. Inspect resolved WorkDefinition
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("5. RESOLVED WORK DEFINITION")
print("-" * 120)

if resolved_work is not None:

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

else:

    print(
        "No WorkDefinition object to inspect."
    )


# ------------------------------------------------------------------
# 6. CorpusSourceFactory API
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("6. CORPUS SOURCE FACTORY RUNTIME API")
print("-" * 120)

Factory = components.get(
    "CorpusSourceFactory"
)

factory = None

if Factory is None:

    print(
        "CorpusSourceFactory unavailable."
    )

else:

    print(
        "CLASS:",
        Factory
    )

    try:

        print(
            "CLASS SIGNATURE:",
            inspect.signature(Factory)
        )

    except Exception as exc:

        print(
            "CLASS SIGNATURE: unavailable:",
            repr(exc)
        )

    try:

        factory = Factory()

        print(
            "CorpusSourceFactory(): PASS"
        )

    except Exception as exc:

        print(
            "CorpusSourceFactory(): FAIL"
        )

        print(
            "ERROR:",
            repr(exc)
        )

    for method_name in (
        "from_file",
        "from_url",
        "from_metadata",
        "is_supported",
    ):

        method = getattr(
            Factory,
            method_name,
            None
        )

        if method is not None:

            try:

                print(
                    f"{method_name}"
                    f"{inspect.signature(method)}"
                )

            except Exception:

                print(
                    method_name
                )


# ------------------------------------------------------------------
# 7. WorkDefinition → CorpusSourceFactory
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("7. WORK DEFINITION → CORPUS SOURCE FACTORY")
print("-" * 120)

source = None

if (
    factory is not None
    and resolved_work is not None
):

    method = getattr(
        Factory,
        "from_metadata",
        None
    )

    if method is None:

        print(
            "CorpusSourceFactory.from_metadata "
            "does not exist."
        )

    else:

        # IMPORTANT:
        # This is a runtime compatibility probe only.
        # It does not mutate production state.

        metadata = (
            amarakosha_definition
            if amarakosha_definition is not None
            else {}
        )

        print(
            "METADATA INPUT:"
        )

        print(
            metadata
        )

        try:

            source = method(
                metadata
            )

            print(
                "from_metadata(metadata): PASS"
            )

            print(
                "RESULT:",
                source
            )

        except Exception as exc:

            print(
                "from_metadata(metadata): "
                "NOT COMPATIBLE"
            )

            print(
                "ERROR:",
                repr(exc)
            )

else:

    print(
        "Work → CorpusSourceFactory "
        "probe could not be attempted."
    )


# ------------------------------------------------------------------
# 8. CorpusSource result
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("8. CORPUS SOURCE RESULT")
print("-" * 120)

if source is None:

    print(
        "CorpusSource: NOT PRODUCED"
    )

else:

    print(
        "CorpusSource: PRODUCED"
    )

    print(
        "TYPE:",
        type(source)
    )

    for name in (
        "source_id",
        "name",
        "source_type",
        "source_format",
        "license",
        "version",
        "status",
        "download_urls",
        "download_url",
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


# ------------------------------------------------------------------
# 9. Acquisition URL evidence
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("9. ACQUISITION URL EVIDENCE")
print("-" * 120)

urls = []

if source is not None:

    for name in (
        "download_urls",
        "download_url",
        "urls",
    ):

        try:

            value = getattr(
                source,
                name
            )

        except Exception:

            continue

        if isinstance(value, str):

            if value.strip():
                urls.append(value)

        elif value:

            try:
                urls.extend(
                    list(value)
                )
            except Exception:
                pass


urls = sorted(
    {
        str(url).strip()
        for url in urls
        if str(url).strip()
    }
)

if urls:

    for url in urls:
        print(
            url
        )

else:

    print(
        "No acquisition URL present."
    )


# ------------------------------------------------------------------
# 10. Architectural gate
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("10. ARCHITECTURAL GATE")
print("-" * 120)

print(
    "WorkDefinition model                  : PRESERVE"
)

print(
    "ResourceId model                      : PRESERVE"
)

print(
    "work_registry.json                    : PRESERVE"
)

print(
    "WorkRegistry                          : PRESERVE"
)

print(
    "CorpusSourceFactory                   : PRESERVE"
)

print(
    "CorpusSource                          : PRESERVE"
)

print(
    "AcquisitionManifest                   : PRESERVE"
)

print(
    "New Amarakośa source class            : NOT JUSTIFIED"
)

print(
    "New Amarakośa provider                : NOT JUSTIFIED"
)

print(
    "Parser grammar                        : DEFER"
)

print(
    "Production modification               : NONE"
)


# ------------------------------------------------------------------
# 11. Final decision
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("11. FINAL DECISION")
print("-" * 120)

if (
    registry is not None
    and resolved_work is not None
):

    print(
        "WorkRegistry → WorkDefinition : VERIFIED"
    )

else:

    print(
        "WorkRegistry → WorkDefinition : NOT VERIFIED"
    )


if source is not None:

    print(
        "WorkDefinition → CorpusSource : VERIFIED"
    )

else:

    print(
        "WorkDefinition → CorpusSource : NOT VERIFIED"
    )


if urls:

    print(
        "CorpusSource → acquisition URL : PRESENT"
    )

else:

    print(
        "CorpusSource → acquisition URL : ABSENT"
    )


print(
    "\nBATCH 5H-5E-10R STATUS: AUDIT COMPLETE"
)

print("=" * 120)
