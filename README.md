# Signal-88

This repository contains a small experimental frontend for a BASIC-like language. The current implementation is written in C and focuses on lexical analysis and parser scaffolding rather than full compilation to machine code or assembly.

## Project structure

- [singal-88.c](singal-88.c) — command-line entry point. It reads a source file from the command line, prints the source, tokenizes it, and attempts to build an AST.
- [frontend/lexer.c](frontend/lexer.c) and [frontend/include/lexer.h](frontend/include/lexer.h) — lexer implementation. It recognizes numbers, strings, characters, identifiers, operators, and many keywords.
- [frontend/parser.c](frontend/parser.c) and [frontend/include/parser.h](frontend/include/parser.h) — parser and AST scaffolding. The implementation is still incomplete and currently only provides placeholder logic.
- [frontend/utils.c](frontend/utils.c) and [frontend/include/utils.h](frontend/include/utils.h) — helper code for reading files.
- [legacy/](legacy/) — older BASIC examples and a previous Python prototype that are not wired into the current C-based frontend.
- [compile.ps1](compile.ps1) — build helper script, but it still points to an older command and should be updated.

## Current status

The codebase is a work in progress:

- The lexer already handles a broad set of token types, including arithmetic operators, comparisons, string literals, and keywords such as let, print, read, if, else, label, and jmp.
- The parser is not fully implemented yet.
- There is no working FASM backend or generated assembly pipeline in the current code.
- A fresh compile attempt still reports inconsistencies in the lexer/parser headers and token definitions, so the project does not build cleanly yet.

## Build

The project can be compiled with:

```bash
clang singal-88.c frontend/lexer.c frontend/parser.c frontend/utils.c -Ifrontend/include -o signal88.exe
```

Run it with:

```bash
./signal88.exe path/to/source.txt
```

On Windows, the executable will be named `signal88.exe`.

## Usage notes

- The program expects the path to a source file as its first command-line argument.
- The current output is mainly diagnostic: it prints the source, the token list, and the AST structure.
- The implementation is educational and experimental, so input validation and full language support are still incomplete.

## Notes for contributors

If you want to extend the project, the most natural next steps are:

1. Finish the parser and AST construction logic.
2. Define a clear intermediate representation for statements and expressions.
3. Add a backend that emits assembly or another target format.
4. Bring [compile.ps1](compile.ps1) in line with the current build steps.

