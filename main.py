code_line = []
variables = set()


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

print("#Our variables:")
print(variables)

def compile_line(line):
    parts = line.split()
    cmd = parts[0]

    if cmd == 'let':
        if len(parts) >= 4:
            return f"    mov rax, {parts[3]}\n    mov [{parts[1]}], rax\n"
        else:
            return ""

    elif cmd == 'add':
        return f"    mov rax, [{parts[2]}]\n    add rax, [{parts[3]}]\n    mov [{parts[1]}], rax\n"

    return ""
for line in code_line:
    output += compile_line(line) + "\n"

output += "\nsegment readable writable\n"
for var in variables:
    output += f"    {var} dq 0\n"

print("#Our compiled code:")
print(output)                    
        