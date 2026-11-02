class VirtualMachine:
    def __init__(self, code):
        self.code = code
        self.variables = {}
        self.stack = []
        self.output = []
        self.steps = 0
        self.labels = {
            instruction[1]: index
            for index, instruction in enumerate(code)
            if instruction[0] == "LABEL"
        }

    def run(self):
        pc = 0
        while pc < len(self.code):
            instruction = self.code[pc]
            op = instruction[0]
            args = instruction[1:]
            self.steps += 1

            if op == "LABEL":
                pass
            elif op == "PUSH":
                self.stack.append(args[0])
            elif op == "LOAD":
                name = args[0]
                if name not in self.variables:
                    raise NameError(f"Variable '{name}' is not defined")
                self.stack.append(self.variables[name])
            elif op == "STORE":
                self.variables[args[0]] = self.stack.pop()
            elif op == "PRINT":
                self.output.append(str(self.stack.pop()))
            elif op == "NEG":
                self.stack.append(-self.stack.pop())
            elif op in ("ADD", "SUB", "MUL", "DIV", "EQ", "NE", "LT", "GT", "LE", "GE"):
                right = self.stack.pop()
                left = self.stack.pop()
                if op == "ADD": result = left + right
                elif op == "SUB": result = left - right
                elif op == "MUL": result = left * right
                elif op == "DIV":
                    if right == 0:
                        raise ZeroDivisionError("Division by zero")
                    result = left / right
                elif op == "EQ": result = left == right
                elif op == "NE": result = left != right
                elif op == "LT": result = left < right
                elif op == "GT": result = left > right
                elif op == "LE": result = left <= right
                else: result = left >= right
                self.stack.append(result)
            elif op == "JUMP_IF_FALSE":
                condition = self.stack.pop()
                if not condition:
                    pc = self.labels[args[0]]
            elif op == "JUMP":
                pc = self.labels[args[0]]
            elif op == "HALT":
                break
            else:
                raise RuntimeError(f"Unknown instruction: {op}")

            pc += 1

        return {
            "output": self.output,
            "variables": self.variables,
            "steps": self.steps
        }
