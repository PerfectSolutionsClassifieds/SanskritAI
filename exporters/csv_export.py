from __future__ import annotations

import csv
import io


def export_words_csv(words: list[dict]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["text", "lemma", "meaning", "pos"])
    writer.writeheader()
    writer.writerows({key: word.get(key) for key in writer.fieldnames} for word in words)
    return output.getvalue()
