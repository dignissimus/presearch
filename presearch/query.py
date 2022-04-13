import enum
import ast

from crawler import ModuleCrawler


class QueryType(enum.Enum):
    MATCH = enum.auto()
    CALCULATE = enum.auto()


class QueryOutcome:
    def __init__(self, tree, data, path):
        self.tree = tree
        self.data = data
        self.path = path


class QueryDomain(enum.Enum):
    MODULE = enum.auto()
    ALL = enum.auto()


class Query:
    def __init__(self, query_type, query_function, crawler=None):
        if not crawler:
            crawler = ModuleCrawler()

        self.type = query_type
        self.function = query_function
        self.crawler = crawler

    def process(self, tree, path):
        outcomes = []
        for subtree in self.crawler.crawl(tree):
            outcomes.append(QueryOutcome(tree, self.function(tree), path))

        return outcomes


class MatchQuery(Query):
    def __init__(self, query_function):
        super(MatchQuery, self).__init__(QueryType.MATCH, query_function)


class QueryResult:
    def __init__(self, query):
        self.outcomes = []
        self.failures = []
        self.query = query

    def match(self, n):
        """Returns the nth match of the query"""
        # TODO: Consider a better way of doing this
        # Perhaps the repeated computations could become computationally expensive
        return list(self.matches)[n]

    @property
    def matches(self):
        """Returns a generator for all the matches of the query"""
        return filter(lambda outcome: outcome.data, self.outcomes)

    def dump_match(self, index):
        return ast.dump(self.match(index).tree, indent=2)

    def add_failure(self, path):
        self.failures.append(path)

    def add_module(self, tree, path):
        self.outcomes += self.query.process(tree, path)

    def process(self, code, path):
        try:
            self.add_module(ast.parse(code), path)
        except SyntaxError:
            self.add_failure(path)
