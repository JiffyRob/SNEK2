from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    # single character
    LEFT_PAREN = 0
    RIGHT_PAREN = 1
    LEFT_BRACE = 2
    RIGHT_BRACE = 3
    COMMA = 4
    DOT = 5
    MINUS = 6
    PLUS = 7
    SEMICOLON = 8
    SLASH = 9
    STAR = 10

    # one or two character tokens
    BANG = 11
    BANG_EQUAL = 12
    EQUAL = 13
    EQUAL_EQUAL = 14
    GREATER = 15
    GREATER_EQUAL = 16
    LESS = 17
    LESS_EQUAL = 18

    # literals
    IDENTIFIER = 19
    STRING = 20
    NUMBER = 21

    # keywords
    AND = 22
    CLASS = 23
    ELSE = 24
    FALSE = 25
    FUN = 26
    FOR = 27
    IF = 28
    NIL = 29
    OR = 30
    PRINT = 31
    RETURN = 32
    SUPER = 33
    THIS = 34
    TRUE = 35
    VAR = 36
    WHILE = 37
    
    # EOF
    EOF = 38

    # Line number
    LINE = 39


class ErrorType(Enum):
    SCAN_ERROR = "Scanner Error"
    PARSE_ERROR = "Parser Error"

def log_error(type: ErrorType, message: str, line: int):
    print(f"ERROR, line {line}\n{type.value}: {message}")
    exit(1)


@dataclass
class Token:
    type: TokenType
    src: str
    literal: str | None
    line: int


class Error(Exception):
    def __init__(self, type, token, message):
        self.type = type
        self.token = token
        self.message = message

    def __str__(self):
        return f"{self.type.value} at line {self.token.line}\n{self.token.src}: \n{self.message}"