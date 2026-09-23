from pathlib import Path
import sys
import inspect

REPO_ROOT = Path("/content/SanskritAI").resolve()
WORKSPACE_ROOT = REPO_ROOT.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

print("=" * 72)
print("13R-8E-1A — AcquisitionResult contract audit")
print("=" * 72)

from SanskritAI.acquisition.models.acquisition_result import AcquisitionResult

print()
print("Module")
print("-" * 72)
print("module :", AcquisitionResult.__module__)
print("class  :", AcquisitionResult.__name__)

print()
print("Dataclass / object fields")
print("-" * 72)

fields = getattr(AcquisitionResult, "__dataclass_fields__", {})
if fields:
    for name, field in fields.items():
        print(f"{name:30} type={field.type!r} default={field.default!r}")
else:
    print("No dataclass fields detected.")

print()
print("Class attributes")
print("-" * 72)

for name in sorted(dir(AcquisitionResult)):
    if name.startswith("_"):
        continue
    try:
        value = getattr(AcquisitionResult, name)
    except Exception:
        continue

    if callable(value):
        print(f"METHOD   {name}")
    else:
        print(f"ATTRIBUTE {name} = {value!r}")

print()
print("Constructor signature")
print("-" * 72)
print(inspect.signature(AcquisitionResult))

print()
print("Method signatures")
print("-" * 72)

for name in sorted(dir(AcquisitionResult)):
    if name.startswith("_"):
        continue

    value = getattr(AcquisitionResult, name, None)

    if callable(value):
        try:
            print(f"{name}{inspect.signature(value)}")
        except (TypeError, ValueError):
            print(name)

print()
print("status attribute exists :", hasattr(AcquisitionResult, "status"))
print("success attribute exists:", hasattr(AcquisitionResult, "success"))
print("error attribute exists  :", hasattr(AcquisitionResult, "error"))
print("message attribute exists:", hasattr(AcquisitionResult, "message"))
print("result attribute exists :", hasattr(AcquisitionResult, "result"))

print()
print("RESULT: PASS — actual AcquisitionResult contract inspected.")
print("=" * 72)
