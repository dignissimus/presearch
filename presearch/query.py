import enum
import ast

from .crawler import ModuleCrawler, RecursiveCrawler
from .tree import PresearchTransformer


class QueryOutcome:
    def __init__(self, tree, data, path):
        self.tree = tree
        self.data = data
        self.path = path


class Domain:
    def __init__(self, tree_type=None, constraints=None):
        if not tree_type:
            tree_type = ast.AST
        if constraints is None:
            constraints = []

        self.tree_type = tree_type
        self.constraints = constraints


# TODO: perhaps remove crawler and make Query barebones
# Or maybe don't do this and still make Query barebones
# Or make crawler to a bit more work
class Query:
    def __init__(self, query_function, crawler=None):
        if not crawler:
            crawler = ModuleCrawler()

        self.function = query_function
        self.crawler = crawler

    def process(self, tree, path):
        outcomes = []
        for subtree in self.crawler.crawl(tree):
            outcomes.append(QueryOutcome(tree, self.function(tree), path))

        return outcomes


class MatchQuery(Query):
    def __init__(self, query_function, **kwargs):
        super(MatchQuery, self).__init__(query_function, **kwargs)


class StatisticalQuery(Query):
    def __init__(self, query_function, domain, **kwargs):
        self.domain = domain
        super(StatisticalQuery, self).__init__(
            query_function, crawler=RecursiveCrawler(), **kwargs
        )


class QueryResult:
    def __init__(self, query):
        self.outcomes = []
        self.failures = []
        self.query = query
        self.transformer = PresearchTransformer()

    def match(self, n):
        """Returns the nth match of the query"""
        # TODO: Consider a better way of doing this
        # Perhaps the repeated computations could become computationally expensive
        return list(self.matches)[n]

    @property
    def match_paths(self):
        return list(
            map(
                lambda outcome: outcome.path,
                filter(lambda outcome: outcome.data, self.outcomes),
            )
        )

    @property
    def matches(self):
        """Returns a generator for all the matches of the query"""
        return filter(lambda outcome: outcome.data, self.outcomes)

    def dump_match(self, index):
        return ast.dump(self.match(index).tree, indent=2)

    def add_failure(self, path):
        self.failures.append(path)

    def add_module(self, tree, path):
        tree = self.transformer.visit(tree)
        self.outcomes += self.query.process(tree, path)

    def process(self, code, path):
        try:
            self.add_module(ast.parse(code), path)
        except SyntaxError:
            self.add_failure(path)
