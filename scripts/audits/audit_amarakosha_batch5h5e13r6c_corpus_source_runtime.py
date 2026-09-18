from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path("/content/SanskritAI")

if str(REPO_ROOT.parent) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT.parent))

from SanskritAI.acquisition.models.source_format import SourceFormat
from SanskritAI.acquisition.models.source_status import SourceStatus
from SanskritAI.acquisition.models.source_type import SourceType
from SanskritAI.acquisition.sources.amarakosha import (
    AMARAKOSHA_ARTIFACT,
    AMARAKOSHA_NAME,
    AMARAKOSHA_SHA256,
    AMARAKOSHA_SOURCE_ID,
    create_amarakosha_source,
)


print("=" * 100)
print("BATCH 5H-5E-13R-6C — AMARAKOSHA CORPUSSOURCE RUNTIME CONTRACT")
print("=" * 100)

source = create_amarakosha_source()

print()
print("SOURCE OBJECT")
print("-------------")
print(source)

print()
print("CANONICAL IDENTITY")
print("------------------")

print("source_id     :", source.source_id)
print("name          :", source.name)
print("source_type   :", source.source_type)
print("source_format :", source.source_format)
print("status        :", source.status)
print("local_path    :", source.local_path)
print("download_urls :", source.download_urls)
print("checksum      :", source.checksum)

print()
print("CONTRACT ASSERTIONS")
print("-------------------")

assert source.source_id == AMARAKOSHA_SOURCE_ID
print("source_id == 'amarakosha' : PASS")

assert source.name == AMARAKOSHA_NAME
print("name == 'Amarakośa' : PASS")

assert source.source_type == SourceType.LEXICON
print("source_type == LEXICON : PASS")

assert source.source_format == SourceFormat.TXT
print("source_format == TXT : PASS")

assert source.status == SourceStatus.REGISTERED
print("status == REGISTERED : PASS")

assert Path(source.local_path) == AMARAKOSHA_ARTIFACT
print("local_path == amarakośa.txt : PASS")

assert AMARAKOSHA_ARTIFACT.exists()
print("artifact exists : PASS")

assert source.checksum == AMARAKOSHA_SHA256
print("checksum == verified SHA-256 : PASS")

assert not source.download_urls
print("download_urls empty : PASS")

metadata = source.metadata or {}

assert metadata.get("encoding") == "utf-8"
print("metadata.encoding == utf-8 : PASS")

assert metadata.get("sha256") == AMARAKOSHA_SHA256
print("metadata.sha256 == verified SHA-256 : PASS")

assert metadata.get("provenance_url") == (
    "http://sanskrit.uohyd.ac.in/scl/"
)
print("embedded provenance URL preserved : PASS")

print()
print("=" * 100)
print("BATCH 5H-5E-13R-6C RESULT : PASS")
print("=" * 100)
