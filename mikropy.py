import paramiko
import pyfiglet
import getpass
from colorama import init, Fore, Style

# Inicializa colorama
init(autoreset=True)

def display_title():
    title = pyfiglet.figlet_format("MikroPy", font="slant")
    print(Fore.BLUE + title)
    print("--------------------------------------------------------------------------------")
    print("MikroPy v.10.2024: Configuraciones avanzadas automáticas para Routers Mikrotik")
    print("Elaborado por: Axel E. Amavizca - axlansar@duck.com - www.facebook.com/AXLANSAR2")
    print("Compatibilidad: RouterOS V7")
    print("--------------------------------------------------------------------------------")
    print("Para la correcta conexión con el Router Mikrotik, recuerda tener habilitado 'SSH'")
    print("")

def connect_to_mikrotik(host, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=username, password=password, allow_agent=False, look_for_keys=False)
        return client
    except Exception as e:
        print(Fore.RED + f"Error al conectar: {e}")
        return None

def ejecutar_comandos(client, commands):
    for command in commands:
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        if error:
            print(Fore.RED + f"Error: {error}")
            print(Fore.RED + "Configuración detenida debido a un error en el comando.")
            break  # Detiene la ejecución si ocurre un error
        elif output:
            print(Fore.GREEN + f"Salida: {output}")
        else:
            print(Fore.CYAN + "Comando ejecutado correctamente.")

def configurar_failoverc(client):
    while True:
        try:
            bridge_setup = input(Fore.GREEN + "¿Algunos de los puertos están agregados a una interfaz bridge? (s/n): " + Fore.WHITE).lower()
            bridge_name = input(Fore.GREEN + "Introduce el nombre de la interfaz bridge (ejemplo: bridge): " + Fore.WHITE) if bridge_setup == "s" else None

            port1 = input(Fore.GREEN + "Introduce el nombre del puerto WAN 1 (ejemplo: ether1, ether2): " + Fore.WHITE)
            ip_wan1 = input(Fore.GREEN + "Introduce la IP WAN 1 (ejemplo: 192.168.1.2/24): " + Fore.WHITE)
            gateway1 = input(Fore.GREEN + "Introduce el gateway WAN 1 (ejemplo: 192.168.1.254): "+ Fore.WHITE)
            port2 = input(Fore.GREEN + "Introduce el nombre del puerto WAN 2 (ejemplo: ether1, ether2): " + Fore.WHITE)
            ip_wan2 = input(Fore.GREEN + "Introduce la IP WAN 2 (ejemplo: 192.168.1.2/24): " + Fore.WHITE)
            gateway2 = input(Fore.GREEN + "Introduce el gateway WAN 2 (ejemplo: 192.168.1.254): " + Fore.WHITE)

            commands = [
                f'interface set [ find default-name={port1} ] comment="WAN 1 - Mikropy"',
                f'interface set [ find default-name={port2} ] comment="WAN 2 - Mikropy"',
                f'/ip address add comment="WAN 1 - Mikropy" address={ip_wan1} interface={port1}',
                f'/ip route add comment="Chequeo WAN 1 - Mikropy" disabled=no distance=1 dst-address=1.0.0.1/32 gateway={gateway1} routing-table=main scope=30 target-scope=10',
                f'/ip route add check-gateway=ping comment="WAN 1 - Mikropy" disabled=no distance=1 dst-address=0.0.0.0/0 gateway=1.0.0.1 routing-table=main scope=30 target-scope=30',
                f"/ip firewall nat add action=masquerade chain=srcnat comment=NAT-Mikropy out-interface={port1}",
                f"/ip dns set allow-remote-requests=yes cache-size=2048KiB servers=1.0.0.2,8.8.4.4",
                f'/ip address add comment="Wan 2 - Mikropy" address={ip_wan2} interface={port2}',
                f'/ip route add comment="Chequeo WAN 2 - Mikropy" disabled=no distance=1 dst-address=8.8.8.8/32 gateway={gateway2} routing-table=main scope=30 target-scope=10',
                f'/ip route add check-gateway=ping comment="WAN 2 - Mikropy" disabled=no distance=2 dst-address=0.0.0.0/0 gateway=8.8.8.8 routing-table=main scope=30 target-scope=30',
                f"/ip firewall nat add action=masquerade chain=srcnat comment=NAT-Mikropy out-interface={port2}"
            ]

            if bridge_name:
                commands.append(f"/interface bridge port remove [find interface={port1} bridge={bridge_name}]")
                commands.append(f"/interface bridge port remove [find interface={port2} bridge={bridge_name}]")
            
            ejecutar_comandos(client, commands)
            print(Fore.CYAN + "La configuración se ha realizado correctamente.")
            break

        except Exception as e:
            print(Fore.RED + f"Ocurrió un error al configurar: {e}")
            continue

