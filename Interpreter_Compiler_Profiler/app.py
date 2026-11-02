import time
import streamlit as st
import pandas as pd
import plotly.express as px

from lexer import tokenize
from parser import parse
from interpreter import Interpreter
from compiler import Compiler, format_code
from virtual_machine import VirtualMachine

st.set_page_config(page_title="Interpreter vs Compiler Profiler", page_icon="⚙️", layout="wide")

st.title("⚙️ Interpreter vs Compiler Profiler")
st.caption("A mini compiler project for demonstrating interpretation, intermediate code generation, and virtual-machine execution.")

DEFAULT_CODE = """a = 10;
b = 20;
c = a + b * 2;
print(c);

if (c > 30) {
    print(100);
} else {
    print(0);
}

i = 1;
sum = 0;
while (i <= 5) {
    sum = sum + i;
    i = i + 1;
}
print(sum);
"""

with st.sidebar:
    st.header("Project information")
    st.write("**Language features**")
    st.write("- Variables and assignments")
    st.write("- Integer and decimal numbers")
    st.write("- +, -, *, / operators")
    st.write("- Comparison operators")
    st.write("- if / else statements")
    st.write("- while loops")
    st.write("- print() statements")
    st.info("Every statement must end with a semicolon. Use braces for if and while blocks.")

st.subheader("1. Enter your mini-language program")
source = st.text_area("Program input", value=DEFAULT_CODE, height=300)

if st.button("▶ Run comparison", type="primary", use_container_width=True):
    try:
        # Interpreter path: measure each phase separately.
        start = time.perf_counter()
        interpreter_tokens = tokenize(source)
        interpreter_lex_time = time.perf_counter() - start

        start = time.perf_counter()
        interpreter_tree = parse(interpreter_tokens)
        interpreter_parse_time = time.perf_counter() - start

        interpreter = Interpreter()
        start = time.perf_counter()
        interpreter_result = interpreter.run(interpreter_tree)
        interpreter_exec_time = time.perf_counter() - start

        # Compiler path: independent tokenization and parsing.
        start = time.perf_counter()
        compiler_tokens = tokenize(source)
        compiler_lex_time = time.perf_counter() - start

        start = time.perf_counter()
        compiler_tree = parse(compiler_tokens)
        compiler_parse_time = time.perf_counter() - start

        compiler = Compiler()
        start = time.perf_counter()
        bytecode = compiler.compile(compiler_tree)
        compile_time = time.perf_counter() - start

        vm = VirtualMachine(bytecode)
        start = time.perf_counter()
        vm_result = vm.run()
        vm_exec_time = time.perf_counter() - start

        if interpreter_result["output"] != vm_result["output"]:
            st.error("The two execution paths produced different outputs. Please check the program.")
        else:
            st.success("Program executed successfully. Both approaches produced the same output.")

        st.subheader("2. Execution results")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Interpreter")
            st.code("\n".join(interpreter_result["output"]) or "(no output)")
            st.metric("Interpreter execution steps", interpreter_result["steps"])
        with col2:
            st.markdown("#### Compiler + Virtual Machine")
            st.code("\n".join(vm_result["output"]) or "(no output)")
            st.metric("VM instructions executed", vm_result["steps"])

        st.subheader("3. Generated intermediate code")
        st.code(format_code(bytecode), language="text")

        st.subheader("4. Phase-wise performance")
        timing_data = pd.DataFrame({
            "Phase": ["Lexical Analysis", "Parsing", "Translation / Code Generation", "Execution"],
            "Interpreter (ms)": [
                interpreter_lex_time * 1000,
                interpreter_parse_time * 1000,
                0.0,  # An interpreter does not generate intermediate code.
                interpreter_exec_time * 1000
            ],
            "Compiler + VM (ms)": [
                compiler_lex_time * 1000,
                compiler_parse_time * 1000,
                compile_time * 1000,
                vm_exec_time * 1000
            ]
        })
        st.dataframe(timing_data, use_container_width=True, hide_index=True)

        chart_data = timing_data.melt(
            id_vars="Phase",
            var_name="Execution approach",
            value_name="Time (ms)"
        )
        fig = px.bar(
            chart_data,
            x="Phase",
            y="Time (ms)",
            color="Execution approach",
            barmode="group",
            title="Phase-wise execution time comparison"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("5. Overall comparison")
        interpreter_total = interpreter_lex_time + interpreter_parse_time + interpreter_exec_time
        compiler_total = compiler_lex_time + compiler_parse_time + compile_time + vm_exec_time

        comparison = pd.DataFrame({
            "Metric": ["Total measured time (ms)", "Execution steps / VM instructions", "Generated bytecode instructions"],
            "Interpreter": [
                round(interpreter_total * 1000, 6),
                interpreter_result["steps"],
                "Not applicable"
            ],
            "Compiler + VM": [
                round(compiler_total * 1000, 6),
                vm_result["steps"],
                len(bytecode)
            ]
        })
        st.dataframe(comparison, use_container_width=True, hide_index=True)

        st.subheader("6. Performance explanation")
        st.write(
            "The interpreter evaluates the parsed syntax tree directly. "
            "The compiler path first translates the syntax tree into simple stack-based "
            "intermediate instructions, then the virtual machine executes those instructions."
        )
        st.warning(
            "For small programs, timing differences can be extremely tiny and affected by "
            "computer load and Python overhead. Do not claim that one approach is always faster. "
            "Compare several larger programs for more meaningful observations."
        )

        report = comparison.to_csv(index=False)
        st.download_button(
            "⬇ Download comparison report (CSV)",
            data=report,
            file_name="execution_comparison.csv",
            mime="text/csv"
        )

    except Exception as error:
        st.error(f"Program error: {error}")
        st.info("Check semicolons, braces, variable names, and division by zero.")

st.divider()
st.caption("Compiler Design Hackathon 2026 | PS-02 — Interpreter vs Compiler Profiler")
