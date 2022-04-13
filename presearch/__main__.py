import argparse
import importlib.util

import presearch
from .query import MatchQuery

import colorama
import termcolor


def main():
    parser = argparse.ArgumentParser(
        description="Syntactically query python source code", prog="presearch"
    )

    parser.add_argument(
        "directory",
        type=str,
        default=".",
        help="The directory containing the source code to query",
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        required=True,
        help="The file containing query to execute",
    )

    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("pql", args.file)
    pql = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pql)

    try:
        query = pql.query
    except AttributeError:
        print("The given file doesn't define a query")
        exit()

    print("Running query...")
    result = presearch.presearch(".", query)

    colorama.init()
    for path in result.match_paths:
        print(f"File {termcolor.colored(path, 'green')} matches query")


if __name__ == "__main__":
    main()
