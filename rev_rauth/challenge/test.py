from Crypto.Cipher import Salsa20
from binascii import unhexlify

# Clave y nonce proporcionados
key = b"ef39f4f20e76e33bd25f4db338e81b10"
nonce = b"d4c270a3"

# Crear el objeto de cifrado Salsa20 con la clave y el nonce
cipher = Salsa20.new(key=key, nonce=nonce)

# Texto cifrado (ejemplo, debe reemplazarse con el texto cifrado real)
ciphertext  = b"\x05\x05\x5f\xb1\xa3\x29\xa8\xd5\x58\xd9\xf5\x56\xa6\xcb\x31\xf3"
ciphertext += b"\x24\x43\x2a\x31\xc9\x9d\xec\x72\xe3\x3e\xb6\x6f\x62\xad\x1b\xf9"

# Desencriptar
plaintext = cipher.decrypt(ciphertext)

# Imprimir el resultado
#print("Texto desencriptado:", plaintext.decode('utf-8', errors='ignore'))
print(plaintext)
