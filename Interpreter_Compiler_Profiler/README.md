# Interpreter vs Compiler Profiler — PS-02

A beginner-friendly Compiler Design project built using Python and Streamlit.

## Features
- Custom mini programming language
- Lexical analysis
- Recursive-descent parser
- Direct AST interpreter
- Intermediate bytecode generation
- Stack-based virtual machine
- Execution time and instruction count comparison
- Interactive performance chart
- CSV report download

## Supported syntax

```text
x = 10;
y = 20;
print(x + y);

if (x < y) {
    print(1);
} else {
    print(0);
}

i = 1;
while (i <= 3) {
    print(i);
    i = i + 1;
}
```

Every assignment and print statement ends with a semicolon. Use braces around if/else and while blocks.

## Run in VS Code

1. Open this folder in VS Code.
2. Open the terminal: Terminal > New Terminal.
3. Create a virtual environment (recommended):

   Windows:
   `python -m venv venv`
   `venv\Scripts\activate`

4. Install dependencies:

   `python -m pip install -r requirements.txt`

5. Start the app:

   `python -m streamlit run app.py`

6. Open the local URL shown in the terminal, usually http://localhost:8501.

## Important note about timing

This project is an educational profiler, not a production-grade benchmark. Timings for tiny programs can be noisy. Run larger programs several times before drawing performance conclusions.
