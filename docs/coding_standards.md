# Coding Standards

- Keep models lightweight.
- Prefer dependency injection for services and plugin integrations.
- Put orchestration in `services/`.
- Keep source data in `data/raw/`, generated data in `data/processed/`,
  reference data in `data/reference/`, user data in `data/user/`, and
  static assets in `resources/`.
- Add tests for every module with non-trivial behavior.
