import ast


class Constraint:
    pass


class ContainsMethodDefinition(Constraint):
    def __init__(self, name=None, has_non_self_argument=None, minargs=None):
        self.name = name
        self.has_non_self_argument = has_non_self_argument
        self.minargs = minargs

    def check(self, tree):
        if not isinstance(tree, (ast.ClassDef)):
            return False

        for statement in tree.body:
            if isinstance(statement, ast.FunctionDef):
                if (
                    self.has_non_self_argument is not None
                    and (len(statement.non_self_arguments) != 0)
                    != self.has_non_self_argument
                ):
                    continue
                if self.minargs is not None and len(statement.arguments) < self.minargs:
                    continue
                if self.name is None:
                    return True
                if statement.name == self.name:
                    return True

        return False
