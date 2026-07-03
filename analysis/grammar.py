from __future__ import annotations


def summarize_grammar(features: dict) -> str:
    return ", ".join(f"{key}={value}" for key, value in features.items())
