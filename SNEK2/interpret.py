import asyncio

from .common import TokenType, ErrorType, Error
from .api import SNEKCallable, AsyncSNEKCallable
from . import environment
import operator
from time import time
from random import randint

class Interpreter:
    def __init__(self, api=None):
        if api is None:
            api = {}
        
        api = {
            "time": SNEKCallable(time, 0),
            "str": SNEKCallable(str, 1),
            "upper": SNEKCallable(lambda x: x.upper(), 1),
            "lower": SNEKCallable(lambda x: x.lower(), 1),
            "title": SNEKCallable(lambda x: x.title(), 1),
            "randint": SNEKCallable(randint, 2),
            "input": SNEKCallable(input, 1),
            "contains": SNEKCallable(lambda x, y: x in y, 2),
            "abs": SNEKCallable(abs, 1),
            "wait": AsyncSNEKCallable(asyncio.sleep, 1),
            **api,
        }

        self.env = self.globals = environment.Environment()

        for name, callable in api.items():
            self.globals.assign(name, callable)

    async def is_truthy(self, value):
        return bool(await self.evaluate(value))
    
    async def operate_unary(self, v, op):
        val = await self.evaluate(v)
        try:
            return op(val)
        except TypeError:
            raise Error(ErrorType.TYPE_ERROR, f"Operation unsupported for type {type(v)}", v.src, v.line)
    
    async def operate_binary(self, expr, op):
        val1 = await self.evaluate(expr.left)
        val2 = await self.evaluate(expr.right)
        try:
            return op(val1, val2)
        except TypeError:
            raise Error(ErrorType.TYPE_ERROR, f"Operation unsupported between types {type(val1)} and {type(val2)}", expr.operator.src, expr.operator.line)

    async def evaluate(self, expr):
        return await expr.accept(self)
    
    async def execute(self, stmt):
        await stmt.accept(self)

    async def execute_block(self, statements, env):
        previous = self.env
        try:
            self.env = env
            for stmt in statements:
                await self.execute(stmt)
        finally:
            self.env = previous
    
    async def visit_expression(self, stmt):
        await self.evaluate(stmt.expression)

    async def visit_if(self, stmt):
        if await self.is_truthy(stmt.condition):
            await self.execute(stmt.if_branch)
        elif stmt.else_branch is not None:
            await self.execute(stmt.else_branch)

    async def visit_while(self, stmt):
        while (await self.is_truthy(stmt.condition)):
            await self.execute(stmt.body)

    async def visit_switch(self, stmt):
        switch_value = await self.evaluate(stmt.expr)
        for case_value, case_body in stmt.cases:
            if (await self.evaluate(case_value)) == switch_value:
                await self.execute(case_body)

    async def visit_print(self, stmt):
        value = await self.evaluate(stmt.expression)
        print(f"SNEK LOG: {self.repr(value)}")

    async def visit_block(self, stmt):
        await self.execute_block(stmt.statements, environment.Environment(self.env))

    async def visit_literal(self, expr):
        return expr.value

    async def visit_logical(self, expr):
        left = await self.evaluate(expr.left)

        if expr.operator == TokenType.OR:
            if await self.is_truthy(left): 
                return left
        else:
            if not await self.is_truthy(left):
                return left

        return await self.evaluate(expr.right)
    
    async def visit_grouping(self, expr):
        return await self.evaluate(expr.expression)
    
    async def visit_unary(self, expr):
        match expr.operator.type:
            case TokenType.BANG:
                return await self.operate_unary(await self.evaluate(expr.right), operator.not_)
            case TokenType.MINUS:
                return await self.operate_unary(await self.evaluate(expr.right), operator.neg)
            
    async def visit_binary(self, expr):
        match expr.operator.type:
            case TokenType.GREATER:
                return await self.operate_binary(expr, operator.gt)
            case TokenType.GREATER_EQUAL:
                return await self.operate_binary(expr, operator.ge)
            case TokenType.LESS:
                return await self.operate_binary(expr, operator.lt)
            case TokenType.LESS_EQUAL:
                return await self.operate_binary(expr, operator.le)
            case TokenType.MINUS:
                return await self.operate_binary(expr, operator.sub)
            case TokenType.PLUS:
                return await self.operate_binary(expr, operator.add)
            case TokenType.SLASH:
                return await self.operate_binary(expr, operator.truediv)
            case TokenType.STAR:
                return await self.operate_binary(expr, operator.mul)
            case TokenType.BANG_EQUAL:
                return await self.operate_binary(expr, operator.ne)
            case TokenType.EQUAL_EQUAL:
                return await self.operate_binary(expr, operator.eq)
            
    async def visit_call(self, expr):
        callee = await self.evaluate(expr.callee)
        arguments = [(await self.evaluate(argument)) for argument in expr.arguments]

        if not isinstance(callee, SNEKCallable):
            raise Error(ErrorType.RUNTIME_ERROR, f"Object {callee} is not a function.", expr.paren.src, expr.paren.line)
        if callee.arity() != len(arguments):
            raise Error(ErrorType.RUNTIME_ERROR, f"Expected {callee.arity()} arguments, got {len(arguments)}", expr.paren.src, expr.paren.line)

        return await callee.call(self, arguments)
            
    async def visit_identifier(self, expr):
        return self.env.get(expr.name)
    
    async def visit_assign(self, expr):
        value = await self.evaluate(expr.value)
        self.env.assign(expr.name.src, value)
        return value
            
    def repr(self, value):
        if value is None:
            return "nil"
        return str(value)
            
    async def interpret(self, statements):
        for stmt in statements:
            await self.execute(stmt)