"""
Quick demonstration of the lexical layer.
"""

from tests.lexical.sample_lexemes import (
    create_rama,
    create_agni,
    create_gam,
)

for lexeme in (
    create_rama(),
    create_agni(),
    create_gam(),
):

    print("=" * 60)
    print(lexeme.lemma)
    print(lexeme.transliteration)

    for entry in lexeme.dictionary_entries:

        print(entry.dictionary_name)

        for sense in entry.senses:
            print("  -", sense.gloss)
