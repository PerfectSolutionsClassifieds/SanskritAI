from __future__ import annotations

from pathlib import Path
import importlib
import sys

REPO_ROOT = Path("/content/SanskritAI")
REPO_PARENT = REPO_ROOT.parent

print("=" * 120)
print("BATCH 5H-5E-10R-1 — SANSKRITAI RUNTIME PACKAGE BOOTSTRAP AUDIT")
print("=" * 120)

# ------------------------------------------------------------------
# 1. Filesystem identity
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("1. REPOSITORY / PACKAGE IDENTITY")
print("-" * 120)

print("REPO_ROOT   :", REPO_ROOT)
print("REPO_PARENT :", REPO_PARENT)
print("REPO_EXISTS :", REPO_ROOT.exists())

print(
    "ROOT __init__.py:",
    (REPO_ROOT / "__init__.py").exists()
)

print(
    "acquisition/__init__.py:",
    (REPO_ROOT / "acquisition" / "__init__.py").exists()
)

print(
    "core/__init__.py:",
    (REPO_ROOT / "core" / "__init__.py").exists()
)


# ------------------------------------------------------------------
# 2. Current Python path
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("2. CURRENT PYTHON PATH")
print("-" * 120)

for index, item in enumerate(sys.path):
    print(f"{index:>3}: {item}")


# ------------------------------------------------------------------
# 3. Bootstrap correct parent
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("3. BOOTSTRAP /content")
print("-" * 120)

if str(REPO_PARENT) not in sys.path:
    sys.path.insert(0, str(REPO_PARENT))

print(
    "Inserted parent path:",
    REPO_PARENT
)

print(
    "Parent available:",
    str(REPO_PARENT) in sys.path
)


# ------------------------------------------------------------------
# 4. SanskritAI package import
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("4. SanskritAI PACKAGE IMPORT")
print("-" * 120)

try:

    SanskritAI = importlib.import_module(
        "SanskritAI"
    )

    print(
        "SanskritAI import: PASS"
    )

    print(
        "MODULE:",
        SanskritAI
    )

    print(
        "FILE:",
        getattr(
            SanskritAI,
            "__file__",
            None
        )
    )

    print(
        "PATH:",
        getattr(
            SanskritAI,
            "__path__",
            None
        )
    )

except Exception as exc:

    print(
        "SanskritAI import: FAIL"
    )

    print(
        "ERROR:",
        repr(exc)
    )


# ------------------------------------------------------------------
# 5. Production component imports
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("5. PRODUCTION COMPONENT IMPORTS")
print("-" * 120)

TARGETS = {
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

loaded = {}

for name, module_name in TARGETS.items():

    try:

        module = importlib.import_module(
            module_name
        )

        loaded[name] = module

        print(
            f"{name:<24}: PASS"
        )

        print(
            f"  module: {module_name}"
        )

        print(
            f"  file  : {getattr(module, '__file__', None)}"
        )

    except Exception as exc:

        print(
            f"{name:<24}: FAIL"
        )

        print(
            f"  module: {module_name}"
        )

        print(
            f"  error : {exc!r}"
        )


# ------------------------------------------------------------------
# 6. Production object imports
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("6. PRODUCTION OBJECT IMPORTS")
print("-" * 120)

OBJECT_TARGETS = {
    "WorkDefinition": (
        "SanskritAI.acquisition.metadata.models.work_definition",
        "WorkDefinition",
    ),

    "WorkRegistry": (
        "SanskritAI.acquisition.metadata.registries.work_registry",
        "WorkRegistry",
    ),

    "ResourceId": (
        "SanskritAI.core.resources.resource_id",
        "ResourceId",
    ),

    "CorpusSource": (
        "SanskritAI.acquisition.models.corpus_source",
        "CorpusSource",
    ),

    "CorpusSourceFactory": (
        "SanskritAI.acquisition.factories.corpus_source_factory",
        "CorpusSourceFactory",
    ),
}

objects = {}

for name, (
    module_name,
    object_name,
) in OBJECT_TARGETS.items():

    try:

        module = importlib.import_module(
            module_name
        )

        obj = getattr(
            module,
            object_name
        )

        objects[name] = obj

        print(
            f"{name:<24}: PASS"
        )

        print(
            f"  object: {obj}"
        )

    except Exception as exc:

        print(
            f"{name:<24}: FAIL"
        )

        print(
            f"  error : {exc!r}"
        )


# ------------------------------------------------------------------
# 7. WorkRegistry construction only
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("7. WORK REGISTRY CONSTRUCTION")
print("-" * 120)

WorkRegistry = objects.get(
    "WorkRegistry"
)

if WorkRegistry is None:

    print(
        "WorkRegistry unavailable."
    )

else:

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
# 8. Final decision
# ------------------------------------------------------------------

print("\n" + "-" * 120)
print("8. FINAL DECISION")
print("-" * 120)

if (
    "WorkRegistry" in objects
    and "WorkDefinition" in objects
    and "CorpusSource" in objects
    and "CorpusSourceFactory" in objects
):

    print(
        "SanskritAI runtime bootstrap : VERIFIED"
    )

    print(
        "Production import boundary   : VERIFIED"
    )

    print(
        "Next audit                   : WORK REGISTRY RUNTIME TRACE"
    )

else:

    print(
        "SanskritAI runtime bootstrap : NOT VERIFIED"
    )

    print(
        "Production import boundary   : NOT VERIFIED"
    )

    print(
        "Production architecture      : DO NOT MODIFY"
    )

    print(
        "Next step                    : FIX AUDIT BOOTSTRAP ONLY"
    )

print(
    "\nBATCH 5H-5E-10R-1 STATUS: AUDIT COMPLETE"
)

print("=" * 120)
