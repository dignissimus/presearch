import presearch
from query import MatchQuery


def main():
    query = MatchQuery(lambda x: True)
    print("Presearching...")
    result = presearch.presearch(".", query)
    print(result.dump_match(0))


if __name__ == "__main__":
    main()
