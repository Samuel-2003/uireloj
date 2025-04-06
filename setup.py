import sys
from cx_Freeze import setup, Executable

# Dependencias
build_exe_options = {
    "packages": ["os", "tkinter", "json", "datetime", "time"],
    "includes": ["pytz"],
    "include_files": ["reloj.ico"],  # Incluye el icono en la distribución
    "excludes": []
}

# Configuración base
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Oculta la consola en Windows

# Configuración del ejecutable
setup(
    name="Reloj Peruano",
    version="1.0",
    description="Reloj con hora peruana flotante",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "RelojPeruano.py",  # Archivo principal
            base=base,
            target_name="RelojPeruano.exe",
            shortcut_name="Reloj Peruano",
            shortcut_dir="DesktopFolder",
            icon="reloj.ico"  # Usa el icono para el ejecutable
        )
    ]
)