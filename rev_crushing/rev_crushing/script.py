from pwn import *

def create_input_file():
    some_bytes = b"""
    Hola como estas?
    HTB{f4k3_fl4g_f0r_t3st1ng}
    magooo
    erjhgu089222s
    """
 
    with open("input", "wb") as binary_file:
        binary_file.write(some_bytes)

#create_input_file()

#f = open("output", "rb")
f = open("message.txt.cz", "rb")

original_data = [b"\x00" for i in range(0x10000)]

data = f.read()

f.close()

release_char = b"\x00"

recolectando_bytes = 0

i = 0

"""
#for i in range(len(data)):
while i < len(data):
    if recolectando_bytes != 1000:
        if data[i] != 0:
            print("Para: ", recolectando_bytes //8)
            recolectando_bytes += 1
            release_char = data[i]
            num_elems = data[i]
            #j = i
            
            while num_elems != 0:
                i += 8
                print(data[i])
                original_data[data[i]] = chr(recolectando_bytes // 8)
                num_elems -= 1
        else:
            recolectando_bytes += 1
    i += 1
"""

release_char = 0

while i < len(data):
    if recolectando_bytes != 1000:
        if data[i] != 0:
            #print("Para: ", hex(recolectando_bytes //8))
            #print("Para: ", hex(data[i]))
            recolectando_bytes += 1
            release_char = data[i]
            num_elems = data[i]
            #j = i
            
            while num_elems != 0:
                i += 8
                #print(data[i:i+2])
                if data[i + 1] != 0:
                    #print(hex(int.from_bytes(data[i:i+2], 'big')))
                    original_data[int.from_bytes(data[i:i+2], 'big')] = chr(recolectando_bytes // 8)
                    if num_elems - 1 == 0:
                        i += 1
                        recolectando_bytes += 1
                else:
                    #print(hex(data[i]))
                    original_data[data[i]] = chr(recolectando_bytes // 8)

                num_elems -= 1
        else:
            recolectando_bytes += 1
    i += 1
        

#print(original_data)

for elem in original_data:
    if elem != b"\x00":
        print(elem, end="")
