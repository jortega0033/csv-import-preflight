# Entry point: argument parsing for `python -m csv_preflight`.
import argparse
import sys

VERSION = "0.0.0"


def main(argv=None):
    parser = argparse.ArgumentParser(prog="csv_preflight")
    parser.add_argument("--version", action="version", version=f"csv_preflight {VERSION}")
    sub = parser.add_subparsers(dest="command")
    serve = sub.add_parser("serve", help="run the local app (not implemented yet)")
    serve.add_argument("--port", type=int, default=8767)
    serve.add_argument("--data-dir", required=True)
    args = parser.parse_args(argv)
    if args.command == "serve":
        print("not implemented yet: see #2", file=sys.stderr)
        return 1
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
