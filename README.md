# dummyBASIC

A tiny educational DBASIC -> FASM compiler written in Python.

This repository contains:
- `main.py` — the compiler script that reads `code.bas` and emits `output.asm`.
- `code.bas` — example/source file you can edit (use your own file name if desired).

Features
- Very small BASIC-like language: `let`, `add`, `sub`, `mul`, `div`, `print`, `prtln`, `tostr`, `toint`.
- Emits FASM-compatible x86_64 assembly and a data segment for strings/variables.
- Minimal runtime helpers (`tostr`, `toint`) are injected only when used.

Prerequisites
- Python 3.7+ to run the compiler (`main.py`).
- (Optional) FASM (Flat Assembler) if you want to assemble the generated `output.asm` into an executable. On Windows you can use WSL to assemble ELF binaries for Linux.

Quick Start
1. Edit or create your `code.bas` in the project root.
2. Run the compiler:

```bash
python main.py
```

3. The compiler writes `output.asm`. To assemble (example for Linux/WSL):

```bash
# install fasm (platform-specific) then
fasm output.asm output
chmod +x output
./output
```

Notes & Limitations
- The compiler is intentionally minimal and does not validate malformed input.
- String literal handling is naive (no escaped quotes); use simple strings.
- Variable declarations are created automatically for `let` statements and stored as 64-bit words (`dq 0`).
- The generated assembly uses Linux syscalls (ELF64). To run on Windows, assemble/target appropriately or run under WSL.

Example `code.bas`
```
let a = 10
let b = 20
add c a b
print "Hello, world"
prtln
```

