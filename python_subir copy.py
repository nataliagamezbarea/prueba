import os
import git

# Configuración
directorio = r"C:\Users\Natalia\Desktop\pythons\2º GRADO MEDIO"
repositorio = "https://github.com/nataliagamezbarea/Segundo_grado_medio.git"
rama = "Segundo_grado_medio"  # Cambié la rama a "Segundo_grado_medio"

# Función para inicializar el repositorio si no está inicializado
def inicializar_git(directorio):
    if not os.path.exists(os.path.join(directorio, ".git")):
        print("Inicializando el repositorio Git...")
        repo = git.Repo.init(directorio)
        origin = repo.create_remote('origin', repositorio)
        try:
            origin.fetch()
            if rama not in repo.heads:
                print(f"Creando la rama {rama}...")
                repo.git.checkout('-b', rama)
            else:
                print(f"Conmutando a la rama existente {rama}...")
                repo.git.checkout(rama)
            repo.git.reset('--hard', f'origin/{rama}')
        except git.exc.GitCommandError as e:
            print(f"No se pudo sincronizar con el repositorio remoto: {e}")
    else:
        repo = git.Repo(directorio)
        if rama not in repo.heads:
            print(f"Creando la rama {rama}...")
            repo.git.checkout('-b', rama)
        else:
            print(f"Conmutando a la rama existente {rama}...")
            repo.git.checkout(rama)
    return repo

# Función para calcular el tamaño de un archivo
def obtener_tamano_archivo(archivo):
    return os.path.getsize(archivo)

# Función para obtener todas las extensiones del directorio (excepto .git)
def obtener_extensiones(directorio):
    extensiones = set()
    for root, dirs, files in os.walk(directorio):
        # Ignorar el directorio .git
        if '.git' in dirs:
            dirs.remove('.git')  # No recorrer el directorio .git
        for file in files:
            _, extension = os.path.splitext(file)
            extension = extension.lower()
            if extension:  # Evita agregar extensiones vacías
                extensiones.add(extension)
    return extensiones

# Función para subir archivos por lotes con un tamaño máximo total
def agregar_y_subir_archivos(extension, directorio, repo, tamano_maximo_gb=2):
    archivos_a_subir = []
    tamano_actual = 0
    lote_actual = []
    tamano_maximo_bytes = tamano_maximo_gb * 1024 * 1024 * 1024

    for root, dirs, files in os.walk(directorio):
        # Ignorar el directorio .git
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file.lower().endswith(extension.lower()):
                archivo = os.path.join(root, file)
                archivo_tamano = obtener_tamano_archivo(archivo)

                # Si el archivo cabe en el lote actual, se agrega
                if tamano_actual + archivo_tamano <= tamano_maximo_bytes:
                    lote_actual.append(archivo)
                    tamano_actual += archivo_tamano
                else:
                    # Intentar subir el lote actual
                    if lote_actual:
                        if subir_lote(repo, lote_actual, extension):
                            archivos_a_subir.extend(lote_actual)
                        lote_actual = [archivo]
                        tamano_actual = archivo_tamano

    # Subir el último lote si queda algo pendiente
    if lote_actual:
        if subir_lote(repo, lote_actual, extension):
            archivos_a_subir.extend(lote_actual)

    if archivos_a_subir:
        print(f"Se subieron correctamente {len(archivos_a_subir)} archivos {extension}.")
    else:
        print(f"No se encontraron archivos {extension} para subir en el directorio o subdirectorios.")

# Función para subir un lote de archivos
def subir_lote(repo, lote, extension):
    try:
        print(f"Subiendo lote de {len(lote)} archivos {extension}...")
        for archivo in lote:
            repo.git.add(archivo)
        repo.git.commit(m=f"Subiendo lote de {len(lote)} archivos {extension}")
        repo.git.push("--set-upstream", "origin", rama)
        print(f"Lote de {len(lote)} archivos {extension} subido correctamente.")
        return True
    except git.exc.GitCommandError as e:
        print(f"Error al subir el lote: {e}")
        print("Intentando subir archivos individualmente...")
        for archivo in lote:
            try:
                repo.git.add(archivo)
                repo.git.commit(m=f"Subiendo archivo {os.path.basename(archivo)}")
                repo.git.push("--set-upstream", "origin", rama)
                print(f"Archivo {os.path.basename(archivo)} subido correctamente.")
            except git.exc.GitCommandError as e_individual:
                print(f"Error al subir el archivo {os.path.basename(archivo)}: {e_individual}")
        return False

# Punto de entrada principal
if __name__ == "__main__":
    # Inicializar repositorio Git
    repo = inicializar_git(directorio)

    # Obtener todas las extensiones de los archivos en el directorio
    extensiones = obtener_extensiones(directorio)

    # Subir archivos de cada extensión encontrada
    for extension in extensiones:
        agregar_y_subir_archivos(extension, directorio, repo, tamano_maximo_gb=2)
