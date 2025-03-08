from .common import TokenType, ErrorType, Error
from .api import SNEKCallable
from . import environment
import operator
from time import time
from random import randint

class Interpreter:
    def __init__(self):
        self.env = self.globals = environment.Environment()
        self.globals.assign("time", SNEKCallable(time, 0))
        self.globals.assign("str", SNEKCallable(str, 1))
        self.globals.assign("upper", SNEKCallable(lambda x: x.upper(), 1))
        self.globals.assign("lower", SNEKCallable(lambda x: x.lower(), 1))
        self.globals.assign("title", SNEKCallable(lambda x: x.title(), 1))
        self.globals.assign("randint", SNEKCallable(randint, 2))
        self.globals.assign("input", SNEKCallable(input, 1))
        self.globals.assign("contains", SNEKCallable(lambda x, y: x in y, 1))
        self.globals.assign("abs", SNEKCallable(lambda x, y: x in y, 1))

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

    def visit_switch(self, stmt):
        switch_value = self.evaluate(stmt.expr)
        for case_value, case_body in stmt.cases:
            if self.evaluate(case_value) == switch_value:
                self.execute(case_body)

    def visit_print(self, stmt):
        value = self.evaluate(stmt.expression)
        print(f"SNEK LOG: {self.repr(value)}")

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
            
    def visit_call(self, expr):
        callee = self.evaluate(expr.callee)
        arguments = [self.evaluate(argument) for argument in expr.arguments]

        if not isinstance(callee, SNEKCallable):
            raise Error(ErrorType.RUNTIME_ERROR, expr.paren, f"Object {callee} is not a function.")
        if callee.arity() != len(arguments):
            raise Error(ErrorType.RUNTIME_ERROR, expr.paren, f"Expected {callee.arity()} arguments, got {len(arguments)}")

        return callee.call(self, arguments)
            
    def visit_identifier(self, expr):
        return self.env.get(expr.name)
    
    def visit_assign(self, expr):
        value = self.evaluate(expr.value)
        self.env.assign(expr.name.src, value)
        return value
            
    def repr(self, value):
        if value is None:
            return "nil"
        return str(value)
            
    def interpret(self, statements):
        for stmt in statements:
            self.execute(stmt)