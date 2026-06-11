# Simple DBASIC-to-FASM compiler
# Reads a very small BASIC-like source file (`code.bas` by default),
# compiles each line into FASM (x86_64) assembly, and writes `output.asm`.
# This script is intentionally minimal and demonstrates a tiny compiler
# pipeline: parse -> compile lines -> emit assembly + data sections.
import os
import time

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
if_label_count = 0
if_stack = []
# remember which variable currently has a string buffer produced by `tostr`
# value: name of a pointer variable that stores the actual string start address
string_buffers = {}

# Pre-defined assembly helpers. When a source line requests a helper
# (for example the `tostr` or `toint` runtime), we add its name to
# `needed_functions` and emit the corresponding assembly below.
# `tostr` walks backward through a temp buffer, writes the NUL byte,
# then repeatedly divides by 10 to emit ASCII digits.
# `toint` scans a digit string from left to right, multiplies the
# accumulator by 10, and adds the next digit value.
FUNCTIONS = {
    'tostr':"""
    tostr:
        mov rcx, 10
        lea rdi, [rdi + 19]
        mov byte [rdi], 0
        cmp rax, 0
        jne .loop
        dec rdi
        mov byte [rdi], '0'
        ret
    .loop:
        xor rdx, rdx
        div rcx
        add dl, '0'
        dec rdi
        mov [rdi], dl
        test rax, rax
        jnz .loop
        ret
    """,
        'toint':"""
    toint:
        xor rax, rax
        mov rcx, 10
    .loop:
        movzx rdx, byte [rsi]
        cmp rdx, 0
        je .done
        cmp rdx, '0'
        jl .done
        cmp rdx, '9'
        jg .done
        sub rdx, '0'
        imul rax, rcx
        add rax, rdx
        inc rsi
        jmp .loop
    .done:
        ret
    """, 
        'tobin':"""
    """,
        'tostrbin':"""
    """,
        'todec':"""
    """,
        'tostrdec':"""
    """,
        'tohex':"""
    """,
        'tostrhex':"""
    """,
        'tooct':"""
    """,
        'tostroct':"""
    """
}

# Pre-defined data constants (emitted into the data segment when used)
CONSTANTS = {
    'prtln':"""
    newline db '', 10, 0
    newline_len = $ - newline
    """
}

# source file to compile. Change to any path as needed.
file = 'code6.bas'  # put here the path to your source file

# start a timer to show compilation duration
start_time = time.perf_counter()

# open the source file for reading (no error handling for brevity)
f = open(file, 'r')

# Read each non-empty line and collect it for compilation.
# Also pre-declare variables when a `let` statement appears.
for line in f:
    line = line.strip()
    if line:
        code_line.append(line)
        parts = line.split()  # tokenize the line by whitespace
        # `let <name> = <value>` creates a storage slot for the variable
        if parts[0] == "let":
            if len(parts) == 3 and parts[2].isdigit():
                variables[parts[1]] = f"rb {parts[2]}"
            else:
                variables[parts[1]] = 'dq 0'

output = "format elf64 executable 3\nentry _start\n\n"  # ELF header and entry point
output += "segment readable executable\n_start:\n"  # text/code segment and _start label

print("#Our code lines:")
print(code_line)          # display the parsed source lines
print(" ")

print("#Our variables:")
print(variables)          # display variables / data declarations collected
print(" ")

