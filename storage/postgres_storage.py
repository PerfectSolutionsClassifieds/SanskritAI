from __future__ import annotations


class PostgresStorage:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def connect(self):
        raise NotImplementedError("Install and configure psycopg before using Postgres storage.")
