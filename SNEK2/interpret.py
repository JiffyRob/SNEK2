from .common import TokenType, ErrorType, Error
from . import environment
import operator

class Interpreter:
    def __init__(self):
        self.env = environment.Environment()

    def is_truthy(self, value):
        return bool(self.evaluate(value))
    
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

    def execute_block(self, statements, env):
        previous = self.env
        try:
            self.env = env
            for stmt in statements:
                self.execute(stmt)
        finally:
            self.env = previous
    
    def visit_expression(self, stmt):
        self.evaluate(stmt.expression)

    def visit_if(self, stmt):
        if self.is_truthy(stmt.condition):
            self.execute(stmt.if_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_while(self, stmt):
        while self.is_truthy(stmt.condition):
            self.execute(stmt.body)

    def visit_print(self, stmt):
        value = self.evaluate(stmt.expression)
        print(f"SNEK LOG: {self.repr(value)}")

    def visit_var(self, stmt):
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        else:
            value = None
        self.env.define(stmt.name, value)

    def visit_block(self, stmt):
        self.execute_block(stmt.statements, environment.Environment(self.env))

    def visit_literal(self, expr):
        return expr.value
    
    def visit_logical(self, expr):
        left = self.evaluate(expr.left)

        if expr.operator == TokenType.OR:
            if self.is_truthy(left): 
                return left
            else:
                if not self.is_truthy(left):
                    return left
                
        return self.evaluate(expr.right)
    
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
            
    def visit_identifier(self, expr):
        return self.env.get(expr.name)
    
    def visit_assign(self, expr):
        value = self.evaluate(expr.value)
        self.env.assign(expr.name, value)
        return value
            
    def repr(self, value):
        if value is None:
            return "nil"
        return str(value)
            
    def interpret(self, statements):
        for stmt in statements:
            self.execute(stmt)