from __future__ import annotations


def infer_karaka(features: dict) -> str | None:
    return features.get("karaka")