def configurar_ecmp(client):
    while True:
        try:
            # Pregunta sobre la interfaz bridge
            bridge_setup = input(Fore.GREEN + "¿algunos de los puertos están agregados a una interfaz bridge? (s/n): " + Fore.WHITE).lower()
            bridge_name = None
            if bridge_setup == "s":
                bridge_name = input(Fore.GREEN + "Introduce el nombre de la interfaz bridge (ejemplo: bridge): " + Fore.WHITE)

            # Datos de configuración WAN
            port1 = input(Fore.GREEN + "Introduce el nombre del puerto WAN 1 (ejemplo: ether1, ether2): " + Fore.WHITE)
            ip_wan1 = input(Fore.GREEN + "Introduce la IP WAN 1 (ejemplo: 192.168.1.2/24): " + Fore.WHITE)
            gateway1 = input(Fore.GREEN + "Introduce el gateway WAN 1 (ejemplo: 192.168.1.254): " + Fore.WHITE)
            port2 = input(Fore.GREEN + "Introduce el nombre del puerto WAN 2 (ejemplo: ether1, ether2): " + Fore.WHITE)
            ip_wan2 = input(Fore.GREEN + "Introduce la IP WAN 2 (ejemplo: 192.168.1.2/24): " + Fore.WHITE)
            gateway2 = input(Fore.GREEN + "Introduce el gateway WAN 2 (ejemplo: 192.168.1.254): " + Fore.WHITE)

            # Comandos de configuración
            commands = [
                f'interface set [ find default-name={port1} ] comment="WAN 1 - Mikropy"',
                f'interface set [ find default-name={port2} ] comment="WAN 2 - Mikropy"',
                f'/ip address add comment="Wan 1 - Mikropy" address={ip_wan1} interface={port1}',
                f'/ip route add comment="Chequeo WAN 1 - Mikropy" disabled=no distance=1 dst-address=1.0.0.1/32 gateway={gateway1} routing-table=main scope=30 target-scope=10',
                f'/ip route add check-gateway=ping comment="WAN 1 - Mikropy" disabled=no distance=1 dst-address=0.0.0.0/0 gateway=1.0.0.1 routing-table=main scope=30 target-scope=30',
                f"/ip firewall nat add action=masquerade chain=srcnat comment=NAT-Mikropy out-interface={port1}",
                f"/ip dns set allow-remote-requests=yes cache-size=2048KiB servers=1.0.0.2,8.8.4.4",
                f'/ip address add comment="Wan 2 - Mikropy" address={ip_wan2} interface={port2}',
                f'/ip route add comment="Chequeo WAN 2 - Mikropy" disabled=no distance=1 dst-address=8.8.8.8/32 gateway={gateway2} routing-table=main scope=30 target-scope=10',
                f'/ip route add check-gateway=ping comment="WAN 2 - Mikropy" disabled=no distance=1 dst-address=0.0.0.0/0 gateway=8.8.8.8 routing-table=main scope=30 target-scope=30',
                f"/ip firewall nat add action=masquerade chain=srcnat comment=NAT-Mikropy out-interface={port2}"
            ]

            # Elimina los puertos WAN del bridge si es necesario
            if bridge_name:
                commands.append(f"/interface bridge port remove [find interface={port1} bridge={bridge_name}]")
                commands.append(f"/interface bridge port remove [find interface={port2} bridge={bridge_name}]")
            
            ejecutar_comandos(client, commands)
            print(Fore.CYAN + "La configuración se ha realizado correctamente.")
            break
        
        except Exception as e:
            print(Fore.RED + f"Ocurrió un error al configurar: {e}")
            continue

