# dummyBASIC

`dummyBASIC` is a tiny educational DBASIC -> FASM compiler written in Python.
It reads a small BASIC-like source file, converts it into FASM-compatible x86_64 assembly, and writes the result to `output.asm`.

## Files

- `main.py` - the compiler script.
- `code.bas` - the default source file compiled by `main.py`.
- `code1.bas` - an additional sample source file you can use or rename.
- `code3.bas` and `code4.bas` - extra sample programs used for testing edge cases.
- `output.asm` - generated assembly output.

## What It Supports

- Variable assignment with `let`.
- Arithmetic operations with `add`, `sub`, `mul`, and `div`.
- Output with `print` and `prtln`.
- Input with `read`.
- Runtime helpers for converting numbers to strings and strings to numbers with `tostr` and `toint`.
- Conditional flow with `if`, `elseif`, `else`, and `end if`.
- Generates a readable text section and a writable data section automatically.

## Language Reference

The compiler accepts a small instruction set:

```text
let name = 10
let text = "hello"
let buff 200
add result left right
sub result left right
mul result left right
div result left right
print "hello"
print name
prtln
read buff
tostr value
toint target
if a == 10 then
elseif a == 5 then
else
end if
```

### Statement Notes

- `let name = 10` reserves a 64-bit variable.
- `let buff 200` reserves a byte buffer for input.
- `print` can print string literals, string variables, and buffers that already contain text.
- `tostr` converts a numeric value into a printable string stored in a temporary buffer.
- `toint` reads text from stdin, parses it as an integer, and stores the result.
- `if` supports `==`, `!=`, `<`, `<=`, `>`, and `>=`.

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

- The compiler is intentionally minimal and does not validate malformed input very deeply.
- String literal handling is naive and does not support escaped quotes.
- Variables declared with `let` are stored as 64-bit values unless they are declared as buffers.
- The generated assembly uses Linux syscalls, so the output is intended for ELF64/Linux-style execution.
- `main.py` always reads `code.bas` by default; change the `file` variable near the top of the script if you want a different input file.

## Example `code.bas`

```text
let a = 10
let b = 20
add c a b
print c

tostr a
print a
read buff
prtln

if a == 10 then
	print "ten"
elseif a == 5 then
	print "five"
else
	print "other"
end if
```

