import zipfile

# Nombre del archivo ZIP
zip_filename = 'spell.zip'

# Nombre del archivo de texto dentro del ZIP
txt_filename = 'spell.txt'

# Contenido del archivo de texto en bytes
txt_content = b'Contenido del archivo spell.txt en bytes'

# Crear el archivo ZIP y añadir el archivo de texto
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    # Escribir el archivo de texto en el ZIP
    zipf.writestr(txt_filename, txt_content)

print(f'Archivo {zip_filename} creado con éxito, contiene el archivo {txt_filename}')

