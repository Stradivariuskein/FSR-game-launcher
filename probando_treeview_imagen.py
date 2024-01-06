import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
global icono
ventana = tk.Tk()
ventana.title("Ejemplo de Treeview con Imágenes")

# Crear un Treeview con dos columnas: 'Ícono' y 'Nombre'
columnas = ("Ícono", "Nombre")
tabla = ttk.Treeview(ventana, columns=columnas)

# Configurar encabezados de columna
for col in columnas:
    tabla.heading(col, text=col)

# Cargar el ícono usando Pillow
icono_path = "J:\\Documentos\\python\\FSR-game-launcher\\icons\\ForeverSkies.ico"    

icono = Image.open(icono_path)
icono = icono.resize((16, 16), Image.Resampling.LANCZOS)
proces_icono = ImageTk.PhotoImage(icono)


label = tk.Label(ventana)
label.config(image=proces_icono)
label.pack()
# Agregar íconos y nombres a la tabla
nombre = "Elemento 1"

# Insertar ítem con imagen
tabla.insert("", "end", values=("", nombre), image=proces_icono)

# Mostrar la tabla
tabla.pack()

ventana.mainloop()
