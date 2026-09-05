from SanskritAI.lexical.builders.lexeme_record_builder import (
    LexemeRecordBuilder,
)
from SanskritAI.lexical.enums.dictionary_source import (
    DictionarySource,
)
from SanskritAI.lexical.enums.language import (
    Language,
)
from SanskritAI.lexical.enums.script import (
    Script,
)
from SanskritAI.lexical.records.lexeme_record import (
    LexemeRecord,
)


def make_record(**overrides) -> LexemeRecord:
    values = {
        "identifier": "lex-001",
        "lemma": "धर्म",
        "normalized": "धर्म",
        "dictionary": DictionarySource.AMARAKOSHA,
        "language": Language.SANSKRIT,
        "script": Script.DEVANAGARI,
        "devanagari": "धर्म",
        "iast": "dharma",
        "transliteration": "dharma",
        "gloss": "duty",
        "tags": ("noun",),
        "notes": "",
    }

    values.update(overrides)

    return LexemeRecord(**values)


def test_build_validated_succeeds_for_valid_record():
    result = LexemeRecordBuilder().build_validated(
        make_record()
    )

    assert result.is_success
    assert result.has_object
    assert result.object is not None
    assert result.object.identifier == "lex-001"


def test_build_validated_rejects_invalid_record():
    result = LexemeRecordBuilder().build_validated(
        make_record(identifier="")
    )

    assert not result.is_success
    assert not result.has_object
    assert result.has_errors


def test_build_many_returns_build_results():
    builder = LexemeRecordBuilder()

    results = builder.build_many(
        [
            make_record(identifier="lex-001"),
            make_record(identifier="lex-002"),
        ]
    )

    assert len(results) == 2
    assert all(result.is_success for result in results)
