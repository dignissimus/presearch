import ast
import os
from .query import QueryResult


def presearch(directory_name, query):
    result = QueryResult(query)
    for (dirpath, _dirnames, filenames) in os.walk(directory_name):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            if not filename.endswith(".py"):
                continue
            with open(path) as file:
                result.process(file.read(), path)

    return result
