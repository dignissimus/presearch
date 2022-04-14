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
    @staticmethod
    def crawl_function(tree):
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
                expressions += RecursiveCrawler.crawl_function(expression)

        return expressions
