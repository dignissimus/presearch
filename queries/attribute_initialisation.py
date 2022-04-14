from presearch.query import Domain, StatisticalQuery
from presearch.constraints import ContainsMethodDefinition
from presearch.tree import ClassDef, Self


def assigns_all_arguments_to_attributes(class_def):
    init_function = class_def.function("__init__")
    for argument in init_function.non_self_arguments:
        if not init_function.contains(Self.attribute(argument.name).assign(argument)):
            return False

    return True


# Calculates the proportion of
query = StatisticalQuery(
    assigns_all_arguments_to_attributes,
    domain=Domain(ClassDef, constraints=[ContainsMethodDefinition("__init__")]),
    domain_description="classes defining __init__",
    match_description="classes whose __init__ functions assigned all non-self arguments as attributes",
)
