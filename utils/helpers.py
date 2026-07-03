from __future__ import annotations


def compact_none(data: dict) -> dict:
    return {key: value for key, value in data.items() if value is not None}
