from presearch.query import MatchQuery

query = MatchQuery(lambda module: module.imports("ast"))
