def encrypt(data, param_2):
    # Convert the given 'data' to a bytearray if it's not already
    if isinstance(data, str):
        data = bytearray(data, 'utf-8')
    
    # Predefined values in byte form
    local_17 = bytearray(b'SUPERSECURE')
    #local_f = bytearray(b'RU')
    #local_d = bytearray(b'E')
    
    # Perform encryption
    for i in range(param_2):
        if i < len(data):
            data[i] = (data[i] + local_17[i % 11])
    
    return bytes(data)

# Example usage:
original_data = "HOLA"
param_2 = len(original_data)
encrypted_data = encrypt(original_data, param_2)
print(encrypted_data)

