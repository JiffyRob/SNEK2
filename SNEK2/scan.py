from .common import TokenType, ErrorType, Token, Error

def is_alphanumeric_or_underscore(c):
    return c.isalnum() or c == "_"

def is_alpha_or_underscore(c):
    return c.isalpha() or c == "_"

class Scanner:
    _cache = {}
    KEYWORDS = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type, literal=None):
        src = self.source[self.start:self.current]
        if token_type == TokenType.EOF:
            src = "<EOF>"
        self.tokens.append(
            Token(token_type, src, literal, self.line)
        )

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True
    
    def previous(self):
        assert self.current > 0
        return self.source[self.current - 1]

    def peek(self):
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def handle_string(self):
        while not self.is_at_end() and self.peek() != '"':
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            raise Error(ErrorType.SCAN_ERROR, "Unterminated string", self.line)

        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def handle_number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def handle_identifier(self):
        while is_alphanumeric_or_underscore(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]
        if text in self.KEYWORDS:
            self.add_token(self.KEYWORDS[text])
        else:
            self.add_token(TokenType.IDENTIFIER, self.source[self.start:self.current])

    def scan_token(self):
        c = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "!" if self.match("="):
                self.add_token(TokenType.BANG_EQUAL)
            case "!":
                self.add_token(TokenType.BANG)
            case "=" if self.match("="):
                self.add_token(TokenType.EQUAL_EQUAL)
            case "=":
                self.add_token(TokenType.EQUAL)
            case "<" if self.match("="):
                self.add_token(TokenType.LESS_EQUAL)
            case "<":
                self.add_token(TokenType.LESS)
            case ">" if self.match("="):
                self.add_token(TokenType.GREATER_EQUAL)
            case ">":
                self.add_token(TokenType.GREATER)
            case "#":
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            case "/":
                self.add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.handle_string()
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                self.handle_number()
            case _ if is_alpha_or_underscore(c):
                self.handle_identifier()
            case _:
                raise Error(ErrorType.SCAN_ERROR, self.previous(), "Unexpected character", self.line)

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan(self):
        if self.start:
            return self.tokens
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.add_token(TokenType.EOF)

        return self.tokens