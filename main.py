from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.pipeline import AnalysisPipeline
from services.export_service import ExportService
from lexicon.dictionary import Dictionary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze Sanskrit text.")
    parser.add_argument("text", nargs="?", default="धर्म कर्म", help="Sanskrit text to analyze")
    parser.add_argument(
        "--dictionary",
        default="data/dictionaries/basic.json",
        help="Path to dictionary JSON",
    )
    parser.add_argument("--output", default="analysis_result", help="Output JSON basename")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    dictionary = Dictionary(Path(args.dictionary))
    pipeline = AnalysisPipeline(dictionary=dictionary)
    exporter = ExportService()
    result = pipeline.run(args.text)

    path = exporter.export_json(args.output, result)
    print(f"Tokens: {', '.join(result.tokens)}")
    print(f"Saved analysis to: {path}")


if __name__ == "__main__":
    main()
