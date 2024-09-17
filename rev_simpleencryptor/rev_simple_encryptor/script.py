import random
import time

def unsigned_char(value):
    # Garantiza que el valor esté entre 0 y 255
    return value & 0xFF

f = open("flag_enc", "rb")

data = f.read()

f.close()

random.seed(1726586998)

for i in range(0, len(data)):
    #print(int.from_bytes(elem, byteorder='big'))
    
    r1 = random.randint(0, 10**10)
    r2 = random.randint(0, 10**10) & 7

    print(r1)
    print(r2)
    print(unsigned_char(((data[i] >> r2) | (data[i] << (8 - r2))) ^ r1))