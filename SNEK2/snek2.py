import asyncio
from enum import Enum
from dataclasses import dataclass




class Expression:
    pass

class BinaryExpression(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Grouping(Expression):
    def __init__(self, expression):
        self.expression = expression

class Literal(Expression):
    def __init__(self, value):
        self.value = value

class Unary(Expression):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right


class SNEKProgram:
    def __init__(self, script, builtins=None, api=None):
        self.tokens = Lexer.tokenize(script)
        

    async def run(self):
        print(self.tokens)
        return 0

    
if __name__ == "__main__":
    with open("test.snek") as f:
        script = f.read()
    scanner = Scanner(script)
    tokens = scanner.scan()
    for t in tokens:
        print(t)
