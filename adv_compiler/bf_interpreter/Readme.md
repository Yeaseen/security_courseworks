# Poly-Interpreters Repository

This repository contains interpreters for various esoteric programming languages. Currently, it includes a Brainfuck interpreter written in C.

## Brainfuck Interpreter in C

The Brainfuck interpreter is designed to execute Brainfuck programs, which is a minimalist esoteric programming language created by Urban Müller.

### Prerequisites

To compile and run the Brainfuck interpreter, you will need:

- GCC (GNU Compiler Collection) or another compatible C compiler
- A POSIX-compliant environment (Linux, macOS, or a POSIX layer on Windows such as Cygwin or WSL)

### Compiling the Interpreter

To compile the Brainfuck interpreter, follow these steps:

1. Open your terminal.
2. Navigate to the directory containing the source code file `bf_interpreter.c`.
3. Run the following command to compile the interpreter:

```bash
gcc -o c_bf_interpreter c_bf_interpreter.c
```

This command will create an executable named `c_bf_interpreter` in the same directory.

### Running a Brainfuck Program

To run a Brainfuck program using the compiled interpreter, you can use the following command:

```bash
./bf_interpreter < path/to/your/brainfuck_program.bf
```

Replace path/to/your/brainfuck_program.bf with the path to the Brainfuck file you want to execute.
