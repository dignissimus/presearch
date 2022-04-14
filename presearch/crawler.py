import ast


class TreeCrawler:
    def __init__(self, crawl_function=None):
        if not crawl_function:
            crawl_function = self.crawl_function

        self.crawl = crawl_function

    @staticmethod
    def crawl_function(module):
        raise Exception("No crawl function provided")


class ModuleCrawler(TreeCrawler):
    @staticmethod
    def crawl_function(module):
        return [module]


class RecursiveCrawler(TreeCrawler):
    def __init__(self, condition=None):
        self.condition = condition
        super(RecursiveCrawler, self).__init__()

    @staticmethod
    def recursive_crawl(tree):
        if not isinstance(tree, ast.AST):
            return []
        expressions = [tree]
        for field in tree._fields:
            sub_expressions = []
            field_value = getattr(tree, field)
            if field_value is None:
                continue
            elif isinstance(field_value, list):
                sub_expressions = field_value
            elif isinstance(field_value, ast.AST):
                sub_expressions = [field_value]
            else:
                pass  # Ignore

            for expression in sub_expressions:
                expressions += RecursiveCrawler.recursive_crawl(expression)

        return expressions

    def crawl_function(self, tree):
        expressions = RecursiveCrawler.recursive_crawl(tree)
        if self.condition is not None:
            return list(filter(self.condition, expressions))

        return expressions
