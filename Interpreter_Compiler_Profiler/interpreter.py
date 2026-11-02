class Interpreter:
    def __init__(self):
        self.variables = {}
        self.output = []
        self.steps = 0

    def evaluate(self, node):
        kind = node[0]
        if kind == "number":
            self.steps += 1
            return node[1]
        if kind == "variable":
            self.steps += 1
            name = node[1]
            if name not in self.variables:
                raise NameError(f"Variable '{name}' is not defined")
            return self.variables[name]
        if kind == "unary":
            self.steps += 1
            return -self.evaluate(node[2])
        if kind == "binary":
            self.steps += 1
            op, left_node, right_node = node[1], node[2], node[3]
            left = self.evaluate(left_node)
            right = self.evaluate(right_node)
            operations = {
                "+": lambda: left + right,
                "-": lambda: left - right,
                "*": lambda: left * right,
                "/": lambda: left / right,
                "==": lambda: left == right,
                "!=": lambda: left != right,
                "<": lambda: left < right,
                ">": lambda: left > right,
                "<=": lambda: left <= right,
                ">=": lambda: left >= right,
            }
            if op == "/" and right == 0:
                raise ZeroDivisionError("Division by zero")
            return operations[op]()
        raise RuntimeError(f"Unknown expression type: {kind}")

    def execute_statements(self, statements):
        for statement in statements:
            kind = statement[0]
            self.steps += 1
            if kind == "assign":
                self.variables[statement[1]] = self.evaluate(statement[2])
            elif kind == "print":
                self.output.append(str(self.evaluate(statement[1])))
            elif kind == "if":
                condition = self.evaluate(statement[1])
                if condition:
                    self.execute_statements(statement[2])
                else:
                    self.execute_statements(statement[3])
            elif kind == "while":
                while self.evaluate(statement[1]):
                    self.execute_statements(statement[2])
            else:
                raise RuntimeError(f"Unknown statement type: {kind}")

    def run(self, tree):
        self.execute_statements(tree[1])
        return {
            "output": self.output,
            "variables": self.variables,
            "steps": self.steps
        }
