from .common import TokenType, ErrorType, Error
import operator

class Interpreter:
    def __init__(self):
        ...

    def is_truthy(self, value):
        return bool(value)
    
    def operate_unary(self, v, op):
        val = self.evaluate(v)
        try:
            return op(val)
        except TypeError:
            raise Error(ErrorType.TYPE_ERROR, None, f"Operation unsupported for type {type(v)}")
    
    def operate_binary(self, expr, op):
        val1 = self.evaluate(expr.left)
        val2 = self.evaluate(expr.right)
        try:
            return op(val1, val2)
        except TypeError:
            raise Error(ErrorType.TYPE_ERROR, expr.operator, f"Operation unsupported between types {type(val1)} and {type(val2)}")

    def evaluate(self, expr):
        return expr.accept(self)
    
    def execute(self, stmt):
        stmt.accept(self)
    
    def visit_expression(self, stmt):
        self.evaluate(stmt.expression)

    def visit_print(self, stmt):
        value = self.evaluate(stmt.expression)
        print(f"SNEK LOG: {self.repr(value)}")

    def visit_literal(self, expr):
        return expr.value
    
    def visit_grouping(self, expr):
        return self.evaluate(expr.expression)
    
    def visit_unary(self, expr):
        match expr.operator.type:
            case TokenType.BANG:
                return self.operate_unary(self.evaluate(expr.right), operator.not_)
            case TokenType.MINUS:
                return self.operate_unary(self.evaluate(expr.right), operator.neg)
            
    def visit_binary(self, expr):
        match expr.operator.type:
            case TokenType.GREATER:
                return self.operate_binary(expr, operator.gt)
            case TokenType.GREATER_EQUAL:
                return self.operate_binary(expr, operator.ge)
            case TokenType.LESS:
                return self.operate_binary(expr, operator.lt)
            case TokenType.LESS_EQUAL:
                return self.operate_binary(expr, operator.le)
            case TokenType.MINUS:
                return self.operate_binary(expr, operator.sub)
            case TokenType.PLUS:
                return self.operate_binary(expr, operator.add)
            case TokenType.SLASH:
                return self.operate_binary(expr, operator.truediv)
            case TokenType.STAR:
                return self.operate_binary(expr, operator.mul)
            case TokenType.BANG_EQUAL:
                return self.operate_binary(expr, operator.ne)
            case TokenType.EQUAL_EQUAL:
                return self.operate_binary(expr, operator.eq)
            
    def repr(self, value):
        if value is None:
            return "nil"
        return str(value)
            
    def interpret(self, statements):
        for stmt in statements:
            self.execute(stmt)