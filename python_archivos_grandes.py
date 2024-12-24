import os
import shutil

def scan_directories(start_path, size_limit_mb, output_file):
    size_limit_bytes = size_limit_mb * 1024 * 1024  # Convertir MB a bytes
    output_dir = os.path.join(start_path, "archivos_grandes")
    os.makedirs(output_dir, exist_ok=True)  # Crear carpeta para archivos grandes

    with open(output_file, 'w', encoding='utf-8') as file_output:
        for root, dirs, files in os.walk(start_path):
            # Ignorar la carpeta 'archivos_grandes'
            if os.path.basename(root) == "archivos_grandes":
                continue

            # Revisar archivos
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    if os.path.getsize(filepath) > size_limit_bytes:
                        file_output.write(f"Archivo: {filepath}, Tamaño: {os.path.getsize(filepath) / (1024 * 1024):.2f} MB\n")
                        # Copiar archivo grande a la carpeta de salida
                        shutil.copy(filepath, output_dir)
                except Exception as e:
                    file_output.write(f"Error al procesar archivo: {filepath}, Error: {e}\n")

            # Revisar carpetas
            for dirname in dirs[:]:
                dirpath = os.path.join(root, dirname)
                if dirname == "archivos_grandes":
                    dirs.remove(dirname)  # Evitar que os.walk procese esta carpeta
                    continue
                try:
                    total_size = sum(os.path.getsize(os.path.join(dirpath, f)) for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f)))
                    if total_size > size_limit_bytes:
                        file_output.write(f"Carpeta: {dirpath}, Tamaño: {total_size / (1024 * 1024):.2f} MB\n")
                except Exception as e:
                    file_output.write(f"Error al procesar carpeta: {dirpath}, Error: {e}\n")

if __name__ == "__main__":
    start_path = input("Introduce la ruta del directorio a escanear: ")
    output_file = "archivos.txt"
    size_limit_mb = 100

    print(f"Escaneando directorios desde: {start_path}...")
    scan_directories(start_path, size_limit_mb, output_file)
    print(f"Escaneo completado. Resultados guardados en {output_file} y archivos grandes copiados en la carpeta 'archivos_grandes'")
