import argparse
import importlib.util

import presearch
from .query import MatchQuery


def main():
    parser = argparse.ArgumentParser(
        description="Syntactically query python source code"
    )

    parser.add_argument("--file", "-f", type=str, required=True)

    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("pql", args.file)
    pql = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pql)

    try:
        query = pql.query
    except AttributeError:
        print("The given file doesn't define a query")
        exit()

    print("Presearching...")
    result = presearch.presearch(".", query)
    print(result.match_paths)


if __name__ == "__main__":
    main()