# the compiler
def compile_line(line):
    """Compile a single tokenized source line into a string of FASM
    instructions. This function returns the assembly snippet for the
    given source statement or an empty string for unrecognized lines.
    """
    global temp_buffer_count
    global str_to_print_count
    global if_label_count
    global if_stack
    global string_buffers

    parts = line.split()
    cmd = parts[0]

    def compile_operand(token):
        """Check if token is a numeric immediate or a variable reference.
        Returns (operand_str, var_name_or_none).
        - If numeric: returns (number, None)
        - If variable: returns ([varname], varname)  for indirect addressing
        """
        if token.lstrip('-').isdigit():
            return token, None
        return f"[{token}]", token

    def compile_condition(left_token, operator, right_token, false_label):
        """Compile a conditional expression (left_token operator right_token).
        Generates assembly that loads operands and jumps to false_label if condition is false.
        Handles comparisons: ==, !=, <, <=, >, >=
        Returns the assembly code string.
        """
        left_operand, left_var = compile_operand(left_token)
        right_operand, right_var = compile_operand(right_token)

        # mov rax, <left> loads the left operand into the accumulator.
        asm = f"    mov rax, {left_operand}\n"
        # mov rbx, <right> loads the right operand when both sides are variables.
        # cmp rax, rbx compares both values directly.
        if left_var is not None and right_var is not None:
            asm += f"    mov rbx, {right_operand}\n"
            asm += "    cmp rax, rbx\n"
        else:
            # cmp rax, <right> handles immediates or one-variable comparisons.
            asm += f"    cmp rax, {right_operand}\n"

        # Map operators to inverse jump instructions (we jump if condition is false)
        jump_map = {
            '==': 'jne',
            '!=': 'je',
            '<': 'jge',
            '<=': 'jg',
            '>': 'jle',
            '>=': 'jl',
        }

        jump = jump_map.get(operator)
        if jump is None:
            raise ValueError(f"Unsupported operator in if-condition: {operator}")

        # jne/jge/jg/jle/jl/jne jumps to the false label when the test fails.
        asm += f"    {jump} {false_label}\n"
        return asm

    def compile_numeric_operand(token, target_reg):
        """Load a token as a numeric value into target_reg.

        Numeric literals are moved directly. Variables backed by string
        buffers are parsed with `toint` first so arithmetic works on the
        actual digits instead of the raw ASCII bytes.
        """
        declaration = variables.get(token)

        if token.lstrip('-').isdigit():
            # mov <reg>, <imm> loads a numeric literal directly.
            return f"    mov {target_reg}, {token}\n"

        if declaration and (declaration.startswith('rb ') or declaration.startswith('db ')):
            needed_functions.add('toint')
            # mov rsi, <token> points the parser at the text buffer.
            # call toint converts the string digits into an integer.
            # mov <reg>, rax keeps the parsed value in the requested register.
            asm = f"    mov rsi, {token}\n    call toint\n"
            if target_reg != 'rax':
                asm += f"    mov {target_reg}, rax\n"
            return asm

        # mov <reg>, [token] loads a numeric variable from memory.
        return f"    mov {target_reg}, [{token}]\n"

    # Simple assignment: let X = 123  or let X = Y
    if cmd == 'let':
        if len(parts) == 2:
            # Bare declaration such as `let buff` is handled in the
            # pre-scan phase and does not need emitted code here.
            return ""

        if len(parts) == 3 and parts[2].isdigit():
            # Buffer declaration such as `let buff 200` is also handled by
            # the pre-scan phase and does not need emitted code here.
            return ""

        if len(parts) < 4:
            raise ValueError(f"Malformed let statement: {line}")

        if parts[3].startswith('"'):
            raw_str = " ".join(parts[3:])
            clean_text = raw_str.strip('"')
            variables[parts[1]] = f"db '{clean_text}', 0"
            return ""
        elif parts[3].isdigit():
            # immediate numeric assignment
            # mov rax, imm loads the literal.
            # mov [dst], rax stores it into the destination variable.
            return f"    mov rax, {parts[3]}\n    mov [{parts[1]}], rax\n"
        else:
            # assign from another variable
            # mov rax, [src] reads the source variable.
            # mov [dst], rax copies it into the destination variable.
            return f"    mov rax, [{parts[3]}]\n    mov [{parts[1]}], rax\n"

    # arithmetic operations: add, sub, mul, div
    elif cmd == 'add':
        if len(parts) < 4:
            raise ValueError(f"Malformed add statement: {line}")
        # rbx gets the right operand first so later toint calls cannot overwrite rax.
        # rax gets the left operand second.
        # add rax, rbx writes the sum back into rax.
        return (
            compile_numeric_operand(parts[3], 'rbx')
            + compile_numeric_operand(parts[2], 'rax')
            + f"    add rax, rbx\n    mov [{parts[1]}], rax\n"
        )

    elif cmd == 'sub':
        if len(parts) < 4:
            raise ValueError(f"Malformed sub statement: {line}")
        # rbx gets the right operand first.
        # rax gets the left operand second.
        # sub rax, rbx computes left minus right.
        return (
            compile_numeric_operand(parts[3], 'rbx')
            + compile_numeric_operand(parts[2], 'rax')
            + f"    sub rax, rbx\n    mov [{parts[1]}], rax\n"
        )

    elif cmd == 'mul':
        if len(parts) < 4:
            raise ValueError(f"Malformed mul statement: {line}")
        # rbx gets the right operand first.
        # rax gets the left operand second.
        # mul rbx multiplies rax by rbx and leaves the result in rax.
        return (
            compile_numeric_operand(parts[3], 'rbx')
            + compile_numeric_operand(parts[2], 'rax')
            + f"    mul rbx\n    mov [{parts[1]}], rax\n"
        )

    elif cmd == 'div':
        if len(parts) < 4:
            raise ValueError(f"Malformed div statement: {line}")
        # rbx gets the divisor.
        # rax gets the dividend.
        # xor rdx, rdx clears the high half before div.
        return (
            compile_numeric_operand(parts[3], 'rbx')
            + compile_numeric_operand(parts[2], 'rax')
            + "    xor rdx, rdx\n    div rbx\n"
            + f"    mov [{parts[1]}], rax\n"
        )

    elif cmd == 'sqr':
        pass

    elif cmd == 'root':
        pass

    elif cmd == 'pow':
        pass

    elif cmd == 'log':
        pass

    elif cmd == 'log10':
        pass

    elif cmd == 'sin':
        pass

    elif cmd == 'cos':
        pass

    elif cmd == 'tg':
        pass

    elif cmd == 'ctg':
        pass

    elif cmd == 'arc-sin':
        pass

    elif cmd == 'arc-cos':
        pass

    elif cmd == 'arc-tg':
        pass

    elif cmd == 'arc-ctg':
        pass

    elif cmd == 'fact':
        pass

    elif cmd == 'tetr':
        pass

    elif cmd == 'mov':
        if len(parts) < 3:
            raise ValueError(f"Malformed mov statement: {line}")
        # mov [dst], [src] copies the value from one variable location to another.
        return f"    mov [{parts[1]}], [{parts[2]}]"    

    # print string literal or variable
    elif cmd == 'print':
        # string with double quotes
        if parts[1].startswith('"'):
            raw_str = " ".join(parts[1:])
            clean_text = raw_str.strip('"')
            str_label = f"_str_const_{str_to_print_count}"

            # Store the literal in the writable data section so the runtime can
            # print it by address.
            variables[str_label] = f"db '{clean_text}', 0"
            str_to_print_count += 1

            # mov rax, 1 selects the write syscall.
            # mov rdi, 1 targets stdout.
            # mov rsi, <label> points to the string.
            # repne scasb finds the NUL terminator.
            # mov rdx, rcx supplies the byte count.
            return (f"    mov rax, 1\n"
                f"    mov rdi, 1\n"
                f"    mov rsi, {str_label}\n"
                f"    mov rdi, rsi\n"
                f"    mov rcx, -1\n"
                f"    xor al, al\n"
                f"    repne scasb\n"
                f"    not rcx\n"
                f"    dec rcx\n"
                f"    mov rdx, rcx\n"
                f"    mov rdi, 1\n"
                f"    syscall\n")

        # string with single quotes
        elif parts[1].startswith("'"):
            raw_str = " ".join(parts[1:])
            clean_text = raw_str.strip("'")
            str_label = f"_str_const_{str_to_print_count}"

            # Single-quoted text is handled the same way as double-quoted text.
            variables[str_label] = f"db '{clean_text}', 0"
            str_to_print_count += 1

            # Same write sequence as the double-quoted case.
            return (f"    mov rax, 1\n"
                    f"    mov rdi, 1\n"
                    f"    mov rsi, {str_label}\n"
                    f"    mov rdi, rsi\n"
                    f"    mov rcx, -1\n"
                    f"    xor al, al\n"
                    f"    repne scasb\n"
                    f"    not rcx\n"
                    f"    dec rcx\n"
                    f"    mov rdx, rcx\n"
                    f"    mov rdi, 1\n"
                    f"    syscall\n")

        else:
            # printing a variable: if it was passed through `tostr`, use the
            # stored string pointer; otherwise we do not have a direct
            # integer-to-text printer yet.
            source_name = parts[1]

            # `tostr` stores the actual string start address in a pointer slot,
            # so `print` can reuse the generated buffer without recomputing it.
            if source_name in string_buffers:
                pointer_name = string_buffers[source_name]
                # mov rsi, [pointer] loads the saved string start.
                # The rest of the sequence measures length and writes to stdout.
                return (f"    mov rax, 1\n"
                        f"    mov rsi, [{pointer_name}]\n"
                        f"    mov rdi, rsi\n"
                        f"    mov rcx, -1\n"
                        f"    xor al, al\n"
                        f"    repne scasb\n"
                        f"    not rcx\n"
                        f"    dec rcx\n"
                        f"    mov rdx, rcx\n"
                        f"    mov rdi, 1\n"
                        f"    syscall\n")

            declaration = variables.get(source_name)
            # Raw input buffers are already strings, so they can be printed as-is.
            if declaration and declaration.startswith('rb '):
                # Same write sequence, but the source is the raw input buffer.
                return (f"    mov rax, 1\n"
                        f"    mov rsi, {source_name}\n"
                        f"    mov rdi, rsi\n"
                        f"    mov rcx, -1\n"
                        f"    xor al, al\n"
                        f"    repne scasb\n"
                        f"    not rcx\n"
                        f"    dec rcx\n"
                        f"    mov rdx, rcx\n"
                        f"    mov rdi, 1\n"
                        f"    syscall\n")

            declaration = variables.get(source_name)
            # Static text declared with `db` is also written directly by address.
            if declaration and declaration.startswith('db '):
                # Same write sequence, but the source is static string data.
                return (f"    mov rax, 1\n"
                        f"    mov rdi, 1\n"
                        f"    mov rsi, {source_name}\n"
                        f"    mov rdi, rsi\n"
                        f"    mov rcx, -1\n"
                        f"    xor al, al\n"
                        f"    repne scasb\n"
                        f"    not rcx\n"
                        f"    dec rcx\n"
                        f"    mov rdx, rcx\n"
                        f"    mov rdi, 1\n"
                        f"    syscall\n")

            # Unknown value types are ignored for now rather than crashing.
            return ""

    # print newline helper
    elif cmd == 'prtln':
        needed_constants.add('prtln')
        # mov rax, 1 selects write.
        # mov rdi, 1 targets stdout.
        # mov rsi, newline points at the newline text.
        # mov rdx, newline_len writes the single line break.
        return (f"    mov rax, 1\n"
                f"    mov rdi, 1\n"
                f"    mov rsi, newline\n"
                f"    mov rdx, newline_len\n"
                f"    syscall\n")

    elif cmd == 'read':
        if len(parts) < 2:
            raise ValueError(f"Malformed read statement: {line}")

        buffer_name = parts[1]
        buffer_decl = variables.get(buffer_name)

        # Use the declared buffer size when available; otherwise fall back to a
        # small fixed input buffer so the generated code can still read safely.
        if buffer_decl and buffer_decl.startswith('rb '):
            buffer_size = buffer_decl.split()[1]
        else:
            buffer_size = '200'

        # mov rax, 0 selects read.
        # mov rdi, 0 targets stdin.
        # mov rsi, buffer_name points to the destination buffer.
        # mov rdx, size limits the read and keeps space for NUL.
        # mov byte [buffer + rax], 0 terminates the input string.
        return (
            f"    mov rax, 0\n"
            f"    mov rdi, 0\n"
            f"    mov rsi, {buffer_name}\n"
            f"    mov rdx, {buffer_size}\n"
            f"    dec rdx\n"
            f"    syscall\n"
            f"    mov byte [{buffer_name} + rax], 0\n"
        )

    # convert integer to string: call helper that needs a temp buffer
    elif cmd == 'tostr':
        needed_functions.add('tostr')
        source_var = parts[1]

        declaration = variables.get(source_var)
        if declaration and declaration.startswith('rb '):
            # Buffers coming from `read` contain text, so parse them to an
            # integer first and then format that value back into a temp string.
            # For input buffers, first parse the text as an integer and then
            # convert that integer back to a string in a dedicated temp buffer.
            needed_functions.add('toint')
            buffer_name = f"_temp_str_{temp_buffer_count}"
            pointer_name = f"_temp_str_ptr_{temp_buffer_count}"
            temp_buffer_count += 1

            variables[buffer_name] = 'rb 20'
            variables[pointer_name] = 'dq 0'
            string_buffers[source_var] = pointer_name

                # mov rsi, source_var points to text input.
                # call toint parses that text as an integer.
                # mov rdi, buffer_name selects the output buffer.
                # call tostr renders the integer as decimal text.
                # mov [pointer_name], rdi stores the start pointer for printing.
            return (f"    mov rsi, {source_var}\n"
                    f"    call toint\n"
                    f"    mov rdi, {buffer_name}\n"
                    f"    call tostr\n"
                    f"    mov [{pointer_name}], rdi\n")

        buffer_name = f"_temp_str_{temp_buffer_count}"
        pointer_name = f"_temp_str_ptr_{temp_buffer_count}"
        temp_buffer_count += 1

        # Reserve a temporary string buffer and remember where `tostr` placed
        # the actual start address so later `print` calls can reuse it.
        variables[buffer_name] = 'rb 20'  # reserve 20 bytes for the string
        variables[pointer_name] = 'dq 0'   # store the actual start pointer returned by tostr
        # remember which pointer belongs to this variable so `print` can reuse it
        string_buffers[source_var] = pointer_name

        # mov rdi, buffer_name selects the destination buffer.
        # mov rax, [source_var] loads the number to format.
        # call tostr writes the decimal representation.
        # mov [pointer_name], rdi preserves the actual start address.
        return (f"    mov rdi, {buffer_name}\n"
            f"    mov rax, [{source_var}]\n"
            f"    call tostr\n"
            f"    mov [{pointer_name}], rdi")

    # parse string to integer using helper
    elif cmd == 'toint':
        needed_functions.add('toint')
        target_var = parts[1]
        buffer_name = f"_temp_str_{temp_buffer_count}"
        temp_buffer_count += 1

        # Read text from stdin into a temporary buffer, terminate it, and let
        # the helper convert the digits into a numeric value.
        variables[buffer_name] = 'rb 20'

        # mov rax, 0 selects read.
        # mov rdi, 0 targets stdin.
        # mov rsi, buffer_name stores typed digits.
        # mov rdx, 20 caps the read length.
        # mov byte [buffer + rax], 0 NUL-terminates the input.
        # mov rsi, buffer_name points the parser at the text.
        # call toint parses the digits.
        # mov [target_var], rax stores the numeric result.
        return (
            f"    mov rax, 0\n"
            f"    mov rdi, 0\n"
            f"    mov rsi, {buffer_name}\n"
            f"    mov rdx, 20\n"
            f"    dec rdx\n"
            f"    syscall\n"
            f"    mov byte [{buffer_name} + rax], 0\n"
            f"    mov rsi, {buffer_name}\n"
            f"    call toint\n"
            f"    mov [{target_var}], rax"
        )

    elif cmd == 'tobin':
        pass

    elif cmd == 'tostrbin':
        pass

    elif cmd == 'todec':
        pass

    elif cmd == 'tostrdec':
        pass

    elif cmd == 'tohex':
        pass

    elif cmd == 'tostrhex':
        pass

    elif cmd == 'tooct':
        pass

    elif cmd == 'tostroct':
        pass

    elif cmd == "if":
        # Parse: if <left> <operator> <right> then
        # Note: 'then' is optional and ignored during tokenization
        if len(parts) < 5:
            raise ValueError(f"Malformed if statement: {line}")

        # Generate unique labels for this if block
        end_label = f"_if_end_{if_label_count}"
        false_label = f"_if_false_{if_label_count}"
        if_label_count += 1

        # Push control state onto stack (will be popped by 'end if')
        if_stack.append({
            'end_label': end_label,      # where to jump when entire if/elseif/else block is done
            'false_label': false_label,  # where to jump if this condition fails
            'has_else': False,           # track if an else clause has been seen
        })

        # Generate condition check and conditional jump to false_label
        return compile_condition(parts[1], parts[2], parts[3], false_label)

    elif cmd == "elseif":
        # Parse: elseif <left> <operator> <right> then
        if not if_stack:
            raise ValueError(f"elseif without matching if: {line}")
        if len(parts) < 5:
            raise ValueError(f"Malformed elseif statement: {line}")

        current = if_stack[-1]
        # Generate new false label for this elseif's condition
        new_false_label = f"_if_false_{if_label_count}"
        if_label_count += 1

        # If previous if/elseif block was taken, jump to end_label
        # Otherwise, place label where previous false_label pointed to
        asm = (
            f"    jmp {current['end_label']}\n"
            f"{current['false_label']}:\n"
        )
        # Check the new elseif condition and jump to new_false_label if fails
        asm += compile_condition(parts[1], parts[2], parts[3], new_false_label)
        # Update stack so next elseif/else uses new_false_label
        current['false_label'] = new_false_label
        return asm

    elif cmd == "else":
        # else block (no condition): label previous false_label and prepare to skip to end
        if not if_stack:
            raise ValueError(f"else without matching if: {line}")

        current = if_stack[-1]
        # Verify only one else per if block
        if current['has_else']:
            raise ValueError(f"duplicate else in the same if block: {line}")
        current['has_else'] = True

        # Jump to end_label if we took any previous condition
        # Place label at false_label so code falls through to else block
        return (
            f"    jmp {current['end_label']}\n"
            f"{current['false_label']}:\n"
        )

    elif cmd == "end" and len(parts) > 1 and parts[1] == "if":
        # end if: close the if/elseif/else block and place end_label
        if not if_stack:
            raise ValueError(f"end if without matching if: {line}")

        # Pop control state for this if block
        current = if_stack.pop()
        asm = ""
        # If there was no else clause, place the final false_label here
        # (so if all conditions fail, execution continues from here)
        if not current['has_else']:
            asm += f"{current['false_label']}:\n"
        # Place end_label to mark end of entire if/elseif/else block
        asm += f"{current['end_label']}:\n"
        return asm

    if cmd == 'label':
        return f".{parts[1]}:"

    if cmd == 'jmp':
        return f"   jmp .{parts[1]}"

    return ""


