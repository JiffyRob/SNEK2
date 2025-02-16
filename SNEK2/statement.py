# AUTO GENERATED FILE

class Statement:
    pass

class Expression(Statement):
    def __init__(self, token, expression):
        self.token = token
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression(self)

class Print(Statement):
    def __init__(self, token, expression):
        self.token = token
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print(self)

