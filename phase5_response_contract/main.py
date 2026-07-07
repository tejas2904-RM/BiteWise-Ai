from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from contract.adapters import from_phase4_response
from contract.models import RecommendationRequest, RecommendationResponse
from contract.schema_export import export_json_schemas, export_typescript_types


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Phase 5: Export and validate the shared API response contract.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    export_parser = sub.add_parser("export", help="Export JSON Schema and TypeScript types.")
    export_parser.add_argument(
        "--schemas-dir",
        type=Path,
        default=Path("schemas"),
        help="Output directory for JSON Schema files.",
    )
    export_parser.add_argument(
        "--typescript",
        type=Path,
        default=Path("typescript/types.ts"),
        help="Output path for TypeScript types.",
    )

    validate_parser = sub.add_parser("validate", help="Validate a JSON file against the contract.")
    validate_parser.add_argument("file", type=Path, help="JSON file to validate.")
    validate_parser.add_argument(
        "--kind",
        choices=["response", "request"],
        default="response",
        help="Schema kind to validate against.",
    )

    adapt_parser = sub.add_parser("adapt", help="Adapt Phase 4 JSON output to Phase 5 contract.")
    adapt_parser.add_argument("file", type=Path, help="Phase 4 recommendations JSON file.")
    adapt_parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output path for normalized contract JSON.",
    )

    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "export":
        schema_paths = export_json_schemas(args.schemas_dir)
        ts_path = export_typescript_types(args.typescript)
        print("Exported schemas:")
        for name, path in schema_paths.items():
            print(f"  - {name}: {path}")
        print(f"Exported TypeScript: {ts_path}")
        return

    if args.command == "validate":
        if not args.file.exists():
            print(f"File not found: {args.file}", file=sys.stderr)
            raise SystemExit(1)
        payload = json.loads(args.file.read_text(encoding="utf-8"))
        model = RecommendationRequest if args.kind == "request" else RecommendationResponse
        result = model.model_validate(payload)
        print(f"Valid {args.kind}: {result.__class__.__name__}")
        return

    if args.command == "adapt":
        if not args.file.exists():
            print(f"File not found: {args.file}", file=sys.stderr)
            raise SystemExit(1)
        payload = json.loads(args.file.read_text(encoding="utf-8"))
        contract = from_phase4_response(payload)
        output = contract.model_dump_json(indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8")
            print(f"Wrote contract JSON to: {args.output}")
        else:
            print(output)


if __name__ == "__main__":
    main()
