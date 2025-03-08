from .common import TokenType, ErrorType, Token, Error
from .expression import (
    Binary,
    Grouping,
    Literal,
    Unary,
    Identifier,
    Assign,
    Logical,
    Call,
    FString,
)
from .statement import Print, Block, If, While, Switch


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.valid = True

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
        raise Error(
            ErrorType.PARSE_ERROR, message, self.previous().src, self.previous().line
        )

    def synchonize(self):
        self.valid = False
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.peek().type in (
                TokenType.WHILE,
                TokenType.IF,
                TokenType.ELSE,
                TokenType.PRINT,
            ):
                return
            self.advance()

    def statement(self):
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.SWITCH):
            return self.switch_statement()
        if self.match(TokenType.LEFT_BRACE):
            return self.block()
        return self.expression_statement()

    def if_statement(self):
        condition = self.expression()
        if not self.check(TokenType.LEFT_BRACE):
            self.consume(TokenType.THEN, "Expected either block statement or 'then'")
        if_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        return If(condition, condition, if_branch, else_branch)

    def while_statement(self):
        condition = self.expression()
        if not self.check(TokenType.LEFT_BRACE):
            self.consume(TokenType.DO, "Expected either block statement or 'do'")
        body = self.statement()

        return While(condition, condition, body)

    def switch_statement(self):
        expr = self.expression()
        self.consume(TokenType.LEFT_BRACE, "Switch statement must start a new block")

        cases = []

        while not self.match(TokenType.RIGHT_BRACE):
            self.consume(TokenType.CASE, "Must only have cases inside switch statement")
            case_expr = self.expression()
            if not self.check(TokenType.LEFT_BRACE):
                self.consume(TokenType.DO, "Expected either block statement or 'do'")
            case_body = self.statement()
            cases.append((case_expr, case_body))

        return Switch(expr, expr, cases)

    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return expr

    def block(self):
        statements = []
        token = self.peek()
        while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return Block(token, statements)

    def print_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(self.peek(), expr)

    def declaration(self):
        try:
            return self.statement()
        except Error as e:
            print(e)
            self.synchonize()
            return None

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self._or()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Identifier):
                name = expr.token
                return Assign(name, name, value)

            raise Error(
                ErrorType.PARSE_ERROR,
                "Invalid assignment target.",
                equals.src,
                equals.line,
            )
        return expr

    def _or(self):
        expr = self._and()

        while self.match(TokenType.OR):
            operator = self.previous()
            right = self._and()
            expr = Logical(expr, operator, right)
        return expr

    def _and(self):
        expr = self.equality()

        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        return expr

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

        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
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

        return self.call()

    def call(self):
        expr = self.primary()

        while self.match(TokenType.LEFT_PAREN):
            expr = self.finish_call(expr)

        return expr

    def finish_call(self, callee):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.expression())
        paren = self.consume(
            TokenType.RIGHT_PAREN, "Expect ')' after function call arguments"
        )

        return Call(callee, callee, paren, arguments)

    def primary(self, const=False):
        token = self.peek()
        if self.match(TokenType.TRUE):
            return Literal(token, True)
        if self.match(TokenType.FALSE):
            return Literal(token, False)
        if self.match(TokenType.NIL):
            return Literal(token, None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(token, self.previous().literal)
        if self.match(TokenType.FSTRING):
            return self.desugar_fstring(token)
        if not const:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.expression()
                self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
                return Grouping(token, expr)
            if self.match(TokenType.IDENTIFIER):
                return Identifier(token, self.previous())

        raise Error(ErrorType.PARSE_ERROR, "Expect expression.", token.src, token.line)

    def desugar_fstring(self, token):
        expressions = []
        while not self.check(TokenType.FSTRING_END):
            current_token = self.peek()
            if current_token.type == TokenType.FSTRING_PART:
                self.advance()
                expressions.append(Literal(current_token, current_token.literal))
            else:
                expressions.append(self.expression())
        self.advance()
        expr = expressions.pop(0)
        for term in expressions:
            expr = Binary(
                term.token,
                expr,
                Token(TokenType.PLUS, "", None, None),
                Call(
                    term.token,
                    Identifier(
                        term.token, Token(TokenType.IDENTIFIER, "str", "str", None)
                    ),
                    None,
                    [term],
                ),
            )

        return expr

    def parse(self):
        tokens = []
        while not self.is_at_end():
            tokens.append(self.declaration())
        if not self.valid:
            return []
        return tokens

    def parse_expression(self):
        expr = self.expression()
        if not self.is_at_end():
            raise Error(
                ErrorType.PARSE_ERROR,
                "Expected 1 expression and nothing more",
                expr.src,
                expr.line,
            )

        return expr
