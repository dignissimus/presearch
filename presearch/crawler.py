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
    def crawl_function(module):
        raise NotImplementedError()
