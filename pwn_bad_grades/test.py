import struct

def f(x):
	# Convertir a bytes
	address_bytes = struct.pack('<Q', x)

	# Convertir los bytes a un valor double
	decimal_double = struct.unpack('d', address_bytes)[0]

	return decimal_double

# Dirección en hexadecimal
hex_address = 0x0000000000401263
print(f(hex_address))


