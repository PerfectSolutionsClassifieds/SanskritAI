
from __future__ import annotations

import inspect

from SanskritAI.amarakosha.builders.synset_record_builder import (
    SynsetRecordBuilder,
)

print("=" * 110)
print("BATCH 5H-4A — CURRENT SYNSET RECORD BUILDER CONTRACT")
print("=" * 110)

print("\nCLASS:")
print(SynsetRecordBuilder)
print("MRO:")
for cls in inspect.getmro(SynsetRecordBuilder):
    print("  ", cls)

print("\nSIGNATURE:")
print(inspect.signature(SynsetRecordBuilder))

print("\nSOURCE:")
print(inspect.getsource(SynsetRecordBuilder))

print("\nBUILD SIGNATURE:")
print(inspect.signature(SynsetRecordBuilder.build))

print("\nBUILD SOURCE:")
print(inspect.getsource(SynsetRecordBuilder.build))

print("\nPUBLIC METHODS:")
for name in sorted(
    name
    for name in dir(SynsetRecordBuilder)
    if not name.startswith("_")
):
    try:
        attribute = getattr(SynsetRecordBuilder, name)
        if callable(attribute):
            print(f"  {name}{inspect.signature(attribute)}")
        else:
            print(f"  {name}")
    except Exception:
        print(f"  {name}")

print("\n" + "=" * 110)
print("BATCH 5H-4A COMPLETE")
print("=" * 110)
