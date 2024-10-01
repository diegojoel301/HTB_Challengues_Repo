from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import binascii

def decrypt(hex_data, key, iv):
    # Convertir el string hexadecimal a bytes
    cipher_text = binascii.unhexlify(hex_data)
    
    # Crear un objeto Cipher
    cipher = Cipher(algorithms.AES(key.encode('utf-8')), modes.CBC(iv.encode('utf-8')), backend=default_backend())
    
    # Crear un objeto de descifrado
    decryptor = cipher.decryptor()
    
    # Desencriptar el texto cifrado
    decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()
    
    # Devolver el texto desencriptado
    return decrypted_data.decode('utf-8')

# Ejemplo de uso
hex_data = "E242E64261D21969F65BEDF954900A995209099FB6C3C682C0D9C4B275B1C212BC188E0882B6BE72C749211241187FA8"  # Reemplaza con tu string hex
key = "_NOT_THE_SECRET_"  # Asegúrate de que la clave tenga la longitud adecuada (16, 24 o 32 bytes para AES)
iv = "_NOT_THE_SECRET_"    # El IV también debe tener 16 bytes para AES

try:
    decrypted_string = decrypt(hex_data, key, iv)
    print("Texto desencriptado:", decrypted_string)
except Exception as e:
    print("Error durante la desencriptación:", e)
