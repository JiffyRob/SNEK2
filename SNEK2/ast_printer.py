#mypy: ignore-errors

class AstPrinter:
    def parenthesize(self, name, *args):
        return f"({name} {' '.join(map(str, args))})"

    def print(self, expression):
        return expression.accept(self)

    def visit_binary(self, expr):
        return f"({expr.operator.src} {self.print(expr.left)} {self.print(expr.right)})"

    def visit_grouping(self, expr):
        return f"(group {self.print(expr.expression)})"

    def visit_literal(self, expr):
        if expr.value == None:
            return "nil"
        return str(expr.value)

    def visit_unary(self, expr):
        return f"({expr.operator.src} {self.print(expr.right)})"
