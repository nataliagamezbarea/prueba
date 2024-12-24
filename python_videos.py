import os
import subprocess
import imageio_ffmpeg as ffmpeg

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

# Función principal para procesar los videos en un directorio
def procesar_videos_en_directorio(carpeta_destino, carpeta_guardada):
    archivos_divididos = []
    for raiz, dirs, archivos in os.walk(carpeta_destino):
        for archivo in archivos:
            archivo_completo = os.path.join(raiz, archivo)
            if archivo.endswith('.mp4'):
                archivos_divididos.extend(dividir_video(archivo_completo, carpeta_guardada))

    print("Procesamiento completo de los videos.")

# Ejemplo de uso con las rutas de los directorios
carpeta_destino = r"C:\Users\Natalia\Desktop\pythons\GRADO_MEDIO\archivos_grandes"  # Cambia esta ruta
carpeta_guardada = r"C:\Users\Natalia\Desktop\pythons\GRADO_MEDIO\archivos_grandes"  # Ruta donde se guardarán los videos divididos
procesar_videos_en_directorio(carpeta_destino, carpeta_guardada)
