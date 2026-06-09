import os
import time

code_line = []
variables = {}

needed_functions = set()
needed_constants = set()

temp_buffer_count = 0
str_to_print_count = 0

start_time = time.perf_counter()

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

CONSTANTS = {
    'prtln':"""
    newline db '', 10, 0
    newline_len = $ - newline
    """
}

file = 'code.bas'

f = open(file, 'r')


for line in f:
    line = line.strip()
    if line:
        code_line.append(line)
        parts = line.split()
        if parts[0] == "let":
            variables[parts[1]] = 'dq 0'

output = "format elf64 executable 3\nentry _start\n\n"
output += "segment readable executable\n_start:\n"            

print("#Our code lines:")
print(code_line)  
print(" ")  

print("#Our variables:")
print(variables)
print(" ")

def compile_line(line):
    global temp_buffer_count
    global str_to_print_count

    parts = line.split()
    cmd = parts[0]

    if cmd == 'let':
        if parts[3].isdigit():
            return f"    mov rax, {parts[3]}\n    mov [{parts[1]}], rax\n"
        else:
            return f"    mov rax, [{parts[3]}]\n    mov [{parts[1]}], rax\n"

    elif cmd == 'add':
        return f"    mov rax, [{parts[2]}]\n    add rax, [{parts[3]}]\n    mov [{parts[1]}], rax\n"
    
    elif cmd == 'sub':
        return f"    mov rax, [{parts[2]}]\n    sub rax, [{parts[3]}]\n    mov [{parts[1]}], rax\n"
    
    elif cmd == 'mul':
        return f"    mov rax, [{parts[2]}]\n    mov rbx, [{parts[3]}]\n    mul rbx\n    mov [{parts[1]}], rax\n"

    elif cmd == 'div':
        return f"    mov rax, [{parts[2]}]\n    mov rbx, [{parts[3]}]\n    div rbx\n    mov [{parts[1]}], rax\n"
    
    elif cmd == 'print':
        if parts[1].startswith('"'):
            raw_str = " ".join(parts[1:])
            clean_text = raw_str.strip('"')
            str_label = f"_str_const_{str_to_print_count}"

            variables[str_label] = f"db '{clean_text}', 0"
            str_to_print_count += 1

            return (f"    mov rax, 1\n"
                    f"    mov rdi, 1\n"
                    f"    mov rsi, {str_label}\n"
                    f"    mov rdx, {len(clean_text)}\n"
                    f"    syscall\n")

        else:
            return ""

    elif cmd == 'prtln':
        needed_constants.add('prtln')
        return (f"    mov rax, 1\n"
                f"    mov rdi, 1\n"
                f"    mov rsi, newline\n"
                f"    mov rdx, newline_len\n"
                f"    syscall\n")

    elif cmd == 'tostr':
        needed_functions.add('tostr')
        source_var = parts[1]
        buffer_name = f"_temp_str_{temp_buffer_count}"
        temp_buffer_count += 1

        variables[buffer_name] = 'rb 20'

        return f"    mov rdi, {buffer_name}\n    mov rax, [{source_var}]\n    call tostr"

    elif cmd == 'toint':
        needed_functions.add('toint')
        target_var = parts[1]
        buffer_name = f"_temp_str_{temp_buffer_count}"
        temp_buffer_count += 1

        variables[buffer_name] = 'rb 20'
        
        return f"    mov rsi, {buffer_name}\n    call toint\n    mov [{target_var}], rax"
    return ""

for line in code_line:
    output += compile_line(line) + "\n"

output += """
    mov rax, 60
    xor rdi, rdi
    syscall
"""    

for func_name in needed_functions:
    output += FUNCTIONS[func_name] + "\n"

output += "\nsegment readable writable\n"
for var, declaration in variables.items():
    if declaration.startswith('db'):
        output += f"    {var} {declaration}\n"
    elif declaration == 'rb 20':
        output += f"    {var} rb 20\n"
    else:
        output += f"    {var} dq 0\n"

for const_name in needed_constants:
    output += CONSTANTS[const_name] + "\n"

print("#Our compiled code:")
print(output)  
print(" ")                  
        
with open('output.asm', 'w') as f:
    f.write(output)
    f.close
print("Code compiled")
end_time = time.perf_counter()

comp_time = end_time - start_time

output = 'output.asm'

file_size = os.path.getsize(file)
output_size = os.path.getsize(output)

print(f"compiled in {comp_time:.6f} sec")
print(f"source file: {file_size} bytes")
print(f"output file: {output_size} bytes")
