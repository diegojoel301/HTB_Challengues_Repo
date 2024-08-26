from pwn import *
import string

def output(string):
    io = process("./chall")
    
    io.sendline(string.encode())

    salida = "9W8TL"

    io.recvuntil("9W8TL")
    salida += io.recvline().strip().decode()

    io.close()

    return salida

#force_brute_v = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32, 33, 34, 35]

initial_flag = "HTB{I_4M_R3v3rse_EnG1ne3eR}"
flag_encoded = "9W8TLp4k7t0vJW7n3VvMCpWq9WzT3C8pZ9Wz"

i = 4

#for elem in force_brute_v:
if True:
    ascii_i = 0
    v_ascii = string.ascii_letters + string.digits
    while output(initial_flag)[5] != flag_encoded[5]:
        initial_flag = initial_flag[:i] + v_ascii[i] + initial_flag[(i+1):]
        ascii_i += 1
    print(initial_flag)
