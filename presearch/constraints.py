import ast


class Constraint:
    pass


class ContainsMethodDefinition(Constraint):
    def __init__(self, name=None):
        self.name = name

    def check(self, tree):
        if not isinstance(tree, (ast.ClassDef)):
            return False

        for statement in tree.body:
            if isinstance(statement, ast.FunctionDef):
                if self.name is None:
                    return True
                if statement.name == self.name:
                    return True

        return False
