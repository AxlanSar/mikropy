# Mikropy

Mikropy es una herramienta desarrollada en python para la realizar configuraciones intermedias y avanzadas en los Enrutadores Mikrotik. Proporciona una forma rápida de configurar equipos Mikrotik desde una interfaz más intuitiva que la consola de Mikrotik sin tener mucho, poco o nulo conocimiento técnico.

Desarrollada por: Axel E. Amavizca (AXLAN SAR)

## Características

- Configuración de failover recursivo
- Configuración de balanceo ECMP
- Configuración de reenvío/apertura de puertos
- Configuración de firewall
- Interfaz de línea de comandos fácil de usar sin necesidad de aprenderse comandos o usar Winbox.

## Requisitos

- Python 3.X
- Bibliotecas requeridas: `paramiko`, `pyfiglet`, `colorama`

## Uso

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/AxlanSar/mikropy.git
   cd mikropy
   ./requerimientos.py #Ejecutar una única vez.
   ./mikropy.py

2. **Conexión al mikrotik:**
   Para que la conexión entre Mikropy y el enrutador Mikrotik se dé correctamente es necesario tener activo el servicio "SSH" en el router.
   Inicia sesión en el router mikrotik, abre la terminal y escribe:
   /ip service set ssh port=22

## Contacto

Facebook: https://www.facebook.com/AXLANSAR2/
Email: axlansar@duck.com

## Imágenes

![mikropy](https://github.com/AxlanSar/mikropy/blob/main/mk1.png)
![mikropy](https://github.com/AxlanSar/mikropy/blob/main/mk2.png)
![mikropy](https://github.com/AxlanSar/mikropy/blob/main/mk3.png)
![mikropy](https://github.com/AxlanSar/mikropy/blob/main/mk4.png)
