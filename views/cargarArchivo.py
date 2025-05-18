import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from estructuras1.views.arbolView import VisualizadorArbol 


# Función para cargar archivos
def cargar_archivo():
    # Cierra la ventana de Pygame al abrir el cuadro de diálogo
    root = tk.Tk()
    puntos = []
    root.withdraw()  # Ocultar la ventana de tkinter
    #Abrir cuadro de dialogo para seleccionar archivo
    file_path = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json"), ("Archivos TXT", "*.txt")])
  
    if file_path:  # Si se selecciona un archivo
   
        with open(file_path, 'r', encoding="utf-8") as file:
            contenido = file.read()
        try:
            #Divide la ruta y accede a la extension
            extension = os.path.splitext(file_path)[1].lower()
            
            if extension == '.json':
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    puntos= data["puntos"]
            else:  # .txt 
                with open(file_path, 'r') as file:
                    contenido = file.read().strip()
                    puntos = eval(contenido)  # Evaluar como lista de tuplas
            if puntos:
                return puntos
        
            
            return True
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
            return False
