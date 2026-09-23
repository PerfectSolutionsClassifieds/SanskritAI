
from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path("/content/SanskritAI").resolve()
REPO_PARENT = REPO_ROOT.parent.resolve()


print("=" * 72)
print("13R-8E-0 — SanskritAI runtime bootstrap audit")
print("=" * 72)

print(f"Repository root : {REPO_ROOT}")
print(f"Repository parent : {REPO_PARENT}")

if not REPO_ROOT.exists():
    raise SystemExit("ABORT — repository root does not exist.")

if not (REPO_ROOT / "__init__.py").exists():
    raise SystemExit(
        "ABORT — SanskritAI package marker __init__.py not found."
    )

# When executing a script by absolute path, Python places the script's
# directory on sys.path, not necessarily the repository parent.
if str(REPO_PARENT) not in sys.path:
    sys.path.insert(0, str(REPO_PARENT))

print()
print("sys.path bootstrap : PASS")

try:
    import SanskritAI

    print(f"SanskritAI import : PASS")
    print(f"SanskritAI path   : {getattr(SanskritAI, '__file__', None)}")
except Exception as exc:
    print(f"SanskritAI import : FAIL — {exc}")
    raise SystemExit(1)

targets = [
    "SanskritAI.acquisition.downloaders.local_file_importer",
    "SanskritAI.acquisition.acquirers.default_source_acquirer",
    "SanskritAI.acquisition.pipelines.acquisition_pipeline",
    "SanskritAI.acquisition.services.default_acquisition_service",
]

print()
print("-" * 72)
print("Target runtime imports")
print("-" * 72)

failed = []

for target in targets:
    try:
        __import__(target)
        print(f"{target} : PASS")
    except Exception as exc:
        print(f"{target} : FAIL — {exc}")
        failed.append((target, exc))

print()
print("-" * 72)

if failed:
    print("RESULT: FAIL — runtime package bootstrap/import remains unresolved.")
    raise SystemExit(1)

print("RESULT: PASS — runtime package bootstrap is valid.")
