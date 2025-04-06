import tkinter as tk
from tkinter import font as tkfont
import datetime
import time
import os
import json
import traceback

try:
    import pytz
    TIENE_PYTZ = True
except ImportError:
    TIENE_PYTZ = False
    print("Advertencia: pytz no está instalado. Se usará la hora local en lugar de la hora peruana.")
    print("Para instalar pytz, ejecuta: pip install pytz")

class RelojPeruano:
    def __init__(self, root):
        # Configuración de la ventana principal
        self.root = root
        self.root.title("Reloj Peruano")
        
        # Quitar bordes de la ventana
        self.root.overrideredirect(True)
        
        # Hacer fondo transparente
        self.root.configure(bg="black")
        self.root.attributes("-transparentcolor", "black")
        
        # No estar siempre encima por defecto
        self.root.attributes("-topmost", False)
        
        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Centrar en pantalla por defecto
        x = (screen_width - 300) // 2
        y = (screen_height - 150) // 2
        
        # Configuración predeterminada
        self.config = {
            "tamano_hora": 72,
            "tamano_fecha": 24,
            "formato_24h": True,
            "mostrar_segundos": True,
            "color_texto": "#FFFFFF",
            "posicion_x": x,
            "posicion_y": y
        }
        
        # Intentar cargar configuración
        try:
            self.cargar_configuracion()
        except Exception as e:
            print(f"Error al cargar configuración: {e}")
        
        # Aplicar posición inicial
        self.root.geometry(f"+{self.config['posicion_x']}+{self.config['posicion_y']}")
        
        # Frame principal transparente
        self.frame_principal = tk.Frame(self.root, bg="black")
        self.frame_principal.pack(padx=0, pady=0)
        
        # Fuentes
        self.fuente_hora = tkfont.Font(family="Helvetica", size=self.config["tamano_hora"], weight="bold")
        self.fuente_fecha = tkfont.Font(family="Helvetica", size=self.config["tamano_fecha"])
        
        # Etiqueta de hora
        self.etiqueta_hora = tk.Label(
            self.frame_principal, 
            font=self.fuente_hora, 
            bg="black",
            fg=self.config["color_texto"],
            text="00:00"
        )
        self.etiqueta_hora.pack(pady=(0, 0))
        
        # Etiqueta de fecha
        self.etiqueta_fecha = tk.Label(
            self.frame_principal, 
            font=self.fuente_fecha, 
            bg="black",
            fg=self.config["color_texto"],
            text="Cargando..."
        )
        self.etiqueta_fecha.pack(pady=(0, 0))
        
        # Eventos para doble clic - Solo en la etiqueta de hora
        self.etiqueta_hora.bind('<Double-Button-1>', self.mostrar_configuracion)
        
        # Eventos para arrastrar desde cualquier parte del reloj
        self.dragging = False
        
        # Aplicar eventos a todos los elementos
        for widget in [self.frame_principal, self.etiqueta_hora, self.etiqueta_fecha]:
            widget.bind('<Button-1>', self.iniciar_arrastre)
            widget.bind('<ButtonRelease-1>', self.detener_arrastre)
            widget.bind('<B1-Motion>', self.arrastrar)
        
        # Iniciar actualización
        self.actualizar_hora()
    
    def iniciar_arrastre(self, event):
        self.rel_x = event.x
        self.rel_y = event.y
        self.dragging = True
    
    def detener_arrastre(self, event):
        self.dragging = False
        self.config["posicion_x"] = self.root.winfo_x()
        self.config["posicion_y"] = self.root.winfo_y()
        self.guardar_configuracion()
    
    def arrastrar(self, event):
        if self.dragging:
            x = self.root.winfo_x() + event.x - self.rel_x
            y = self.root.winfo_y() + event.y - self.rel_y
            self.root.geometry(f"+{x}+{y}")
    
    def obtener_hora_actual(self):
        if TIENE_PYTZ:
            # Usar hora de Perú
            zona_horaria = pytz.timezone('America/Lima')
            return datetime.datetime.now(zona_horaria)
        else:
            # Usar hora local si no está pytz
            return datetime.datetime.now()
    
    def actualizar_hora(self):
        try:
            # Obtener hora
            ahora = self.obtener_hora_actual()
            
            # Formatear hora
            formato_hora = "%H:%M" if self.config["formato_24h"] else "%I:%M %p"
            if self.config["mostrar_segundos"]:
                formato_hora += ":%S"
            
            tiempo = ahora.strftime(formato_hora)
            fecha = ahora.strftime("%A, %d de %B de %Y")
            
            # Traducir al español
            meses = {
                "January": "enero", "February": "febrero", "March": "marzo", "April": "abril",
                "May": "mayo", "June": "junio", "July": "julio", "August": "agosto",
                "September": "septiembre", "October": "octubre", "November": "noviembre", "December": "diciembre"
            }
            dias = {
                "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves",
                "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
            }
            
            for ingles, espanol in meses.items():
                fecha = fecha.replace(ingles, espanol)
            for ingles, espanol in dias.items():
                fecha = fecha.replace(ingles, espanol)
            
            # Actualizar etiquetas
            self.etiqueta_hora.config(text=tiempo)
            self.etiqueta_fecha.config(text=fecha)
            
            # Programar próxima actualización
            self.root.after(1000, self.actualizar_hora)
        except Exception as e:
            print(f"Error al actualizar la hora: {e}")
            self.root.after(5000, self.actualizar_hora)
    
    def mostrar_configuracion(self, event=None):
        try:
            # Crear ventana de configuración
            ventana_config = tk.Toplevel(self.root)
            ventana_config.title("Configuración del Reloj")
            ventana_config.geometry("350x350")
            ventana_config.resizable(False, False)
            ventana_config.attributes('-topmost', True)
            
            # Frame de configuración
            frame_config = tk.Frame(ventana_config, padx=20, pady=20)
            frame_config.pack(fill=tk.BOTH, expand=True)
            
            # Tamaño hora
            tk.Label(frame_config, text="Tamaño de hora:").grid(row=0, column=0, sticky=tk.W, pady=5)
            tamano_hora_var = tk.IntVar(value=self.config["tamano_hora"])
            tamano_hora_slider = tk.Scale(
                frame_config, from_=24, to=120, orient=tk.HORIZONTAL, 
                variable=tamano_hora_var, length=150
            )
            tamano_hora_slider.grid(row=0, column=1, pady=5)
            
            # Tamaño fecha
            tk.Label(frame_config, text="Tamaño de fecha:").grid(row=1, column=0, sticky=tk.W, pady=5)
            tamano_fecha_var = tk.IntVar(value=self.config["tamano_fecha"])
            tamano_fecha_slider = tk.Scale(
                frame_config, from_=12, to=48, orient=tk.HORIZONTAL, 
                variable=tamano_fecha_var, length=150
            )
            tamano_fecha_slider.grid(row=1, column=1, pady=5)
            
            # Formato 24h
            formato_24h_var = tk.BooleanVar(value=self.config["formato_24h"])
            formato_24h_check = tk.Checkbutton(
                frame_config, text="Formato 24 horas", variable=formato_24h_var
            )
            formato_24h_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
            
            # Mostrar segundos
            mostrar_segundos_var = tk.BooleanVar(value=self.config["mostrar_segundos"])
            mostrar_segundos_check = tk.Checkbutton(
                frame_config, text="Mostrar segundos", variable=mostrar_segundos_var
            )
            mostrar_segundos_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
            
            # Color texto
            tk.Label(frame_config, text="Color del texto:").grid(row=4, column=0, sticky=tk.W, pady=5)
            color_texto_var = tk.StringVar(value=self.config["color_texto"])
            color_texto_entry = tk.Entry(frame_config, textvariable=color_texto_var, width=10)
            color_texto_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
            
            # Siempre visible
            topmost_var = tk.BooleanVar(value=self.root.attributes('-topmost'))
            topmost_check = tk.Checkbutton(
                frame_config, text="Mostrar por encima de otras ventanas", 
                variable=topmost_var
            )
            topmost_check.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=5)
            
            # Ayuda
            tk.Label(
                frame_config, 
                text="• Doble clic en la hora para abrir configuración\n• Arrastrar para cambiar posición",
                justify=tk.LEFT,
                font=("Helvetica", 8)
            ).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
            
            # Botones
            frame_botones = tk.Frame(frame_config)
            frame_botones.grid(row=7, column=0, columnspan=2, pady=20)
            
            # Guardar
            guardar_button = tk.Button(
                frame_botones, text="Guardar", width=10,
                command=lambda: self.guardar_configuracion_ventana(
                    tamano_hora_var.get(), 
                    tamano_fecha_var.get(),
                    formato_24h_var.get(),
                    mostrar_segundos_var.get(),
                    color_texto_var.get(),
                    topmost_var.get(),
                    ventana_config
                )
            )
            guardar_button.pack(side=tk.LEFT, padx=10)
            
            # Salir
            salir_button = tk.Button(
                frame_botones, text="Salir", width=10,
                command=lambda: self.root.destroy()
            )
            salir_button.pack(side=tk.LEFT, padx=10)
            
        except Exception as e:
            print(f"Error al mostrar configuración: {e}")
    
    def guardar_configuracion_ventana(self, tamano_hora, tamano_fecha, formato_24h, 
                               mostrar_segundos, color_texto, topmost, ventana_config):
        try:
            # Verificar color de texto
            if not color_texto or color_texto.strip() == "":
                color_texto = "#FFFFFF"
            
            # Actualizar configuración
            self.config["tamano_hora"] = tamano_hora
            self.config["tamano_fecha"] = tamano_fecha
            self.config["formato_24h"] = formato_24h
            self.config["mostrar_segundos"] = mostrar_segundos
            self.config["color_texto"] = color_texto
            
            # Guardar en archivo
            self.guardar_configuracion()
            
            # Actualizar interfaz
            self.fuente_hora.configure(size=tamano_hora)
            self.fuente_fecha.configure(size=tamano_fecha)
            self.etiqueta_hora.config(fg=color_texto)
            self.etiqueta_fecha.config(fg=color_texto)
            
            # Configurar si estará por encima
            self.root.attributes('-topmost', topmost)
            
            # Cerrar ventana
            ventana_config.destroy()
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
    
    def guardar_configuracion(self):
        try:
            # Guardar en archivo
            ruta_config = os.path.join(os.path.expanduser("~"), "reloj_peruano_config.json")
            with open(ruta_config, "w") as archivo:
                json.dump(self.config, archivo)
        except Exception as e:
            print(f"Error al guardar archivo de configuración: {e}")
    
    def cargar_configuracion(self):
        try:
            # Cargar desde archivo
            ruta_config = os.path.join(os.path.expanduser("~"), "reloj_peruano_config.json")
            if os.path.exists(ruta_config):
                with open(ruta_config, "r") as archivo:
                    configuracion_guardada = json.load(archivo)
                    
                    # Verificar color de texto
                    if "color_texto" in configuracion_guardada and (
                        not configuracion_guardada["color_texto"] or 
                        configuracion_guardada["color_texto"].strip() == ""
                    ):
                        configuracion_guardada["color_texto"] = "#FFFFFF"
                    
                    # Actualizar configuración
                    self.config.update(configuracion_guardada)
        except Exception as e:
            print(f"Error al cargar configuración: {e}")

def main():
    try:
        root = tk.Tk()
        app = RelojPeruano(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")

if __name__ == "__main__":
    main()
