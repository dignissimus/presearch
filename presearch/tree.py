import ast


class PresearchTransformer(ast.NodeTransformer):
    def visit_Module(self, module):
        module.__class__ = PresearchModule
        return module


class PresearchModule(ast.Module):
    def imports(self, name):
        for statement in self.body:
            if isinstance(statement, ast.Import):
                for alias in statement.names:
                    if alias.name == "ast":
                        return True
        return False

    def defines(self, name):
        for statement in self.body:
            if isinstance(statement, ast.FunctionDef) or isinstance(
                statement, ast.AsyncFunctionDef
            ):
                if statement.name == name:
                    return True
        return False


class PresearchClassDef(ast.ClassDef):
    pass


Module = PresearchModule
ClassDef = PresearchClassDef
