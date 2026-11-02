class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def check(self, kind):
        return self.current().kind == kind

    def advance(self):
        token = self.current()
        if token.kind != "EOF":
            self.pos += 1
        return token

    def expect(self, kind):
        token = self.current()
        if token.kind != kind:
            raise SyntaxError(
                f"Expected {kind}, found {token.kind} ({token.value!r}) "
                f"at line {token.line}, column {token.column}"
            )
        return self.advance()

    def parse(self):
        statements = []
        while not self.check("EOF"):
            if self.check("SEMICOLON"):
                self.advance()
                continue
            statements.append(self.statement())
        return ("program", statements)

    def statement(self):
        if self.check("IDENT"):
            name = self.advance().value
            self.expect("ASSIGN")
            expr = self.expression()
            self.expect("SEMICOLON")
            return ("assign", name, expr)

        if self.check("PRINT"):
            self.advance()
            self.expect("LPAREN")
            expr = self.expression()
            self.expect("RPAREN")
            self.expect("SEMICOLON")
            return ("print", expr)

        if self.check("IF"):
            self.advance()
            self.expect("LPAREN")
            condition = self.expression()
            self.expect("RPAREN")
            then_body = self.block()
            else_body = []
            if self.check("ELSE"):
                self.advance()
                else_body = self.block()
            return ("if", condition, then_body, else_body)

        if self.check("WHILE"):
            self.advance()
            self.expect("LPAREN")
            condition = self.expression()
            self.expect("RPAREN")
            body = self.block()
            return ("while", condition, body)

        token = self.current()
        raise SyntaxError(
            f"Unexpected token {token.value!r} at line {token.line}, column {token.column}"
        )

    def block(self):
        self.expect("LBRACE")
        statements = []
        while not self.check("RBRACE"):
            if self.check("EOF"):
                raise SyntaxError("Missing closing '}'")
            statements.append(self.statement())
        self.expect("RBRACE")
        return statements

    def expression(self):
        return self.comparison()

    def comparison(self):
        node = self.term()
        while self.check("EQ") or self.check("NE") or self.check("LT") or self.check("GT") or self.check("LE") or self.check("GE"):
            op = self.advance().value
            right = self.term()
            node = ("binary", op, node, right)
        return node

    def term(self):
        node = self.factor()
        while self.check("PLUS") or self.check("MINUS"):
            op = self.advance().value
            right = self.factor()
            node = ("binary", op, node, right)
        return node

    def factor(self):
        node = self.unary()
        while self.check("STAR") or self.check("SLASH"):
            op = self.advance().value
            right = self.unary()
            node = ("binary", op, node, right)
        return node

    def unary(self):
        if self.check("MINUS"):
            self.advance()
            return ("unary", "-", self.unary())
        return self.primary()

    def primary(self):
        if self.check("NUMBER"):
            value = self.advance().value
            return ("number", float(value) if "." in value else int(value))
        if self.check("IDENT"):
            return ("variable", self.advance().value)
        if self.check("LPAREN"):
            self.advance()
            node = self.expression()
            self.expect("RPAREN")
            return node
        token = self.current()
        raise SyntaxError(
            f"Expected a number, variable, or '(', found {token.value!r} "
            f"at line {token.line}, column {token.column}"
        )

def parse(tokens):
    return Parser(tokens).parse()
