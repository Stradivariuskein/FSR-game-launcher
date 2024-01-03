import json
import os
import zipfile
import shutil


# cosntantes
MOD_PATH = os.path.abspath("./mods")

SOTORAGE_PATH = "store.json"

INSTALLED_MODS = 'installed_mods'

COOMONS_FILES = 'commons_files'

#globales
file_content = {'mods': []}


# descomprime los archivos de una carpeta de forma recursiva
def uncompres_files(path):
    # Obtener la lista de archivos y carpetas en el directorio actual
    content = os.listdir(path)
    

    for element in content:
        element_path = os.path.join(path, element)

        # Verificar si es un archivo ZIP
        if element.endswith('.zip') and os.path.isfile(element_path):
            # Descomprimir el archivo ZIP
            with zipfile.ZipFile(element_path, 'r') as zip_ref:
                folder_name = element.split('.')[0]
                uncompres_path = os.path.join(path, folder_name)
                zip_ref.extractall(uncompres_path)

            # Eliminar el archivo ZIP después de descomprimirlo (opcional)
            os.remove(element_path)
        
        # Si es un directorio, llamar a la función de manera recursiva
        elif os.path.isdir(element_path):
            uncompres_files(element_path)


    ######################################
    # falta descomprimir los archivo 7z  #
    ######################################

# obtiene los datos nesearios de los mods apartir del path
def get_data_to_path(path):
    # obtenemos fsr_version/mod_version/mod_name
    if path.endswith('.toml'):
        truncated_path = os.path.dirname(path).split('mods')[1]
    else:
        truncated_path = path.split('mods')[1]
    data_mod = truncated_path.split('\\')[1:]
    mod_name = data_mod[0]
    mod_version = data_mod[1]
    if len(data_mod) > 3:
        fsr_version = data_mod[2]
    elif len(data_mod) == 3:
        fsr_version = "DLSS"
    if path.endswith('.toml'):
        data = {                
            mod_name:{
            'mod_version': mod_version,
            'path': path
            }                
        }

    else:
        data = {                
        mod_name:{
        'mod_version': mod_version,
        'fsr_version': fsr_version,
        'path': os.path.dirname(path)
        }                
    }
    return data

# detecta los mods presentes en la carpeta mdos
def detect_mods(path: str):
    # la variable global es para no pisar el contenido en cada iteracion recursiva
    global file_content
    # Obtener la lista de archivos y carpetas en el directorio actual
    content = os.listdir(path)
        
    for element in content:
        element_path = os.path.join(path, element)
        if element.endswith('.asi') and os.path.isfile(element_path):
            data = get_data_to_path(element_path)

            file_content['mods'].append(data)


        elif element.endswith('.toml') and os.path.isfile(element_path):
            data = get_data_to_path(element_path)
            if not COOMONS_FILES in file_content:
                file_content[COOMONS_FILES] = [data]
            else:
                file_content[COOMONS_FILES].append(data)

            
        # Si es un directorio, llamar a la función de manera recursiva
        elif os.path.isdir(element_path):
            detect_mods(element_path)
    


# copia los archivos del mod en el directorio del juego y guarda en el archivo los cambios
def install_mod(game_path: str, mod_path: str, mod_version: str, mod_name: str):
    global file_content
    files_copied = []
    
    with open(SOTORAGE_PATH, 'r') as file:
        
        data = json.load(file)

        command = f'copy "{mod_path}\\*" "{game_path}"'

        os.system(command)
        files_copied += os.listdir(mod_path)


        for common_file in data[COOMONS_FILES]:
            if common_file[mod_name]['mod_version'] == mod_version:
                command = f'copy "{common_file[mod_name]['path']}" "{game_path}"'

                os.system(command)
                files_copied += [os.path.basename(common_file[mod_name]['path'])]

        data = {
            'path': game_path,
            'files': files_copied
        }
        if not INSTALLED_MODS in file_content:
            file_content[INSTALLED_MODS] = [data]
        else:
            file_content[INSTALLED_MODS].append(data)

    
    with open(SOTORAGE_PATH, 'w') as f:
        json.dump(file_content, f, indent=4)


# elimina los archivos del mod de la carpeta del juego
def uninstall_mod(id: int):
    global file_content
    mod_instaled = file_content[INSTALLED_MODS][id]

    for to_delete in mod_instaled['files']:
        command = f'del "{os.path.join(mod_instaled['path'], to_delete)}"'

        os.system(command)
    with open(SOTORAGE_PATH, 'w') as f:
        #del data[INSTALLED_MODS][id]
        
        del file_content[INSTALLED_MODS][id]
        json.dump(file_content, f, indent=4)



if __name__ == "__main__":
    detect_mods(MOD_PATH)
    with open(SOTORAGE_PATH, 'w') as f:
        json.dump(file_content, f, indent=4)
        
    install_mod('J:\\Documentos\\python\\gui-fsr3-launcher\\test_game', 'J:\\Documentos\\python\\gui-fsr3-launcher\\mods\\FSR2FSR3\\0.7.2\\FSR2FSR3_220', '0.7.2', 'FSR2FSR3')

    uninstall_mod(0)