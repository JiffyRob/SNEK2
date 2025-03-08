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

class Call(Expression):
    def __init__(self, token, callee, paren, arguments):
        self.token = token
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call(self)

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

class Logical(Expression):
    def __init__(self, token, left, operator, right):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical(self)

class Unary(Expression):
    def __init__(self, token, operator, right):
        self.token = token
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary(self)

class Identifier(Expression):
    def __init__(self, token, name):
        self.token = token
        self.name = name

    def accept(self, visitor):
        return visitor.visit_identifier(self)

class Assign(Expression):
    def __init__(self, token, name, value):
        self.token = token
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign(self)

