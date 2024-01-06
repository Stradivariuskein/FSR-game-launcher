import json
import os
import zipfile
import shutil


# cosntantes
MOD_PATH = os.path.abspath("./mods")

SOTORAGE_PATH = "store.json"

EXT_ICON_PATH = os.path.abspath('iconsext.exe')

ICONS_PATH = os.path.abspath("./icons")

# Obtiene el directorio actual del script en ejecución
WORK_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
print(WORK_DIRECTORY)

INSTALLED_MODS = 'installed_mods'

COOMONS_FILES = 'commons_files'

#globales
file_content = {'mods': []}

#############################################################################################################################
# agregar funcion para desactivar el overlay
# agregar funcion para crear mods
# common_files reemplazar por un unico archivo enable gpu 
# agregar ruta de juegos de stema y epic
#############################################################################################################################
# wrapper para guardar los cambios del archvo
def saved_file(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        global file_content  
        with open(SOTORAGE_PATH, 'w') as f:
            json.dump(file_content, f, indent=4)
        return result

    return wrapper


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
@saved_file
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
    

# valida si el archivo existe y contiene data
def read_storage():
    global file_content
    try:
        with open(SOTORAGE_PATH, 'r') as f:
            file_data = json.load(f)
            if file_data and file_data['mods'] != []:
                file_content = file_data

                return True
    except FileNotFoundError:
        detect_mods(MOD_PATH)
        return False
    except KeyError:
        detect_mods(MOD_PATH)
        return False
    except Exception as e:
        raise e


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
                command = f'copy "{common_file[mod_name]["path"]}" "{game_path}"'

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
        command = f'del "{os.path.join(mod_instaled["path"], to_delete)}"'

        os.system(command)
    with open(SOTORAGE_PATH, 'w') as f:
        
        del file_content[INSTALLED_MODS][id]
        json.dump(file_content, f, indent=4)

# extrae el icono del exe
def extract_icon(path) -> str:
    tmp_icon = os.path.join(ICONS_PATH, 'tmp')
    # aseguramos q no alla otros iconos en el directorio
    os.system(f'del /Q /S {tmp_icon}\\*')
    command = f'{EXT_ICON_PATH} /save "{path}" "{tmp_icon}" -icons'
    os.system(command)
    icons = os.listdir(tmp_icon)
    if icons != []:
        # obtenemos el nombre del icono y su extencion
        name_ico, extension_ico = os.path.splitext(os.path.basename(f"{tmp_icon}\\{icons[0]}"))
        # obtenemos el nombre del juego(exe)
        name_exe, _ = os.path.splitext(os.path.basename(f"{path}"))
        
        icon_path =f"{ICONS_PATH}\\{name_exe}{extension_ico}"
        command = f'move "{tmp_icon}\\{name_ico}{extension_ico}" "{icon_path}"'
        os.system(command)
    else:
        tmp_icon = ''
        print("Error: No se puedo estraer el cicono")
    # eliminamos los archivos temporales
    os.system(f'del /Q /S {tmp_icon}\\*')
    return icon_path

# extrae el icono del juego y 
@saved_file
def get_icon(exe_path) -> int:
    icon_path = extract_icon(exe_path)
    icon = {'icon_path': icon_path}
    if 'icons' in file_content:
        file_content['icons'].append(icon)
        icon_index = len(file_content['icons']) - 1
    else:
        file_content['icons'] = [icon]
        icon_index = 0
    return icon_index

@saved_file
def add_game(path, game_name=None):
    global file_content 
    
    if game_name is None:
        game_name, _ = os.path.splitext(os.path.basename(path))
    
    iconID = get_icon(path)
    game = {
        'name': game_name,
        'path': path,
        'iconID': iconID,
        'modID': None
        }
    
    if 'games' in file_content:
        file_content['games'].append(game)
    else:
        file_content['games'] = [game]
    return game




if __name__ == "__main__":


    path = 'J:\\Descargas\\Forever Skies-InsaneRamZes\\ForeverSkies.exe'
    read_storage()
    add_game(path)
    detect_mods(MOD_PATH)
    
        
    install_mod('J:\\Documentos\\python\\FSR-game-launcher\\test_game', 'J:\\Documentos\\python\\FSR-game-launcher\\mods\\FSR2FSR3\\0.7.2\\FSR2FSR3_220', '0.7.2', 'FSR2FSR3')

    uninstall_mod(0)