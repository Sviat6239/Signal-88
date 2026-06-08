import os

code_line = []
variables = set()
needed_functions = set()
temp_buffer_count = 0

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
        sub rdx, '0'
        imul rax, rcx
        add rax, rdx
        inc rsi
        jmp .loop
    .done:
        ret
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
            variables.add(parts[1])

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
    parts = line.split()
    cmd = parts[0]

    if cmd == 'let':
        if len(parts) >= 4:
            return f"    mov rax, {parts[3]}\n    mov [{parts[1]}], rax\n"
        else:
            return ""

    elif cmd == 'add':
        return f"    mov rax, [{parts[2]}]\n    add rax, [{parts[3]}]\n    mov [{parts[1]}], rax\n"
    
    elif cmd == 'sub':
        return f"    mov rax, [{parts[2]}]\n    sub rax, [{parts[3]}]\n    mov [{parts[1]}], rax\n"
    
    elif cmd == 'mul':
        return f"    mov rax, [{parts[2]}]\n    mov rbx, [{parts[3]}]\n    mul rbx\n    mov [{parts[1]}], rax\n"

    elif cmd == 'div':
        return f"    mov rax, [{parts[2]}]\n    mov rbx, [{parts[3]}]\n    div rbx\n    mov [{parts[1]}], rax\n"
    
    elif cmd  == 'print':
       return "     print func" 

    elif cmd == 'tostr':
        source_var = parts[1]
        buffer_name = f"_temp_str_{temp_buffer_count}"
        temp_buffer_count += 1

        variables.add(f"{buffer_name} rb 20")

        return f"   mov rdi, {buffer_name}\n    mov rax, [{source_var}]\n   call tostr"

    elif cmd == 'toint':
        return "    toint func"

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
for var in variables:
    if ' ' in var:
        output += f"    {var}\n"
    else:
        output += f"    {var} dq 0\n"


print("#Our compiled code:")
print(output)  
print(" ")                  
        
f = open('output.asm', 'w')   
f.write(output)   
print("Code compiled")
