
from __future__ import annotations

"""
SanskritAI
==========

Prototype Reader Utility
(Install : !pip install indic_transliteration)

A reader-facing lexical preview utility for Sanskrit ślokas.

This script is intentionally heuristic and prototype-oriented.
It is NOT a canonical grammar engine.

It performs:
- tokenization
- light normalization
- simple heuristic root guessing
- Wiktionary lookup
- readable lexical preview output

The long-term canonical grammar and lexicon work belongs to
the Sanskrit Domain Layer.

Version
-------
v0.1.0
"""

from dataclasses import dataclass
import re
import string
from functools import lru_cache
from typing import Any

import requests
from indic_transliteration import sanscript


SLOKA_IAST = "vidyā dadāti vinayam vinayād yāti pātratām"


@dataclass(frozen=True, slots=True)
class LexicalPreviewResult:
    token_index: int
    token_iast: str
    root_guess_iast: str
    word_devanagari: str
    meaning_grammar: str
    found_sanskrit_entry: bool


def tokenize_iast(text: str) -> list[str]:
    words = text.split()
    return [word.strip(string.punctuation).lower() for word in words if word.strip()]


def guess_root_iast(word_iast: str) -> str:
    """
    Very small heuristic stemmer.

    This is intentionally approximate and should be treated as
    a prototype preview aid only.
    """
    root_iast = word_iast

    if word_iast.endswith("tām"):
        root_iast = word_iast[:-3]
    elif word_iast.endswith("ād"):
        root_iast = word_iast[:-2] + "a"
    elif word_iast.endswith("ām"):
        root_iast = word_iast[:-2] + "ā"
    elif word_iast.endswith("am"):
        root_iast = word_iast[:-2] + "a"
    elif word_iast.endswith("ena"):
        root_iast = word_iast[:-4] + "a"
    elif word_iast.endswith("asya"):
        root_iast = word_iast[:-4] + "a"

    return root_iast


def iast_to_devanagari(text_iast: str) -> str:
    return sanscript.transliterate(
        text_iast,
        sanscript.IAST,
        sanscript.DEVANAGARI,
    )


@lru_cache(maxsize=256)
def fetch_wiktionary_extract(word_deva: str) -> str:
    url = "https://en.wiktionary.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": word_deva,
        "prop": "extracts",
        "explaintext": True,
    }
    headers = {
        "User-Agent": "SanskritAI-PrototypeReader/0.1 "
        "(https://github.com/openai)"
    }

    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    for page_id, page_info in pages.items():
        if page_id == "-1":
            continue
        return page_info.get("extract", "")

    return ""


def extract_sanskrit_section(extract: str) -> tuple[bool, str]:
    """
    Returns:
        (found_sanskrit_section, cleaned_preview_text)
    """
    if not extract:
        return False, ""

    if not re.search(r"==\s*Sanskrit\s*==", extract):
        return False, ""

    sanskrit_part = re.split(r"==\s*Sanskrit\s*==", extract, maxsplit=1)[1]
    sanskrit_section = re.split(r"\n==\s*[A-Za-z]+", sanskrit_part, maxsplit=1)[0]

    lines: list[str] = []
    for line in sanskrit_section.split("\n"):
        line = line.strip()
        if not line:
            continue
        clean_line = re.sub(r"=+", "", line).strip()
        if clean_line:
            lines.append(clean_line)

    formatted_preview = "\n    ".join(lines[:8])
    return True, formatted_preview


def analyze_sloka_with_readable_definitions(
    sloka_iast: str = SLOKA_IAST,
) -> list[LexicalPreviewResult]:
    print("==================================================")
    print("Prototype Reader Utility")
    print(f"Embedded Sloka : {sloka_iast}")
    print("==================================================\n")

    print("Querying the Wikimedia/Wiktionary API...\n")

    results: list[LexicalPreviewResult] = []
    words = tokenize_iast(sloka_iast)

    for index, word_iast in enumerate(words, start=1):
        root_iast = guess_root_iast(word_iast)
        word_deva = iast_to_devanagari(root_iast)

        print(
            f"--- Token {index}: {word_iast} "
            f"-> Root searched: {root_iast} ({word_deva}) ---"
        )

        try:
            extract = fetch_wiktionary_extract(word_deva)
            found_sanskrit, formatted_preview = extract_sanskrit_section(extract)

            if found_sanskrit:
                print(f"Meaning & Grammar:\n    {formatted_preview}\n")
                results.append(
                    LexicalPreviewResult(
                        token_index=index,
                        token_iast=word_iast,
                        root_guess_iast=root_iast,
                        word_devanagari=word_deva,
                        meaning_grammar=formatted_preview,
                        found_sanskrit_entry=True,
                    )
                )
            else:
                print(f"No direct Sanskrit entry found for '{word_deva}'.\n")
                results.append(
                    LexicalPreviewResult(
                        token_index=index,
                        token_iast=word_iast,
                        root_guess_iast=root_iast,
                        word_devanagari=word_deva,
                        meaning_grammar="",
                        found_sanskrit_entry=False,
                    )
                )

        except requests.exceptions.Timeout:
            print("Error: The request timed out.\n")
            results.append(
                LexicalPreviewResult(
                    token_index=index,
                    token_iast=word_iast,
                    root_guess_iast=root_iast,
                    word_devanagari=word_deva,
                    meaning_grammar="",
                    found_sanskrit_entry=False,
                )
            )
        except requests.exceptions.RequestException as e:
            print(f"Network Error: {e}\n")
            results.append(
                LexicalPreviewResult(
                    token_index=index,
                    token_iast=word_iast,
                    root_guess_iast=root_iast,
                    word_devanagari=word_deva,
                    meaning_grammar="",
                    found_sanskrit_entry=False,
                )
            )
        except Exception as e:
            print(f"Unexpected Error: {e}\n")
            results.append(
                LexicalPreviewResult(
                    token_index=index,
                    token_iast=word_iast,
                    root_guess_iast=root_iast,
                    word_devanagari=word_deva,
                    meaning_grammar="",
                    found_sanskrit_entry=False,
                )
            )

    return results


if __name__ == "__main__":
    analyze_sloka_with_readable_definitions()
