# AUTO GENERATED FILE

class Expression:
    pass

class Binary(Expression):
    def __init__(self, token, left, operator, right):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary(self)

class Grouping(Expression):
    def __init__(self, token, expression):
        self.token = token
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping(self)

class Literal(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)

class Unary(Expression):
    def __init__(self, token, operator, right):
        self.token = token
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary(self)

