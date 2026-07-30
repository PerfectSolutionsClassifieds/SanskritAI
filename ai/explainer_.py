from __future__ import annotations

from models.analysis_result import AnalysisResult


def explain_result(result: AnalysisResult) -> str:
    known = [word for word in result.words if word.meaning]
    if not known:
        return "No dictionary meanings found yet."
    return "\n".join(f"{word.text}: {word.meaning}" for word in known)
