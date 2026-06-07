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

def compile_line():
    parts = line.split()
    cmd = parts[0]

    if cmd == 'let':
        var_name = parts[1]
        val = parts[3]
        