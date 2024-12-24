import os
import zipfile
import rarfile
import subprocess
import imageio_ffmpeg as ffmpeg

# Función para descomprimir un archivo ZIP
def descomprimir_zip(archivo_zip, carpeta_destino):
    with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
        zip_ref.extractall(carpeta_destino)
    print(f"Archivo ZIP descomprimido en {carpeta_destino}")

# Función para descomprimir un archivo RAR
def descomprimir_rar(archivo_rar, carpeta_destino):
    with rarfile.RarFile(archivo_rar) as rar_ref:
        rar_ref.extractall(carpeta_destino)
    print(f"Archivo RAR descomprimido en {carpeta_destino}")

# Función para dividir un archivo MP4 en partes de aproximadamente 100 MB
def dividir_video(archivo_mp4, carpeta_guardada):
    tamano_bytes = os.path.getsize(archivo_mp4)
    tamano_mb = tamano_bytes / (1024 * 1024)  # Tamaño en MB
    
    if tamano_mb > 100:  # Solo dividir si el archivo es mayor que 100 MB
        print(f"El archivo {archivo_mp4} tiene un tamaño de {tamano_mb:.2f} MB, será dividido.")

        # Crear la carpeta videos_guardados si no existe
        if not os.path.exists(carpeta_guardada):
            os.makedirs(carpeta_guardada)

        # Nombre base del archivo
        archivo_basename = os.path.basename(archivo_mp4).replace(".mp4", "")
        
        # Calcular cuántas partes se necesitan (tamaño en bytes)
        partes = tamano_bytes // 104857600  # 100 MB en bytes
        if tamano_bytes % 104857600 != 0:
            partes += 1  # Si hay residuo, agrega una parte extra

        archivos_divididos = []
        for i in range(partes):
            # Generar el nombre para cada parte
            archivo_parte = os.path.join(carpeta_guardada, f"{archivo_basename}_parte{i + 1}.mp4")

            # Dividir el archivo en partes de 100 MB utilizando FFmpeg
            ffmpeg_path = ffmpeg.get_ffmpeg_exe()
            start_time = i * 100  # Empezar a partir de 100 MB por cada parte
            command = [
                ffmpeg_path, '-i', archivo_mp4, '-ss', str(start_time), 
                '-fs', str(104857600), '-c', 'copy', archivo_parte
            ]
            
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            archivos_divididos.append(archivo_parte)

        print(f"El archivo ha sido dividido en las siguientes partes: {', '.join(archivos_divididos)}")
        
        # Eliminar el archivo original después de dividirlo
        os.remove(archivo_mp4)
        print(f"Archivo original {archivo_mp4} eliminado.")
        
        return archivos_divididos
    else:
        print(f"El archivo {archivo_mp4} no supera los 100 MB, no es necesario dividirlo.")
        return [archivo_mp4]

# Función para comprimir todos los archivos en un directorio
def comprimir_a_zip(carpeta_destino):
    archivos_comprimidos = []

    # Crear una lista de todos los archivos a comprimir
    for raiz, dirs, archivos in os.walk(carpeta_destino):
        for archivo in archivos:
            archivos_comprimidos.append(os.path.join(raiz, archivo))

    # Crear el primer archivo ZIP
    archivo_zip = os.path.join(carpeta_destino, "archivos_comprimidos.zip")
    dividir_zip(archivos_comprimidos, archivo_zip)

# Función para dividir el archivo ZIP si es mayor a 98 MB
def dividir_zip(archivos, archivo_zip):
    total_size = sum(os.path.getsize(archivo) for archivo in archivos)
    MAX_TAMANO_ZIP_MB = 98  # Máximo tamaño de archivo ZIP en MB
    if total_size / (1024 * 1024) <= MAX_TAMANO_ZIP_MB:
        # Si el tamaño total es menor a 98 MB, simplemente lo comprimimos en un solo ZIP
        with zipfile.ZipFile(archivo_zip, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
            for archivo in archivos:
                zipf.write(archivo, os.path.relpath(archivo, os.path.dirname(archivo_zip)))
        print(f"Archivo comprimido: {archivo_zip}, tamaño: {total_size / (1024 * 1024):.2f} MB")
    else:
        # Si el tamaño total es mayor a 98 MB, lo dividimos en múltiples archivos ZIP
        part_number = 1
        current_zip_name = archivo_zip.replace(".zip", f"_parte{part_number}.zip")
        current_zip = zipfile.ZipFile(current_zip_name, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)

        current_size = 0
        for archivo in archivos:
            file_size = os.path.getsize(archivo)
            if current_size + file_size > MAX_TAMANO_ZIP_MB * 1024 * 1024:
                # Si agregar el siguiente archivo excede el límite, cerramos el archivo ZIP actual y abrimos uno nuevo
                current_zip.close()
                part_number += 1
                current_zip_name = archivo_zip.replace(".zip", f"_parte{part_number}.zip")
                current_zip = zipfile.ZipFile(current_zip_name, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
                current_size = 0  # Resetamos el tamaño acumulado

            current_zip.write(archivo, os.path.relpath(archivo, os.path.dirname(archivo_zip)))
            current_size += file_size

        current_zip.close()  # Cerramos el último archivo ZIP
        print(f"Archivo comprimido en múltiples partes: {part_number} archivos ZIP generados.")

# Función principal que maneja la descompresión y búsqueda de archivos MP4
def procesar_archivo(archivo, carpeta_destino, carpeta_guardada):
    if archivo.endswith('.zip'):
        descomprimir_zip(archivo, carpeta_destino)
    elif archivo.endswith('.rar'):
        descomprimir_rar(archivo, carpeta_destino)
    else:
        print("El archivo no es ni ZIP ni RAR.")
        return

    archivos_extraidos = []
    for raiz, dirs, archivos in os.walk(carpeta_destino):
        for archivo in archivos:
            archivo_completo = os.path.join(raiz, archivo)
            if archivo.endswith('.mp4'):
                archivos_extraidos.extend(dividir_video(archivo_completo, carpeta_guardada))
            else:
                archivos_extraidos.append(archivo_completo)

    comprimir_a_zip(carpeta_destino)

# Ejemplo de uso con las rutas de los directorios
archivo_comprimido = r"C:\Users\Natalia\Downloads\ARCHIVOS PARA DIVIDIR\video\15. Tea Station_part1.zip"  # O puede ser .rar
carpeta_destino = r"C:\Users\Natalia\Downloads\ARCHIVOS PARA DIVIDIR\video1"  # Cambia esta ruta a donde quieras
carpeta_guardada = r"C:\Users\Natalia\Downloads\ARCHIVOS PARA DIVIDIR\video1\videos_guardados"  # Ruta donde se guardarán los videos divididos
procesar_archivo(archivo_comprimido, carpeta_destino, carpeta_guardada)
