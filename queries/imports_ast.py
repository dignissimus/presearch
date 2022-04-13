from presearch.query import MatchQuery


def module_imports_ast(module):
    return module.imports("ast")


query = MatchQuery(module_imports_ast)
