import os
from collections import Counter

# Ruta de la carpeta
carpeta = r"C:\Users\Natalia\Desktop\pythons\GRADO_MEDIO"

# Verificar si la carpeta existe
if not os.path.exists(carpeta):
    print(f"La carpeta {carpeta} no existe.")
else:
    # Crear un contador para las extensiones
    contador_extensiones = Counter()

    # Recorrer todos los archivos en la carpeta
    for root, dirs, files in os.walk(carpeta):
        for file in files:
            # Obtener la extensión del archivo
            _, extension = os.path.splitext(file)
            # Incrementar el contador para esa extensión
            contador_extensiones[extension] += 1

    # Mostrar el resultado
    print("Cantidad de archivos por extensión:")
    for extension, count in contador_extensiones.items():
        print(f"{extension if extension else 'Sin extensión'}: {count}")
