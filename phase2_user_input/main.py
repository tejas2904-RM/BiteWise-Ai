from __future__ import annotations

import argparse

import uvicorn

from src.cli import run_cli


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Phase 2: User preference input.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("cli", help="Collect preferences via CLI and print JSON.")

    serve_parser = subparsers.add_parser("serve", help="Start the preference input API.")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)
    serve_parser.add_argument("--reload", action="store_true")

    return parser


def main() -> None:
    parser = build_parser()
    args, remaining = parser.parse_known_args()

    if args.command == "cli":
        run_cli(remaining)
        return

    if args.command == "serve":
        uvicorn.run("src.api:app", host=args.host, port=args.port, reload=args.reload)
        return


if __name__ == "__main__":
    main()
