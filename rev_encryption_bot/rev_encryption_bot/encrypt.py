"""
gef➤  i b
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   0x000055555555569a 
        breakpoint already hit 1 time
2       breakpoint     keep y   0x00005555555554ba 
        breakpoint already hit 1 time
3       breakpoint     keep y   0x00005555555553e9 
4       breakpoint     keep y   0x0000555555555504 
        breakpoint already hit 6 times
5       breakpoint     keep y   0x00005555555553e9 
6       breakpoint     keep y   0x00005555555555b5 
7       breakpoint     keep y   0x00005555555555a1 
        breakpoint already hit 5 times

"""


"""
undefined8 FUN_001011d9(int param_1)

{
  int a1;
  uint v [20];
  FILE *fd;
  int j;
  int i;
  
  fd = fopen("data.dat","a");
  a1 = param_1;
  for (i = 0; i < 8; i = i + 1) {
    v[i] = a1 % 2;
    a1 = a1 / 2;
  }
  for (j = 7; -1 < j; j = j + -1) {
    fprintf(fd,"%d",(ulong)v[j]);
  }
  fclose(fd);
  return 0;
}
"""
def binary_v(x):
    v = [0 for i in range(8)]

    for i in range(0, 8):
        v[i] = x % 2
        x //= 2

    return [str(elem) for elem in v[::-1]]

def pow_2(x):
    return 2**x

def imprime_caracter(param_1):
    #caracteres = [elem for elem in range(0x52, 0x7a + 1)]
    #caracteres = [0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5a, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f, 0x50, 0x51, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x6b, 0x6c, 0x6d, 0x6e, 0x6f, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x79, 0x7a]
    caracteres = "RSTUVWXYZ0123456789ABCDEFGHIJKLMNOPQabcdefghijklmnopqrstuvwxyz"
    caracteres = [ord(elem) for elem in caracteres]
    return chr(caracteres[param_1%len(caracteres)])


encoded = "aaaaaaaabaaaaaaacaaaaaaadaa"

encoded = "hola_como_3st4s_h0y_p4puuuu"

v = list()

binaryzed = str()

for elem in encoded:
    binaryzed += ''.join(binary_v(ord(elem)))

#print(binaryzed)

i = 6 - 1

for k in range(6, len(binaryzed) + 6, 6):
    i = k - 1

    a2 = 0

    for j in range(0, 6):
        a2 += int(binaryzed[i - j]) * (2**j)

    print(imprime_caracter(a2), end="")



