from presearch.query import MatchQuery

# Matches files that import the `ast` library
query = MatchQuery(lambda module: module.imports("ast"))
