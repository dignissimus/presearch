from presearch.query import Domain, StatisticalQuery
from presearch.constraints import ContainsMethodDefinition
from presearch.tree import ClassDef, Self


def assigns_all_arguments_to_attributes(class_def):
    init_function = class_def.function("__init__")
    for argument in init_function.non_self_arguments:
        if Self.attribute(argument.name).assign(argument) not in init_function:
            return False

    return True


def assigns_one_or_more_arguments_to_attributes(class_def):
    count = 0

    init_function = class_def.function("__init__")
    for argument in init_function.non_self_arguments:
        if Self.attribute(argument.name).assign(argument) not in init_function:
            continue
        return True

    return False


def assigns_two_or_more_arguments_to_attributes(class_def):
    count = 0

    init_function = class_def.function("__init__")
    for argument in init_function.non_self_arguments:
        if Self.attribute(argument.name).assign(argument) not in init_function:
            continue
        count += 1

    return count >= 2


def assigns_three_or_more_arguments_to_attributes(class_def):
    count = 0

    init_function = class_def.function("__init__")
    for argument in init_function.non_self_arguments:
        if Self.attribute(argument.name).assign(argument) not in init_function:
            continue
        count += 1

    return count >= 3


# Calculates the proportion of class `__init__` definitions
# that assign all their non-self arguments as attributes
queries = [
    StatisticalQuery(
        assigns_all_arguments_to_attributes,
        domain=Domain(
            ClassDef,
            constraints=[
                ContainsMethodDefinition("__init__", has_non_self_argument=True)
            ],
        ),
        domain_description="classes defining __init__",
        match_description="classes whose __init__ functions assigned all non-self arguments as attributes",
    ),
    StatisticalQuery(
        assigns_one_or_more_arguments_to_attributes,
        domain=Domain(
            ClassDef,
            constraints=[
                ContainsMethodDefinition(
                    "__init__", has_non_self_argument=True, minargs=2
                )
            ],
        ),
        domain_description="__init__ functions with at least one non-self argument",
        match_description="__init__ functions that assigned one or more non-self arguments as attributes",
    ),
    StatisticalQuery(
        assigns_two_or_more_arguments_to_attributes,
        domain=Domain(
            ClassDef,
            constraints=[
                ContainsMethodDefinition(
                    "__init__", has_non_self_argument=True, minargs=3
                )
            ],
        ),
        domain_description="__init__ functions with at least two non-self arguments",
        match_description="__init__ functions that assigned two or more non-self arguments as attributes",
    ),
    StatisticalQuery(
        assigns_three_or_more_arguments_to_attributes,
        domain=Domain(
            ClassDef,
            constraints=[
                ContainsMethodDefinition(
                    "__init__", has_non_self_argument=True, minargs=4
                )
            ],
        ),
        domain_description="__init__ functions with at least three non-self arguments",
        match_description="__init__ functions that assigned three or more non-self arguments as attributes",
    ),
]
