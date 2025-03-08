from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    # single character
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # one or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # keywords
    AND = auto()
    # CLASS = auto()
    DO = auto()
    ELSE = auto()
    FALSE = auto()
    # FUN = auto()
    # FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    # RETURN = auto()
    # SUPER = auto()
    THEN = auto()
    # THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    SWITCH = auto()
    CASE = auto()
    
    # EOF
    EOF = auto()

    # Line number
    LINE = auto()


class ErrorType(Enum):
    SCAN_ERROR = "Scanner Error"
    PARSE_ERROR = "Parser Error"
    TYPE_ERROR = "Type Error"
    RUNTIME_ERROR = "Runtime Error"
    REDECLARED_VARIABLE_ERROR = "Redeclared Variable Error"
    UNBOUND_VARIABLE_ERROR = "Unbound Variable Error"


def throw(error):
    raise error


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
        return f"{self.type.value} at line {self.token.line} (\"{self.token.src}\"):\n{self.message}"