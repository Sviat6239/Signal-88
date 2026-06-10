# dummyBASIC

`dummyBASIC` is a tiny educational DBASIC -> FASM compiler written in Python.
It reads a simple BASIC-like source file, converts it into FASM-compatible x86_64 assembly, and writes the result to `output.asm`.

## Files

- `main.py` - the compiler script.
- `code.bas` - the default source file compiled by `main.py`.
- `code1.bas` - an additional sample source file you can use or rename.
- `output.asm` - generated assembly output.

## Features

- Variable assignment with `let`.
- Arithmetic operations with `add`, `sub`, `mul`, and `div`.
- Output with `print` and `prtln`.
- Runtime helpers for converting numbers to strings and strings to numbers with `tostr` and `toint`.
- Conditional flow with `if`, `elseif`, `else`, and `end if`.
- Generates a readable text section and a writable data section automatically.

## Example Language

The current compiler supports a very small instruction set:

```text
let name = 10
add result left right
sub result left right
mul result left right
div result left right
print "hello"
prtln
tostr value
toint target
if a == 10 then
elseif a == 5 then
else
end if
```

## Prerequisites

- Python 3.7+ to run `main.py`.
- Optional: FASM (Flat Assembler) if you want to assemble the generated `output.asm` into an executable.
- On Windows, WSL is the easiest way to assemble and run the ELF64 output.

## Quick Start

1. Edit `code.bas` in the project root.
2. Run the compiler:

```bash
python main.py
```

3. The compiler writes `output.asm`.
4. Assemble and run it if you have FASM installed:

```bash
fasm output.asm output
chmod +x output
./output
```

## Notes

- The compiler is intentionally minimal and does not yet validate malformed input very deeply.
- String literal handling is naive and does not support escaped quotes.
- Variables declared with `let` are stored as 64-bit values (`dq 0`).
- `print` currently handles string literals directly. If you want to print a number as text, convert it first with `tostr` and then print the variable.
- The generated assembly uses Linux syscalls, so the output is intended for ELF64/Linux-style execution.

## Example `code.bas`

```text
let a = 10
let b = 20
add c a b

tostr a
print a
prtln

if a == 10 then
	print "ten"
elseif a == 5 then
	print "five"
else
	print "other"
end if
```

