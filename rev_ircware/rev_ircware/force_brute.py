import re

def give_flag(key):
    flag_encode = [0x09, 0x07, 0x11, 0x48, 0x20, 0x73, 0x02, 0x68, 0x2c, 0x67, 0x62, 0x02, 0x3e, 0x36, 0x7d, 0x1a, 0x1e, 0x35, 0x1f, 0x07, 0x2a, 0x1d, 0x3c, 0x0b, 0x71, 0x25, 0x62, 0x57, 0x7e, 0x30, 0x13, 0x3b, 0x71, 0x07, 0x2e]
    #key = [0x41, 0x53, 0x53, 0x33, i, j]

    i = 0

    ans = str()

    for elem in flag_encode:
        ans += chr(elem ^ key[i % len(key)])
        i += 1

    return ans

for l in range(30, 150):
    for k in range(30, 150):
        for j in range(30, 150):
            for i in range(30, 150):
                key = [0x41, 0x53, 0x53, 0x33, i, j, k, l]
                #patron = r"^HTB{.*}$"
                patron = r"^HTB\{[a-zA-Z0-9_]+\}$"
                if re.match(patron, give_flag(key)):
                    print(give_flag(key))     
