from .common import TokenType, ErrorType, Token, Error
from .expression import Binary, Grouping, Literal, Unary
from .statement import Print

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def is_at_end(self):
        return self.current >= len(self.tokens) - 1

    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        # ported from Java.  get() doesn't handle negatives.
        assert self.current > 0
        return self.tokens[self.current - 1]

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
            
        return False
    
    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise Error(ErrorType.PARSE_ERROR, self.peek(), message)
    
    def synchonize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.peek().type in (TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.PRINT, TokenType.RETURN):
                return
            self.advance()

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()
        return self.expression_statement()
    
    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return expr
    
    def print_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(self.peek(), expr)

    def expression(self):
        return self.equality()
    
    def equality(self):
        expr = self.comparison()
        token = self.peek()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(token, expr, operator, right)

        return expr
    
    def comparison(self):
        expr = self.term()
        token = self.peek()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(token, expr, operator, right)

        return expr
    
    def term(self):
        expr = self.factor()
        token = self.peek()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(token, expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()
        token = self.peek()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(token, expr, operator, right)

        return expr
    
    def unary(self):
        token = self.peek()
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()

            return Unary(token, operator, right)
        
        return self.primary()
        
    def primary(self):
        token = self.peek()
        if self.match(TokenType.TRUE):
            return Literal(token, True)
        if self.match(TokenType.FALSE):
            return Literal(token, False)
        if self.match(TokenType.NIL):
            return Literal(token, None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(token, self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(token, expr)
        
        raise Error(ErrorType.PARSE_ERROR, self.peek(), "Expect expression.")
    
    def parse(self):
        while not self.is_at_end():
            yield self.statement()