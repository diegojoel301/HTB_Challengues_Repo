#with open("./syscall777_if_1.txt") as f:
with open("./out_1") as f:
    raw_lines = f.readlines()

lines = {}
start_lines = []

# parse
for l in raw_lines:
    if "A = mem[" in l:
        continue
    l = l.split()
    line_id = int(l[0][:-1])
    ope = " ".join(l[5:])
    ope = ope.replace("if", "")
    ope = ope.replace("else", "")
    ope = ope.replace("(A == ", "")
    ope = ope.replace(")", "")
    ope = ope.split(" goto ")
    ope = list(map(int, ope))
    lines[line_id] = ope

    if len(ope) == 2:
        start_lines.append((line_id, ope))

constraints = []
for line_id, (A, next_line) in start_lines:
    constraint = []
    constraint.append(A)
    A, next_line, _ = lines[next_line+1]
    constraint.append(A)
    A, next_line, _ = lines[next_line+1]
    constraint.append(A)
    A, next_line, _ = lines[next_line+1]
    constraint.append(A)
    constraints.append(constraint)

print(constraints)