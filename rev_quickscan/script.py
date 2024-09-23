from pwn import *
import angr
import base64
import os

class Binary:
    def __init__(self, file_name):
        self.proj = angr.Project(file_name, auto_load_libs=False)
        self.base_address = self.proj.entry
        self.last_value_rsp = str()

    def hook_syscall(self, state):
        sp = state.regs.rsp

        memory_content = state.memory.load(sp, 32)

        memory_content_bytes = state.solver.eval(memory_content, cast_to=bytes)

        memory_as_hex = memory_content_bytes.hex()[:48]

        self.last_value_rsp = memory_as_hex
    
    def get_last_value_rsp(self):

        syscall_exit = self.base_address + 26

        self.proj.hook(syscall_exit, self.hook_syscall)

        state = self.proj.factory.entry_state()
        simgr = self.proj.factory.simgr(state)

        simgr.explore()

def b64_binary(b64):
    os.system("rm test")
    b64 = b64.strip().decode()
    b64_decode = base64.b64decode(b64)

    f = open("test", "wb")
    f.write(b64_decode)
    f.close()

io = remote("83.136.255.40", 54453)

for i in range(129):
    io.recvuntil("ELF:  ")

    val_b64 = io.recvline()

    b64_binary(val_b64)
    
    b1 = Binary("./test")

    b1.get_last_value_rsp()

    #print("===>", b1.last_value_rsp)

    #print(val_b64)

    io.sendlineafter("Bytes? ", b1.last_value_rsp)

io.interactive()
