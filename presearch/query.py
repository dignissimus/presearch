import enum
import ast

from .crawler import ModuleCrawler, RecursiveCrawler
from .tree import PresearchTransformer

import termcolor
import colorama


class QueryOutcome:
    def __init__(self, tree, data, path):
        self.tree = tree
        self.data = data
        self.path = path


class Domain:
    def __init__(self, tree_type=None, constraints=None):
        if tree_type is None:
            tree_type = ast.AST

        if constraints is None:
            constraints = []

        self.tree_type = tree_type
        self.constraints = constraints

    def check(self, tree):
        if not isinstance(tree, self.tree_type):
            return False

        for constraint in self.constraints:
            if not constraint.check(tree):
                return False

        return True


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
            outcomes.append(QueryOutcome(subtree, self.function(subtree), path))

        return outcomes


class MatchQuery(Query):
    def __init__(self, query_function, **kwargs):
        super(MatchQuery, self).__init__(query_function, **kwargs)

    def pprint(self, outcomes):
        for path in set(
            map(
                lambda outcome: outcome.path,
                filter(lambda outcome: outcome.data, outcomes),
            )
        ):
            print(f"File {termcolor.colored(path, 'green')} matches query")


class StatisticalQuery(Query):
    def __init__(
        self,
        query_function,
        domain,
        domain_description=None,
        match_description=None,
        **kwargs,
    ):
        if not domain_description:
            domain_description = "expressions in the domain"

        if not match_description:
            match_description = "query matches"

        self.domain_description = domain_description
        self.match_description = match_description

        self.domain = domain
        super(StatisticalQuery, self).__init__(
            query_function, crawler=RecursiveCrawler(condition=domain.check), **kwargs
        )

    def pprint(self, values):
        values = list(map(lambda outcome: outcome.data, values))
        total = len(values)
        matches = sum(values)
        if total != 0:
            percentage = round(100 * matches / total, 2)
        else:
            percentage = 0

        print(
            f"Out of {termcolor.colored(str(total), 'magenta')}"
            f" {termcolor.colored(self.domain_description, 'blue')},"
            f" there were {termcolor.colored(str(matches), 'green')}"
            f" ({termcolor.colored(str(percentage), 'green')}%)"
            f" {termcolor.colored(self.match_description, 'blue')}."
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
        return set(filter(lambda outcome: outcome.data, self.outcomes))

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

    def compute(self):
        return self.query.compute(self.outcomes)

    def pprint(self):
        self.query.pprint(self.outcomes)
