# Simple DBASIC-to-FASM compiler
# Reads a very small BASIC-like source file (`code.bas` by default),
# compiles each line into FASM (x86_64) assembly, and writes `output.asm`.
# This script is intentionally minimal and demonstrates a tiny compiler
# pipeline: parse -> compile lines -> emit assembly + data sections.
import os
import time
from linux64 import *

# `code_line` holds non-empty, stripped source lines in order.
# `variables` collects declared variables and string constants used
# by the generated assembly code (mapped to FASM declarations).
code_line = []
variables = {}

# track helper functions and constants that need to be emitted
# (e.g. runtime helpers like `tostr` or data like `prtln` newline)
needed_functions = set()
needed_constants = set()

# counters used to generate unique temporary labels
temp_buffer_count = 0
str_to_print_count = 0

# end time counter
end_time = time.perf_counter()

print("#Our compiled code:") # --\
print(output)                # --- prints the compiled code
print(" ")                   # --/

# writing output fasm code into a file
with open('output.asm', 'w') as f:
    f.write(output)
    f.close
print("Code compiled")

# computes time what was needed to compile
comp_time = end_time - start_time

# path to genereted code for size computing
output = 'output.asm'

file_size = os.path.getsize(file) # computes the source code file size
output_size = os.path.getsize(output) # computes the compiled DBASIC code into FASM code file size

print(f"compiled in {comp_time:.6f} sec") # prints time what was needed to compile code
print(f"source file: {file_size} bytes") # prints sourse code size
print(f"output file: {output_size} bytes") # prints done code size
