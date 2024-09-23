from elftools.elf.elffile import ELFFile

def get_entry_point(binary_path):
    with open(binary_path, 'rb') as f:
        elf = ELFFile(f)
        entry_point = elf.header['e_entry']
        return entry_point

binary_path = './quick_1'  # Ruta a tu binario
entry = get_entry_point(binary_path)
print(f"Entry point: {hex(entry)}")
