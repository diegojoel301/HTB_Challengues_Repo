with open("./out") as f:
    raw_lines = f.readlines()

lines = {}
start_lines = []

for l in raw_lines:
    if "A = args[" in l or "":
        continue

    l = l.split()
    line_id = int(l[0][:-1])
    ope = " ".join(l[5:])
    ope = ope.replace("if", "")
    ope = ope.replace("(A == ", "")
    ope = ope.replace(")", "")
    ope = ope.split(" goto ")
    print(ope)
    ope = list(map(int, ope))
    #ope = list(map(lambda x: int(x, 0), ope))
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