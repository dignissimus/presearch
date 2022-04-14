import argparse
import importlib.util

import presearch
from .query import MatchQuery

import colorama


def main():
    colorama.init()
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

    if hasattr(pql, "queries"):
        queries = pql.queries
        print("Running queries...")
    elif hasattr(pql, "query"):
        queries = [pql.quert]
        print("Running query...")
    else:
        print("The given file doesn't define a query")
        exit(1)

    colorama.init()
    for query in queries:
        result = presearch.presearch(args.directory, query)
        result.pprint()


if __name__ == "__main__":
    main()
