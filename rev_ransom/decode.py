"""
void encrypt(longlong file,ulonglong param_2)

{
  undefined8 local_17;
  undefined2 local_f;
  undefined local_d;
  int i;
  
  local_17 = 0x4345535245505553;
  local_f = 0x5255;
  local_d = 0x45;
  for (i = 0; (ulonglong)(longlong)i < param_2; i = i + 1) {
    *(char *)(file + i) =
         *(char *)((longlong)&local_17 + (ulonglong)(longlong)i % 0xb) + *(char *)(file + i);
  }
  return;
}
"""

def decrypt(data):
    local_17 = bytearray(b'SUPERSECURE')
    data = bytearray(data)
    for i in range(len(data)):
        data[i] = (data[i] - local_17[i % 11])
    
    return bytes(data)

#original_data = b'\x9b\xa4\x9c\x86'
#encrypted_data = decrypt(original_data)
#print(encrypted_data)

# Open the file in binary mode and read the bytes
f = open("./login.xlsx.enc", "rb")

file_bytes = f.read()

key = b"SUPERSECURE"

i = 0

for elem in file_bytes:
    print(elem - key[i % 11], end = ", ")
    i += 1

f.close()
