def right_shift(input_file, output_file, shift_amount):
    # Abrir el archivo binario de entrada en modo lectura
    with open(input_file, 'rb') as infile:
        # Leer todos los datos
        data = infile.read()

    # Crear un bytearray para almacenar los nuevos bytes después del desplazamiento
    shifted_data = bytearray()

    # Iterar sobre los bytes y aplicar el desplazamiento a la derecha
    for byte in data:
        shifted_byte = byte << shift_amount  # Desplazar a la derecha el número de bits especificado
        shifted_data.append(shifted_byte)

    # Abrir el archivo binario de salida en modo escritura
    with open(output_file, 'wb') as outfile:
        # Escribir los datos desplazados
        outfile.write(shifted_data)

# Ejemplo de uso
right_shift('message.txt.cz', 'output.bin', 1)
