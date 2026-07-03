# Architecture

SanskritAI uses one architecture style:

- `core/` contains configuration, constants, and exceptions.
- `models/` contains lightweight data objects only.
- `interfaces/` defines contracts for interchangeable implementations.
- `services/` orchestrates workflows and owns business logic.
- `pipeline/` owns execution order for analysis workflows.
- `registry/` handles plugin and analyzer discovery.
- `input/`, `analysis/`, `lexicon/`, `storage/`, `exporters/`, and `ai/`
  contain focused implementation details.
- `data/raw`, `data/processed`, `data/reference`, and `data/user`
  keep source, generated, bundled, and user-owned data separate.

Do not add `engine/`, a separate `config/`, or duplicate model names such as
`models/analysis.py`.