def configurar_reenvio(client):
    while True:
        try:
    
            # Datos de configuración WAN
            wanp = input(Fore.GREEN + "Introduce el nombre del puerto WAN (ejemplo: ether1, ether2): " + Fore.WHITE)
            port = input(Fore.GREEN + "Introduce el puerto (ejemplo: 443, 80): " + Fore.WHITE)
            protocol = input(Fore.GREEN + "Introduce el protocolo (ejemplo: tcp o udp): " + Fore.WHITE)
            ipdestino = input(Fore.GREEN + "Introduce la ip de destino (ejemplo: 192.168.1.56): " + Fore.WHITE)

            # Comandos de configuración
            commands = [
                f'ip firewall nat add action=dst-nat chain=dstnat comment="Reenvio - Mikropy" dst-port={port} in-interface={wanp} protocol={protocol} to-addresses={ipdestino} to-ports={port}'
            ]

            ejecutar_comandos(client, commands)
            print(Fore.CYAN + "La configuración se ha realizado correctamente.")

            break

        except Exception as e:
            print(Fore.RED + f"Ocurrió un error al configurar: {e}")
            continue   

def firewall(client):
    while True:
        try:
    
            print("Configurando firewall.....")

            # Comandos de configuración
            commands = [
                f'ip firewall filter add chain=input connection-state=established,related action=accept comment="Mikropy - aceptar los paquetes de conexiones establecidas y relacionadas" disabled=no',
                f'ip firewall filter add chain=input connection-state=invalid action=drop comment="Mikropy - descarta los paquetes invalido" disabled=no',
                f'ip firewall filter add action=add-src-to-address-list address-list="port:8000" address-list-timeout=1m chain=input dst-port=8000 protocol=tcp comment="Mikropy - Port Knocking"',
                f'ip firewall filter add action=add-src-to-address-list address-list="port:7000" comment="Mikropy - Port Knocking" address-list-timeout=1m chain=input dst-port=7000 protocol=tcp src-address-list="port:8000"',
                f'ip firewall filter add action=add-src-to-address-list address-list="secure-knocking-list" comment="Mikropy - Port Knocking" address-list-timeout=60m chain=input dst-port=9000 protocol=tcp src-address-list="port:7000"',
                f'ip firewall filter add chain=input dst-port=8291 protocol=tcp src-address-list=secure-knocking-list action=accept comment="Mikropy - Port Knocking"',
                f'ip firewall filter add action=drop chain=input src-address-list="Brute Force" comment="Mikropy - Bloqueo de fuerza bruta"',
                f'ip firewall filter add action=add-src-to-address-list address-list="Brute Force" comment="Mikropy - Bloqueo de fuerza bruta" address-list-timeout=10m chain=input connection-state=new limit=!1/1m,5:packet dst-port=8291,22 protocol=tcp',
                f'ip firewall filter add action=accept chain=input comment="Mikropy - Evitar Ping Flood" icmp-options=8:0 limit=1,5:packet protocol=icmp',
                f'ip firewall filter add action=accept comment="Mikropy - Evitar Ping Flood" chain=input icmp-options=0:0 protocol=icmp',
                f'ip firewall filter add action=drop comment="Mikropy - Evitar Ping Flood" chain=input protocol=icmp',
                f'ip firewall filter add action=drop chain=input comment="Mikropy - Bloquear escaneadores de puertos" src-address-list="port scanners"',
                f'ip firewall filter add action=add-src-to-address-list address-list="port scanners" address-list-timeout=4w2d chain=input comment="------Escaneadores de puertos Mikropy" protocol=tcp psd=10,3s,3,1',
                f'ip firewall filter add action=add-src-to-address-list address-list="port scanners" address-list-timeout=4w2d chain=input comment="------NMAP FIN Stealth scan Mikropy" protocol=tcp tcp-flags=fin,!syn,!rst,!psh,!ack,!urg',
                f'ip firewall filter add action=add-src-to-address-list address-list="port scanners" address-list-timeout=4w2d chain=input comment="------SYN/FIN scan Mikropy" protocol=tcp tcp-flags=fin,syn',
                f'ip firewall filter add action=add-src-to-address-list address-list="port scanners" address-list-timeout=4w2d chain=input comment="------SYN/RST scan Mikropy" protocol=tcp tcp-flags=syn,rst',
                f'ip firewall filter add action=add-src-to-address-list address-list="port scanners" address-list-timeout=4w2d chain=input comment="------FIN/PSH/URG scan Mikropy" protocol=tcp tcp-flags=fin,psh,urg,!syn,!rst,!ack',
                f'ip firewall filter add action=add-src-to-address-list address-list="port scanners" address-list-timeout=4w2d chain=input comment="------ALL/ALL scan Mikropy" protocol=tcp tcp-flags=fin,syn,rst,psh,ack,urg',
                f'ip firewall filter add action=add-src-to-address-list address-list="port scanners" address-list-timeout=4w2d chain=input comment="------NMAP NULL scan Mikropy" protocol=tcp tcp-flags=!fin,!syn,!rst,!psh,!ack,!urg',
                f'ip firewall filter add action=drop chain=input comment="Mikropy - Bloqueo Syn flood" src-address-list=Syn_Flooder',
                f'ip firewall filter add action=add-src-to-address-list comment="Mikropy - Bloqueo Syn flood" address-list=Syn_Flooder address-list-timeout=30m chain=input connection-limit=30,32 protocol=tcp tcp-flags=syn',
                f'ip firewall filter add action=tarpit chain=input comment="Mikropy - Bloqueo DOS attack" connection-limit=3,32 protocol=tcp src-address-list="DOS attack"',
                f'ip firewall filter add action=add-src-to-address-list comment="Mikropy - Bloqueo DOS attack" address-list="DOS attack" address-list-timeout=1d chain=input connection-limit=100,32 protocol=tcp'
            ]

            ejecutar_comandos(client, commands)
            print(Fore.CYAN + "La configuración se ha realizado correctamente.")
            break
        
        except Exception as e:
            print(Fore.RED + f"Ocurrió un error al configurar: {e}")
            continue

