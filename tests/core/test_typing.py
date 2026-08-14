from collections.abc import Callable, Iterable, Iterator, Mapping, MutableMapping, MutableSequence, MutableSet, Sequence
from pathlib import Path
from typing import Any, TypeVar
from SanskritAI.core.typing import (
    T,
    KT,
    VT,
    TNode,
    TChild,
    TMetadata,
    TIdentifier,
    TObject,
    JsonValue,
    JsonDict,
    PathLike,
    Attributes,
    Items,
    ItemIterator,
    MappingType,
    MutableMappingType,
    SequenceType,
    MutableSequenceType,
    MutableSetType,
    Factory,
    Predicate,
    Transformer,
    Consumer,
)


def test_generic_type_variables_exist():
    type_variables = (
        T,
        KT,
        VT,
        TNode,
        TChild,
        TMetadata,
        TIdentifier,
        TObject,
    )
    for type_variable in type_variables:
        assert isinstance(type_variable, TypeVar)


def test_tobject_is_exported():
    from SanskritAI.core.typing import __all__
    assert "TObject" in __all__


def test_tobject_is_unconstrained():
    assert TObject.__bound__ is None
    assert TObject.__constraints__ == ()


def test_json_aliases_exist():
    assert JsonValue is not None
    assert JsonDict is not None


def test_path_like_accepts_string_and_path():
    string_path: PathLike = "example/path"
    pathlib_path: PathLike = Path("example/path")
    assert isinstance(string_path, str)
    assert isinstance(pathlib_path, Path)


def test_attributes_is_dictionary():
    attributes: Attributes = {"lemma": "राम", "count": 1}
    assert isinstance(attributes, dict)
    assert attributes["lemma"] == "राम"


def test_collection_aliases_are_available():
    items: Items[int] = [1, 2, 3]
    iterator: ItemIterator[int] = iter(items)
    mapping: MappingType[str, int] = {"a": 1}
    mutable_mapping: MutableMappingType[str, int] = {"a": 1}
    sequence: SequenceType[int] = (1, 2, 3)
    mutable_sequence: MutableSequenceType[int] = [1, 2, 3]
    mutable_set: MutableSetType[int] = {1, 2, 3}

    assert isinstance(items, Iterable)
    assert isinstance(iterator, Iterator)
    assert isinstance(mapping, Mapping)
    assert isinstance(mutable_mapping, MutableMapping)
    assert isinstance(sequence, Sequence)
    assert isinstance(mutable_sequence, MutableSequence)
    assert isinstance(mutable_set, MutableSet)


def test_callable_aliases_are_available():
    def factory() -> int:
        return 1

    def predicate(value: int) -> bool:
        return value > 0

    def transformer(value: int) -> int:
        return value + 1

    def consumer(value: int) -> None:
        return None

    factory_value: Factory[int] = factory
    predicate_value: Predicate[int] = predicate
    transformer_value: Transformer[int] = transformer
    consumer_value: Consumer[int] = consumer

    assert callable(factory_value)
    assert callable(predicate_value)
    assert callable(transformer_value)
    assert callable(consumer_value)


def test_all_expected_symbols_are_exported():
    from SanskritAI.core.typing import __all__

    expected = {
        "T",
        "KT",
        "VT",
        "TNode",
        "TChild",
        "TMetadata",
        "TIdentifier",
        "TObject",
        "JsonValue",
        "JsonDict",
        "PathLike",
        "Attributes",
        "Items",
        "ItemIterator",
        "MappingType",
        "MutableMappingType",
        "SequenceType",
        "MutableSequenceType",
        "MutableSetType",
        "Factory",
        "Predicate",
        "Transformer",
        "Consumer",
    }

    assert set(__all__) == expected


def test_json_dict_accepts_json_compatible_values():
    value: JsonDict = {
        "string": "value",
        "integer": 1,
        "float": 1.5,
        "boolean": True,
        "null": None,
        "list": [1, "two", False],
        "nested": {"key": "value"},
    }

    assert value["string"] == "value"
    assert value["integer"] == 1
    assert value["nested"] == {"key": "value"}
