# SanskritAI

SanskritAI is a starter Sanskrit knowledge platform.

The architecture is intentionally frozen around one style:

- `core/` for configuration, constants, and exceptions
- `models/` for lightweight data objects
- `interfaces/` for abstract contracts
- `services/` for orchestration and business logic
- `input/`, `analysis/`, `lexicon/`, `storage/`, `exporters/`, and `ai/` for focused implementation modules

Legacy alternatives such as `engine/`, a separate `config/`, or `models/analysis.py`
are deliberately not generated.

## Quick Start

```bash
python main.py "धर्म कर्म"
python -m pytest
```

## Current Features

- Sanskrit text normalization
- Devanagari and IAST-aware tokenization
- Dictionary-backed lexical lookup
- Lightweight morphology result model
- JSON export of analysis results
- CSV-to-JSON dictionary builder
