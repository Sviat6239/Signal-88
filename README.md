# dummyBASIC

`dummyBASIC` is a tiny educational DBASIC -> FASM compiler written in Python.
It reads a small BASIC-like source file, converts it into FASM-compatible x86_64 assembly, and writes the result to `output.asm`.

## Files

- `main.py` - the compiler script.
- `code6.bas` - the default source file compiled by `main.py`.
- `code1.bas` - a compact output example.
- `code2.bas` - a simple variable copy example.
- `code3.bas` - a number-to-text and text-to-number example.
- `code4.bas` - an input-buffer example.
- `code5.bas` - a larger arithmetic and conditional example.
- `code7.bas` - a label and jump example.
- `output.asm` - generated assembly output.

## Current State

The compiler currently supports a small but working slice of the language:

- `let` for numeric variables, string literals, bare declarations, and sized input buffers.
- `add`, `sub`, `mul`, and `div`.
- `mov` for direct variable copies.
- `print` for string literals, string variables, and raw input buffers.
- `prtln` for writing a newline.
- `read` for stdin input into a buffer.
- `tostr` and `toint` runtime helpers for converting between numbers and text.
- `if`, `elseif`, `else`, and `end if`.
- `label` and `jmp` for simple local jumps.

The math and base-conversion commands that appear in the parser are currently stubs and are not implemented yet.

## Language Reference

The compiler accepts a small instruction set:

```text
let name = 10
let text = "hello"
let buff 200
mov target source
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
label loop
jmp loop
```

### Statement Notes

- `let name = 10` reserves a 64-bit variable.
- `let buff 200` reserves a byte buffer for input.
- `mov target source` copies one variable into another.
- `print` can print string literals, string variables, and buffers that already contain text.
- `tostr` converts a numeric value into a printable string stored in a temporary buffer.
- `toint` reads text from stdin, parses it as an integer, and stores the result.
- `if` supports `==`, `!=`, `<`, `<=`, `>`, and `>=`.
- `label` and `jmp` are translated directly into local FASM labels and jumps.
- `sqr`, `root`, `pow`, `log`, `log10`, `sin`, `cos`, `tg`, `ctg`, `arc-sin`, `arc-cos`, `arc-tg`, `arc-ctg`, `fact`, `tetr`, `tobin`, `tostrbin`, `todec`, `tostrdec`, `tohex`, `tostrhex`, `tooct`, and `tostroct` are parser stubs only.

## Prerequisites

- Python 3.7+ to run `main.py`.
- Optional: FASM (Flat Assembler) if you want to assemble the generated `output.asm` into an executable.
- On Windows, WSL is the easiest way to assemble and run the ELF64 output.

## Quick Start

1. Edit `code6.bas` in the project root, or change the `file` variable in `main.py` to point at a different source.
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
- `main.py` reads `code6.bas` by default; change the `file` variable near the top of the script if you want a different input file.
- String-backed numeric inputs are parsed with `toint` before arithmetic so `add`, `sub`, `mul`, and `div` operate on values, not ASCII bytes.

## Examples

Simple output from [code1.bas](code1.bas):

```text
print "hello"

prtln
```

Input and conversion from [code4.bas](code4.bas):

```text
let msg1 = "type some thing:>>>"
let buff 200

print msg1
read buff

tostr buff
print buff

prtln
```

Arithmetic and conditionals from [code5.bas](code5.bas):

```text
let numA = 10
let numB = 20
let numC = 0

add numC numA numB
print "text text text"

if numA == 10 then
    print "ten"
elseif numA == 5 then
    print "five"
else
    print "another value"
end if
```

Direct copy and local jumps from [code2.bas](code2.bas) and [code7.bas](code7.bas):

```text
let target = 0
let source = 55

mov target source
```

```text
label labelebele
print "labelebele"
jmp labelebele
```

