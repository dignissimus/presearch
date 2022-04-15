import ast


class PresearchTransformer(ast.NodeTransformer):
    def visit_Module(self, module):
        module.__class__ = PresearchModule
        self.generic_visit(module)
        return module

    def visit_ClassDef(self, class_def):
        class_def.__class__ = PresearchClassDef
        self.generic_visit(class_def)
        return class_def

    def visit_FunctionDef(self, function_def):
        function_def.__class__ = PresearchFunctionDef
        self.generic_visit(function_def)
        return function_def

    def visit_Name(self, name):
        name.__class__ = PresearchName
        self.generic_visit(name)
        return name

    def visit_arg(self, arg):
        arg.__class__ = PresearchArg
        self.generic_visit(arg)
        return arg

    def visit_Attribute(self, attribute):
        attribute.__class__ = PresearchAttribute
        self.generic_visit(attribute)
        return attribute


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
    def defines(self, name):
        for statement in self.body:
            if isinstance(statement, ast.FunctionDef) or isinstance(
                statement, ast.AsyncFunctionDef
            ):
                if statement.name == name:
                    return True
        return False

    def function(self, name):
        for statement in self.body:
            if isinstance(statement, ast.FunctionDef):
                if statement.name == name:
                    return statement

        return None


class PresearchFunctionDef(ast.FunctionDef):
    @property
    def arguments(self):
        return self.args.posonlyargs + self.args.args + self.args.kwonlyargs

    @property
    def non_self_arguments(self):
        return self.arguments[1:]

    def contains(self, expression):
        if isinstance(expression, ast.Assign):
            for statement in self.body:
                if not isinstance(statement, ast.Assign):
                    continue
                if (
                    statement.targets == expression.targets
                    and statement.value == expression.value
                ):
                    return True
                else:
                    continue
        return False

    def __contains__(self, expression):
        return self.contains(expression)


class PresearchName(ast.Name):
    def __eq__(self, other):
        if not isinstance(other, ast.Name):
            return False
        return self.id == other.id

    def assign(self, expression):
        return ast.Assign([self.store()], expression)

    def store(self):
        return PresearchName(self.id, ast.Store())

    def attribute(self, name):
        return PresearchAttribute(self, name, ast.Load())


class PresearchArg(ast.arg):
    @property
    def name(self):
        return self.arg


class PresearchAttribute(ast.Attribute):
    def __eq__(self, other):
        if not isinstance(other, ast.Attribute):
            return False
        return self.value == other.value and self.attr == other.attr

    def assign(self, expression):
        if isinstance(expression, ast.arg):
            expression = PresearchName(expression.arg, ast.Load())

        return ast.Assign([self.store()], expression)

    def store(self):
        return PresearchAttribute(self.value, self.attr, ast.Store())


Module = PresearchModule
ClassDef = PresearchClassDef
Name = PresearchName
Variable = PresearchName
Self = PresearchName("self", ast.Load())
