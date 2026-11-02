import re
from dataclasses import dataclass

@dataclass
class Token:
    kind: str
    value: str
    line: int
    column: int

TOKEN_SPEC = [
    ("NUMBER",   r"\d+(?:\.\d+)?"),
    ("IDENT",    r"[A-Za-z_][A-Za-z0-9_]*"),
    ("EQ",       r"=="),
    ("NE",       r"!="),
    ("LE",       r"<="),
    ("GE",       r">="),
    ("ASSIGN",   r"="),
    ("LT",       r"<"),
    ("GT",       r">"),
    ("PLUS",     r"\+"),
    ("MINUS",    r"-"),
    ("STAR",     r"\*"),
    ("SLASH",    r"/"),
    ("LPAREN",   r"\("),
    ("RPAREN",   r"\)"),
    ("LBRACE",   r"\{"),
    ("RBRACE",   r"\}"),
    ("SEMICOLON",r";"),
    ("NEWLINE",  r"\n"),
    ("SKIP",     r"[ \t\r]+"),
    ("MISMATCH", r"."),
]
MASTER_RE = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))

KEYWORDS = {"if": "IF", "else": "ELSE", "while": "WHILE", "print": "PRINT"}

def tokenize(source):
    tokens = []
    line = 1
    line_start = 0
    for match in MASTER_RE.finditer(source):
        kind = match.lastgroup
        value = match.group()
        column = match.start() - line_start + 1

        if kind == "NEWLINE":
            line += 1
            line_start = match.end()
            continue
        if kind == "SKIP":
            continue
        if kind == "MISMATCH":
            raise SyntaxError(f"Unexpected character {value!r} at line {line}, column {column}")
        if kind == "IDENT" and value in KEYWORDS:
            kind = KEYWORDS[value]
        tokens.append(Token(kind, value, line, column))

    tokens.append(Token("EOF", "", line, len(source) - line_start + 1))
    return tokens