# compilation of all our saved lines in code_line variable
    # Each source line expands to one or more assembly instructions that are
    # appended to the executable text section in order.
for line in code_line:
    # compile each collected source line into assembly and append
    output += compile_line(line) + "\n"

# generating an exit command using linux syscall
# mov rax, 60 selects exit.
# xor rdi, rdi sets the return code to zero.
# syscall terminates the program.
output += """
    mov rax, 60
    xor rdi, rdi
    syscall
"""

# generating all mentioned in sourse code function bellow the exit block
for func_name in needed_functions:
    # emit helper function code if requested by the source
    output += FUNCTIONS[func_name] + "\n"

output += "\nsegment readable writable\n"
for var, declaration in variables.items():
    # emit data declarations collected while compiling lines
    if declaration.startswith('db'):
        output += f"    {var} {declaration}\n"
    elif declaration.startswith('rb '):
        output += f"    {var} {declaration}\n"
    else:
        output += f"    {var} dq 0\n"

for const_name in needed_constants:
    # emit any required constant blocks (e.g. newline bytes)
    output += CONSTANTS[const_name] + "\n"

# Print the generated assembly and save it to disk so the compiler can be used
# as a simple one-step source-to-output tool.
print("#Our compiled code:") # --\
print(output)                # --- prints the compiled code
print(" ")                   # --/

# writing output fasm code into a file
with open('output.asm', 'w') as f:
    f.write(output)
    f.close
print("Code compiled")

# end time counter
end_time = time.perf_counter()

# computes time what was needed to compile
comp_time = end_time - start_time

# path to genereted code for size computing
output = 'output.asm'

file_size = os.path.getsize(file) # computes the source code file size
output_size = os.path.getsize(output) # computes the compiled DBASIC code into FASM code file size

print(f"compiled in {comp_time:.6f} sec") # prints time what was needed to compile code
print(f"source file: {file_size} bytes") # prints sourse code size
print(f"output file: {output_size} bytes") # prints done code size
