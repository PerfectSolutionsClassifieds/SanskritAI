
from SanskritAI.acquisition.lexical.monier_williams import (
    DelimitedMonierWilliamsParser,
    MonierWilliamsSourceAcquirer,
    MonierWilliamsSourceParser,
)


class StubAcquirer(MonierWilliamsSourceAcquirer):

    def __init__(self, text):
        self.text = text
        self.called = False

    def acquire(self):
        self.called = True
        return self.text


def test_source_parser_acquires_then_parses():
    acquirer = StubAcquirer(
        "headword\tdefinition\n"
        "rāma\tpleasing\n"
    )

    parser = MonierWilliamsSourceParser(
        acquirer=acquirer,
    )

    entries = parser.parse()

    assert acquirer.called is True
    assert len(entries) == 1
    assert entries[0].headword == "rāma"


def test_source_parser_accepts_custom_parser():
    acquirer = StubAcquirer(
        "headword\tdefinition\n"
        "rāma\tpleasing\n"
    )

    parser = DelimitedMonierWilliamsParser()

    source_parser = MonierWilliamsSourceParser(
        acquirer=acquirer,
        parser=parser,
    )

    assert source_parser.parser is parser