def borrar(client):
    while True:
        try:

            # Comandos de configuración
            commands = [
                f'/ip firewall filter remove [find comment~"Mikropy"]',
                f'/ip route remove [find comment~"Mikropy"]',
                f'/ip firewall nat remove [find comment~"Mikropy"]',
                f'/ip address remove [find comment~"Mikropy"]'
            ]

            ejecutar_comandos(client, commands)
            print(Fore.CYAN + "La configuración se ha realizado correctamente.")
            break

        except Exception as e:
            print(Fore.RED + f"Ocurrió un error al configurar: {e}")
            continue   


def main():
    while True:
        display_title()
        
        host = input(Fore.GREEN + "Introduce la IP del MikroTik: " + Fore.WHITE)
        username = input(Fore.GREEN + "Introduce el nombre de usuario: " + Fore.WHITE)
        password = getpass.getpass(Fore.GREEN + "Introduce la contraseña: " + Fore.WHITE)

        client = connect_to_mikrotik(host, username, password)
        if client is None:
            print(Fore.RED + "No se pudo conectar al MikroTik. Verifica los datos e intenta nuevamente.")
            input(Fore.WHITE + "Presiona Enter para intentar de nuevo...")
            continue

        while True:
            print(" ")
            print(" ")
            print(Fore.YELLOW + "Menú de opciones:" )
            print(Fore.YELLOW + "1. Configurar Failover recursivo (Disponible solamente para 2 WANs)")
            print(Fore.YELLOW + "2. Configurar Balanceo ECMP + Failover (Disponible solamente para 2 WANs)")
            print(Fore.YELLOW + "3. Configurar Reenvio de puertos")
            print(Fore.YELLOW + "4. Firewall protección básica ")
            print(Fore.YELLOW + "5. Borrar configuraciones Mikropy")
            print(Fore.YELLOW + "6. Salir")

            choice = input(Fore.YELLOW + "Selecciona una opción: " + Fore.WHITE)

            if choice == '1':
                configurar_failoverc(client)
            elif choice == '2':
                configurar_ecmp(client)
            elif choice == '3':
                configurar_reenvio(client)
            elif choice == '4':
                firewall(client)
            elif choice == '5':
                borrar(client)
            elif choice == '6':
                client.close()
                return
            else:
                print(Fore.RED + "Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()