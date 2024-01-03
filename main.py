import tkinter as tk
from tkinter import ttk

def agregar_juego():
    # Lógica para agregar juego
    pass

def agregar_mods():
    # Lógica para agregar mods
    pass

def jugar():
    # Lógica para iniciar el juego
    pass

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("FSR Game Launcher")


# Cuadro de texto para buscar
cuadro_buscar = tk.Entry(ventana)
cuadro_buscar.grid(row=0, column=0, padx=10, pady=10, sticky="ew")  # Añadir columnspan



# Boton para instalar mod
button_install_mod = tk.Button(ventana, text="Instalar mod", command=agregar_juego)
# Boton para desinstalar mod
button_uninstall_mod = tk.Button(ventana, text="Desisntalar mod", command=agregar_juego)
# Botón para agregar juego
button_add_game = tk.Button(ventana, text="Agregar Juego", command=agregar_juego)
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

# Tabla con 4 columnas
columnas = ("Nombre", "Género", "Año", "Plataforma")
tabla = ttk.Treeview(ventana, columns=columnas, show="headings")
for col in columnas:
    tabla.heading(col, text=col)
tabla.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", rowspan=caunt_buttons)  




# Configurar el layout de la ventana
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=1)

# ventana.rowconfigure(1, weight=1)
# ventana.rowconfigure(2, weight=1)
# ventana.rowconfigure(3, weight=1)
# ventana.rowconfigure(4, weight=1)
# ventana.rowconfigure(5, weight=1)

# Iniciar el bucle principal
ventana.mainloop()
