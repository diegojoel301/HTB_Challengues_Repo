from Crypto.Cipher import Salsa20

def decrypt(data, key, nonce):
    cipher = Salsa20.new(key=key, nonce=nonce)
    #return cipher.decrypt(ciphertext).decode('utf-8')
    return cipher.decrypt(data)

def encrypt(key, plaintext):
    cipher = Salsa20.new(key=key)
    ciphertext = cipher.nonce + cipher.encrypt(plaintext)
    return ciphertext

key = b"ef39f4f20e76e33bd25f4db338e81b10"
nonce = b"d4c270a3"

data  = b"\x05\x05\x5f\xb1\xa3\x29\xa8\xd5\x58\xd9\xf5\x56\xa6\xcb\x31\xf3"
data += b"\x24\x43\x2a\x31\xc9\x9d\xec\x72\xe3\x3e\xb6\x6f\x62\xad\x1b\xf9"

print(decrypt(data, key, nonce).decode())