import os
import zipfile
from datetime import datetime

def crear_respaldo_quirurgico():
    # Identificación de rutas (Dinámico y adaptable)
    dir_actual = os.getcwd()
    nombre_proyecto = os.path.basename(dir_actual)
    
    # El respaldo se guarda un nivel más arriba (C:\Felipe\Pae\) para no empaquetarse a sí mismo
    dir_padre = os.path.dirname(dir_actual)
    
    # Generación de Timestamp (Sello de tiempo)
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo_zip = f"Respaldo_{nombre_proyecto}_{fecha_hora}.zip"
    ruta_completa_zip = os.path.join(dir_padre, nombre_archivo_zip)
    
    # Lista negra de carpetas destructivas o pesadas
    carpetas_ignoradas = {'.venv', '__pycache__', '.git', '.vscode'}
    
    print(f"[INICIO] Iniciando Protocolo de Respaldo para: {nombre_proyecto}")
    print(f"[INFO]   Filtrando dependencias pesadas...")

    # Creación del archivo ZIP
    with zipfile.ZipFile(ruta_completa_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for raiz, directorios, archivos in os.walk(dir_actual):
            
            # Intervención en la lista de directorios para saltar las carpetas ignoradas
            directorios[:] = [d for d in directorios if d not in carpetas_ignoradas]
            
            for archivo in archivos:
                # Evitar respaldar archivos basura temporales
                if archivo.endswith('.pyc') or archivo.endswith('.log'):
                    continue
                    
                ruta_absoluta = os.path.join(raiz, archivo)
                # Crear ruta relativa para que el ZIP mantenga la estructura limpia
                ruta_relativa = os.path.relpath(ruta_absoluta, dir_actual)
                
                zipf.write(ruta_absoluta, ruta_relativa)
                
    print(f"[OK]     Respaldo exitoso y limpio!")
    print(f"[RUTA]   Archivo guardado en: {ruta_completa_zip}")

if __name__ == "__main__":
    crear_respaldo_quirurgico()