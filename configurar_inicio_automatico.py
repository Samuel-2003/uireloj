import os
import sys
import winreg
import tkinter as tk
from tkinter import messagebox

def configurar_inicio_automatico():
    """Configura el Reloj Peruano para que inicie automáticamente con Windows"""
    try:
        # Obtenemos la ruta del ejecutable
        if getattr(sys, 'frozen', False):
            # Si es la aplicación empaquetada
            ruta_ejecutable = sys.executable
        else:
            # Si es el script Python
            ruta_ejecutable = os.path.abspath(__file__)
            ruta_ejecutable = ruta_ejecutable.replace('configurar_inicio_automatico.py', 'RelojPeruano.py')
            # Usar pythonw.exe para ejecutar sin consola
            ruta_ejecutable = f'pythonw "{ruta_ejecutable}"'
        
        # Acceder al registro de Windows
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        
        # Configurar para inicio automático
        winreg.SetValueEx(key, "RelojPeruano", 0, winreg.REG_SZ, ruta_ejecutable)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Error al configurar inicio automático: {e}")
        return False

def eliminar_inicio_automatico():
    """Elimina el Reloj Peruano del inicio automático de Windows"""
    try:
        # Acceder al registro de Windows
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        
        # Eliminar entrada
        try:
            winreg.DeleteValue(key, "RelojPeruano")
        except FileNotFoundError:
            # No existe la entrada, no hay problema
            pass
        
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Error al eliminar inicio automático: {e}")
        return False

def verificar_inicio_automatico():
    """Verifica si el Reloj Peruano está configurado para iniciar automáticamente"""
    try:
        # Acceder al registro de Windows
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_READ
        )
        
        try:
            # Intentar leer la entrada
            winreg.QueryValueEx(key, "RelojPeruano")
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            # No existe la entrada
            winreg.CloseKey(key)
            return False
    except Exception as e:
        print(f"Error al verificar inicio automático: {e}")
        return False

if __name__ == "__main__":
    # Crear ventana
    ventana = tk.Tk()
    ventana.title("Configuración de Inicio Automático")
    ventana.geometry("400x150")
    ventana.resizable(False, False)
    
    # Frame principal
    frame = tk.Frame(ventana, padx=20, pady=20)
    frame.pack(expand=True, fill=tk.BOTH)
    
    # Verificar estado actual
    estado_actual = verificar_inicio_automatico()
    
    # Mensaje
    mensaje = "El Reloj Peruano está configurado para iniciar automáticamente con Windows." if estado_actual else "El Reloj Peruano NO está configurado para iniciar automáticamente con Windows."
    tk.Label(frame, text=mensaje, wraplength=350).pack(pady=10)
    
    # Botones
    frame_botones = tk.Frame(frame)
    frame_botones.pack(pady=10)
    
    def activar():
        exito = configurar_inicio_automatico()
        if exito:
            messagebox.showinfo("Éxito", "El Reloj Peruano iniciará automáticamente con Windows.")
        else:
            messagebox.showerror("Error", "No se pudo configurar el inicio automático.")
        ventana.destroy()
    
    def desactivar():
        exito = eliminar_inicio_automatico()
        if exito:
            messagebox.showinfo("Éxito", "El Reloj Peruano ya no iniciará automáticamente con Windows.")
        else:
            messagebox.showerror("Error", "No se pudo eliminar la configuración de inicio automático.")
        ventana.destroy()
    
    tk.Button(frame_botones, text="Activar inicio automático", width=20, command=activar).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botones, text="Desactivar inicio automático", width=20, command=desactivar).pack(side=tk.LEFT, padx=5)
    
    # Iniciar ventana
    ventana.mainloop()