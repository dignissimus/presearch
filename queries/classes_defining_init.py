from presearch.tree import ClassDef
from presearch.query import Domain, StatisticalQuery

# Calculates the percentage of classes that define `__init__`
query = StatisticalQuery(
    lambda klass: klass.defines("__init__"),
    domain=Domain(ClassDef),
    domain_description="class definitions",
    match_description="classes that explicitly define __init__",
)
