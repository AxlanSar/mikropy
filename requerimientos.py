import subprocess
import sys

# Lista de paquetes a instalar
packages = ["paramiko", "pyfiglet", "colorama"]

def install(package):
    """Instala un paquete utilizando pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    """Verifica si los paquetes están instalados y los instala si no lo están."""
    for package in packages:
        try:
            __import__(package)  # Intenta importar el paquete
            print(f"{package} ya está instalado.")
        except ImportError:
            print(f"Instalando {package}...")
            install(package)

if __name__ == "__main__":
    main()
