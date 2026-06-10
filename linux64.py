
# Pre-defined assembly helpers. When a source line requests a helper
# (for example the `tostr` or `toint` runtime), we add its name to
# `needed_functions` and emit the corresponding assembly below.
FUNCTIONS = {
    'tostr':"""
    tostr:
        mov rcx, 10
        mov rdx, rdi
        add rdi, 19
        mov byte [rdi], 0
    .loop:
        dec rdi
        xor rdx, rdx
        div rcx
        add dl, '0'
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
file = 'code.bas'  # put here the path to your source file

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

    parts = line.split()
    cmd = parts[0]

    # Simple assignment: let X = 123  or let X = Y
    if cmd == 'let':
        if parts[3].isdigit():
            # immediate numeric assignment
            return f"    mov rax, {parts[3]}\n    mov [{parts[1]}], rax\n"
        else:
            # assign from another variable
            return f"    mov rax, [{parts[3]}]\n    mov [{parts[1]}], rax\n"

    # arithmetic operations: add, sub, mul, div
    elif cmd == 'add':
        return f"    mov rax, [{parts[2]}]\n    add rax, [{parts[3]}]\n    mov [{parts[1]}], rax\n"

    elif cmd == 'sub':
        return f"    mov rax, [{parts[2]}]\n    sub rax, [{parts[3]}]\n    mov [{parts[1]}], rax\n"

    elif cmd == 'mul':
        return f"    mov rax, [{parts[2]}]\n    mov rbx, [{parts[3]}]\n    mul rbx\n    mov [{parts[1]}], rax\n"

    elif cmd == 'div':
        return f"    mov rax, [{parts[2]}]\n    mov rbx, [{parts[3]}]\n    div rbx\n    mov [{parts[1]}], rax\n"

    # print string literal or variable
    elif cmd == 'print':
        # string with double quotes
        if parts[1].startswith('"'):
            raw_str = " ".join(parts[1:])
            clean_text = raw_str.strip('"')
            str_label = f"_str_const_{str_to_print_count}"

            # declare a data constant for the string
            variables[str_label] = f"db '{clean_text}', 0"
            str_to_print_count += 1

            # syscall write(1, str, len)
            return (f"    mov rax, 1\n"
                    f"    mov rdi, 1\n"
                    f"    mov rsi, {str_label}\n"
                    f"    mov rdx, {len(clean_text)}\n"
                    f"    syscall\n")

        # string with single quotes
        elif parts[1].startswith("'"):
            raw_str = " ".join(parts[1:])
            clean_text = raw_str.strip("'")
            str_label = f"_str_const_{str_to_print_count}"

            variables[str_label] = f"db '{clean_text}', 0"
            str_to_print_count += 1

            return (f"    mov rax, 1\n"
                    f"    mov rdi, 1\n"
                    f"    mov rsi, {str_label}\n"
                    f"    mov rdx, {len(clean_text)}\n"
                    f"    syscall\n")

        else:
            # printing a variable or unsupported operand
            return ""

    # print newline helper
    elif cmd == 'prtln':
        needed_constants.add('prtln')
        return (f"    mov rax, 1\n"
                f"    mov rdi, 1\n"
                f"    mov rsi, newline\n"
                f"    mov rdx, newline_len\n"
                f"    syscall\n")

    # convert integer to string: call helper that needs a temp buffer
    elif cmd == 'tostr':
        needed_functions.add('tostr')
        source_var = parts[1]
        buffer_name = f"_temp_str_{temp_buffer_count}"
        temp_buffer_count += 1

        variables[buffer_name] = 'rb 20'  # reserve 20 bytes for the string

        return f"    mov rdi, {buffer_name}\n    mov rax, [{source_var}]\n    call tostr"

    # parse string to integer using helper
    elif cmd == 'toint':
        needed_functions.add('toint')
        target_var = parts[1]
        buffer_name = f"_temp_str_{temp_buffer_count}"
        temp_buffer_count += 1

        variables[buffer_name] = 'rb 20'

        return f"    mov rsi, {buffer_name}\n    call toint\n    mov [{target_var}], rax"

    return ""

# compilation of all our saved lines in code_line variable
for line in code_line:
    # compile each collected source line into assembly and append
    output += compile_line(line) + "\n"

# generating an exit command using linux syscall
output += """
    mov rax, 60
    xor rdi, rdi
    syscall
