from presearch.query import Domain, StatisticalQuery
from presearch.constraints import ContainsMethodDefinition
from presearch.tree import ClassDef

# TODO: rename function
def query_function(class_def):
    pass


# Sketch, not at all concrete
# Maybe allow type to take a list as well as an AST type
# For possible AST types
query = StatisticalQuery(
    query_function,
    domain=Domain(ClassDef, constraints=[ContainsMethodDefinition("__init__")]),
)
