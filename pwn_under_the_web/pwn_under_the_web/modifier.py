from PIL import Image, PngImagePlugin

# Ruta del archivo PNG
input_file = "starry_night.png"
output_file = "starry_night_mod.png"

# Cargar la imagen
image = Image.open(input_file)

# Crear metadatos personalizados
metadata = PngImagePlugin.PngInfo()
metadata.add_text("Title", "AAAAAAAAAAAAAAA")
metadata.add_text("Artist", "BBBBBBBBBBBBBB")
metadata.add_text("Copyright", "CCCCCCCCCCCCCCC")

# Guardar la imagen con los nuevos metadatos
image.save(output_file, "PNG", pnginfo=metadata)

print(f"Metadatos actualizados y guardados en {output_file}")





