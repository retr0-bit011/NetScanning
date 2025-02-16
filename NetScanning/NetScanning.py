import subprocess
import ipaddress
import socket
import shlex
import time
import sys
import platform
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_host(ip):
    """Realiza un ping a una dirección IP para verificar si está activa."""
    try:
        # Comando de ping según el sistema operativo
        if platform.system().lower() == "windows":
            command = ['ping', '-n', '1', '-w', '1000', str(ip)]
        else:
            command = ['ping', '-c', '1', '-W', '1', str(ip)]

        response = subprocess.run(
            command,
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        return ip if response.returncode == 0 else None
    except Exception as e:
        print(f"Error al hacer ping a {ip}: {e}", file=sys.stderr)
        return None

def ping_sweep(network):
    """Escanea una red para encontrar hosts activos."""
    print("\n[+] Iniciando Ping Sweep...")
    live_hosts = []
    try:
        # Validar la red ingresada
        network = ipaddress.IPv4Network(network, strict=False)
    except ValueError as e:
        print(f"[!] Error: La red ingresada no es válida. {e}", file=sys.stderr)
        return []

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(ping_host, str(ip)): ip for ip in network.hosts()}
        try:
            for future in as_completed(futures):
                result = future.result()
                if result:
                    print(f"[+] Host activo: {result}")
                    live_hosts.append(result)
        except KeyboardInterrupt:
            print("\n[!] Deteniendo escaneo...")
            sys.exit(0)
    return live_hosts

def scan_port(ip, port):
    """Escanea un puerto específico en una dirección IP."""
    try:
        with socket.create_connection((ip, port), timeout=1):
            return port
    except (socket.timeout, ConnectionRefusedError, socket.error) as e:
        return None

def port_scan(ip, ports_to_scan):
    """Escanea una lista de puertos en una dirección IP."""
    print(f"\n[+] Escaneando puertos en {ip}...")
    open_ports = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in ports_to_scan}
        try:
            for future in as_completed(futures):
                result = future.result()
                if result:
                    print(f"[+] Puerto abierto en {ip}: {result}")
                    open_ports.append(result)
        except KeyboardInterrupt:
            print("\n[!] Deteniendo escaneo...")
            sys.exit(0)
    return open_ports

def banner_grabbing(ip, port):
    """Intenta obtener el banner de un servicio en un puerto abierto."""
    try:
        with socket.create_connection((ip, port), timeout=3) as s:
            s.sendall(b"GET / HTTP/1.1\r\nHost: test\r\n\r\n")  # Envía una solicitud HTTP básica
            response = s.recv(1024).decode(errors="ignore").strip()
            
            # Busca el encabezado "Server" en la respuesta
            for line in response.split("\n"):
                if "Server:" in line:
                    return line.strip()  # Devuelve el banner del servidor
            
            return "No se pudo obtener el banner"
    except Exception as e:
        return f"Error al obtener el banner: {e}"

def save_report(report, filename="informe.txt"):
    """Guarda el informe en un archivo de texto."""
    try:
        # Verificar si el archivo ya existe
        if os.path.exists(filename):
            print(f"[!] Advertencia: El archivo {filename} ya existe. Se sobrescribirá.")
        
        # Guardar el informe
        with open(filename, "w") as file:
            file.write("--- Informe de Reconocimiento ---\n")
            for host, ports in report.items():
                file.write(f"\n[+] Host: {host}\n")
                for port, banner in ports.items():
                    file.write(f"  [+] Puerto {port}: {banner}\n")
        print(f"\n[+] Informe guardado en {os.path.abspath(filename)}")
    except Exception as e:
        print(f"[!] Error al guardar el informe: {e}", file=sys.stderr)

def main():
    print("|¬||¬| NetScanning by retr0 |¬||¬|\n")

    try:
        # Solicitar la red y los puertos a escanear
        network = input("Ingrese la red (formato CIDR, ejemplo: 192.168.1.0/24): ").strip()
        ports_input = input("Ingrese los puertos a escanear (ejemplo: 80,443,1-1024): ").strip()

        # Procesar los puertos ingresados
        ports_to_scan = set()
        for part in ports_input.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                ports_to_scan.update(range(start, end + 1))
            else:
                ports_to_scan.add(int(part))

        # Escanear hosts activos
        live_hosts = ping_sweep(network)
        if not live_hosts:
            print("[!] No se encontraron hosts activos.")
            return

        # Escanear puertos y obtener banners
        report = {}
        for host in live_hosts:
            open_ports = port_scan(host, ports_to_scan)
            report[host] = {}
            for port in open_ports:
                banner = banner_grabbing(host, port)
                report[host][port] = banner

        # Mostrar el informe final
        print("\n--- Informe de Reconocimiento ---")
        for host, ports in report.items():
            print(f"\n[+] Host: {host}")
            for port, banner in ports.items():
                print(f"  [+] Puerto {port}: {banner}")

        # Preguntar si se desea guardar el informe
        save_option = input("\n¿Desea guardar el informe en un archivo? (s/n): ").strip().lower()
        if save_option == "s":
            filename = input("Ingrese el nombre del archivo (o presione Enter para usar 'informe.txt'): ").strip()
            if not filename:
                filename = "informe.txt"
            save_report(report, filename)
        else:
            print("\n[+] Saliendo sin guardar el informe.")

    except KeyboardInterrupt:
        print("\n[!] Deteniendo...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
