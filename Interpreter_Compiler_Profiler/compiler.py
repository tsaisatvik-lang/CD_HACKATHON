class Compiler:
    def __init__(self):
        self.code = []
        self.label_count = 0

    def emit(self, instruction, *args):
        self.code.append((instruction, *args))

    def new_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def compile_expression(self, node):
        kind = node[0]
        if kind == "number":
            self.emit("PUSH", node[1])
        elif kind == "variable":
            self.emit("LOAD", node[1])
        elif kind == "unary":
            self.compile_expression(node[2])
            self.emit("NEG")
        elif kind == "binary":
            self.compile_expression(node[2])
            self.compile_expression(node[3])
            opcode = {
                "+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV",
                "==": "EQ", "!=": "NE", "<": "LT", ">": "GT",
                "<=": "LE", ">=": "GE"
            }[node[1]]
            self.emit(opcode)
        else:
            raise RuntimeError(f"Unknown expression type: {kind}")

    def compile_statements(self, statements):
        for statement in statements:
            kind = statement[0]
            if kind == "assign":
                self.compile_expression(statement[2])
                self.emit("STORE", statement[1])
            elif kind == "print":
                self.compile_expression(statement[1])
                self.emit("PRINT")
            elif kind == "if":
                else_label = self.new_label()
                end_label = self.new_label()
                self.compile_expression(statement[1])
                self.emit("JUMP_IF_FALSE", else_label)
                self.compile_statements(statement[2])
                self.emit("JUMP", end_label)
                self.emit("LABEL", else_label)
                self.compile_statements(statement[3])
                self.emit("LABEL", end_label)
            elif kind == "while":
                start_label = self.new_label()
                end_label = self.new_label()
                self.emit("LABEL", start_label)
                self.compile_expression(statement[1])
                self.emit("JUMP_IF_FALSE", end_label)
                self.compile_statements(statement[2])
                self.emit("JUMP", start_label)
                self.emit("LABEL", end_label)
            else:
                raise RuntimeError(f"Unknown statement type: {kind}")

    def compile(self, tree):
        self.compile_statements(tree[1])
        self.emit("HALT")
        return self.code

def format_code(code):
    lines = []
    for index, instruction in enumerate(code):
        if instruction[0] == "LABEL":
            lines.append(f"{instruction[1]}:")
        else:
            args = ", ".join(map(str, instruction[1:]))
            lines.append(f"{index:03d}: {instruction[0]} {args}".rstrip())
    return "\n".join(lines)
