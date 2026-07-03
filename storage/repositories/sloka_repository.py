from __future__ import annotations

from models.sloka import Sloka


class SlokaRepository:
    def __init__(self):
        self._items: list[Sloka] = []

    def add(self, sloka: Sloka) -> None:
        self._items.append(sloka)

    def all(self) -> list[Sloka]:
        return list(self._items)
