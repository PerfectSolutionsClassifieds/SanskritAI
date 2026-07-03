from __future__ import annotations


class DatabaseConnection:
    def __init__(self, dsn: str | None = None):
        self.dsn = dsn

    def connect(self):
        if not self.dsn:
            raise ValueError("Database DSN is required.")
        raise NotImplementedError("Add a database driver before opening connections.")
