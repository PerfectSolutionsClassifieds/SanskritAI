from __future__ import annotations


class CorpusRepository:
    def __init__(self):
        self._records: list[dict] = []

    def add(self, record: dict) -> None:
        self._records.append(record)

    def search(self, query: str) -> list[dict]:
        return [record for record in self._records if query in str(record)]
