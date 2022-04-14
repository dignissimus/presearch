import ast


class Constraint:
    pass


class ContainsMethodDefinition(Constraint):
    def __init__(self, name=None):
        self.name = name

    def check(tree):
        for statement in self.body:
            if isinstance(statement, ast.FunctionDef):
                if name is None:
                    return True
                if name == self.name:
                    return True

        return False
