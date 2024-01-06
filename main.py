import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import backend



def msj_error(mensaje):
    messagebox.showerror("Error", mensaje)

def fill_table():
    tabla.delete(*tabla.get_children())
    try:
        games_list = backend.file_content['games']
    except KeyError:
        return
    icons_paths = backend.file_content['icons']

    # Validaciones de parámetros
    if not isinstance(games_list, list):
        raise ValueError("Se esperaba una lista")

    # Llenar la tabla con los registros    
    for game in games_list:
        icon_path = icons_paths[game['iconID']]['icon_path']

        # Cargar y escalar la imagen

        icon = Image.open(icon_path)
        icon = icon.resize((30, 30), Image.Resampling.LANCZOS)
        icon = ImageTk.PhotoImage(icon)
        try:
            icon_list.append(icon)
        except FileNotFoundError:
            pass
       
        tabla.insert("", "end", tags=("higth-30"), image=icon_list[-1], values=(game['name'], game["modID"]))

def add_game():
    game_path = filedialog.askopenfilename(filetypes=[("Archivos ejecutables", "*.exe")])
    if game_path:
        if os.path.isfile(game_path):
            backend.add_game(game_path)
        else:
            msj_error("Archivo invalido, seleccione el ejecutable princiapl del juego (ej: juego.exe)")
        print(game_path)

def agregar_mods():
    # Lógica para agregar mods
    pass

def jugar():
    # Lógica para iniciar el juego
    pass
backend.read_storage()
# Crear la ventana principal
ventana = tk.Tk()
ventana.title("FSR Game Launcher")
global icon_list
icon_list = []


# Cuadro de texto para buscar
cuadro_buscar = tk.Entry(ventana)
cuadro_buscar.grid(row=0, column=0, padx=10, pady=10, sticky="ew")  # Añadir columnspan


button_refresh_table = tk.Button(ventana, text="Actualizar", command=fill_table)
button_refresh_table.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
# Boton para instalar mod
button_install_mod = tk.Button(ventana, text="Instalar mod", command=add_game)
# Boton para desinstalar mod
button_uninstall_mod = tk.Button(ventana, text="Desisntalar mod", command=add_game)
# Botón para agregar juego
button_add_game = tk.Button(ventana, text="Agregar Juego", command=add_game)
# Botón para agregar mods
button_add_mods = tk.Button(ventana, text="Agregar Mods", command=agregar_mods)
# Botón para jugar
button_play = tk.Button(ventana, text="Jugar", command=jugar)


list_buttons = [button_add_game, button_install_mod, button_add_mods, button_uninstall_mod, button_play]
caunt_buttons = len(list_buttons)
# agregamos los botones y configuramos las filas
for i in range(0, caunt_buttons):
    ventana.rowconfigure(i+1, weight=1)
    list_buttons[i].grid(row=i+1, column=1, pady=10, padx=10, sticky="new", rowspan=caunt_buttons)

# Tabla con 2 columnas
columnas = ("Nombre", "MOD")
# Add the rowheight
s=ttk.Style()
s.configure('Treeview', rowheight=40)


tabla = ttk.Treeview(ventana, columns=columnas)
tabla.column("# 0", width=50, minwidth=50)
tabla.column("# 1",anchor=tk.CENTER)
tabla.column("# 2",anchor=tk.CENTER)
for col in columnas:
    tabla.heading(col, text=col)
tabla.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", rowspan=caunt_buttons)  




# Configurar el layout de la ventana
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=1)



# Iniciar el bucle principal
ventana.mainloop()
