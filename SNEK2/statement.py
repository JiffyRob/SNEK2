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

class If(Statement):
    def __init__(self, token, condition, if_branch, else_branch):
        self.token = token
        self.condition = condition
        self.if_branch = if_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if(self)

class While(Statement):
    def __init__(self, token, condition, body):
        self.token = token
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while(self)

class Block(Statement):
    def __init__(self, token, statements):
        self.token = token
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block(self)

class Switch(Statement):
    def __init__(self, token, expr, cases):
        self.token = token
        self.expr = expr
        self.cases = cases

    def accept(self, visitor):
        return visitor.visit_switch(self)

