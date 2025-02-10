import subprocess
import ipaddress
import socket
import shlex
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_host(ip):
    
    try:
        response = subprocess.run(
            ['ping', '-c', '1', '-W', '1', shlex.quote(str(ip))],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return ip if response.returncode == 0 else None
    except Exception:
        return None

def ping_sweep(network):
    
    print("\nIniciando Ping Sweep...")
    live_hosts = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(ping_host, ip): ip for ip in ipaddress.IPv4Network(network, strict=False)}
        try:
            for future in as_completed(futures):
                result = future.result()
                if result:
                    print(f"Host activo: {result}")
                    live_hosts.append(str(result))
        except KeyboardInterrupt:
            print("\nDeteniendo...")
            time.sleep(2)
            sys.exit(0)
    return live_hosts

def scan_port(ip, port):
    
    try:
        with socket.create_connection((ip, port), timeout=1):
            return port
    except (socket.timeout, ConnectionRefusedError):
        return None

def port_scan(ip):

    print(f"\nEscaneando puertos en {ip}...")
    open_ports = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(1, 1025)}
        try:
            for future in as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
        except KeyboardInterrupt:
            print("\nDeteniendo...")
            time.sleep(2)
            sys.exit(0)
    return open_ports

def banner_grabbing(ip, port):
    """Obtiene el banner de un servicio en un puerto abierto."""
    try:
        with socket.create_connection((ip, port), timeout=3) as s:
            s.sendall(b"GET / HTTP/1.1\r\nHost: test\r\n\r\n")  
            response = s.recv(1024).decode(errors="ignore").strip()

            
            for line in response.split("\n"):
                if "Server:" in line:
                    return line.strip()  
            
            return "No se pudo obtener el banner correctamente"
    except Exception:
        return "No se pudo obtener el banner"


def main():
    print("|¬||¬|NetScanning by retr0|¬||¬|\n")

    try:
        network = input("Ingrese la red (formato CIDR, ejemplo: 192.168.1.0/24): ").strip()
        live_hosts = ping_sweep(network)

        report = {}
        for host in live_hosts:
            open_ports = port_scan(host)
            report[host] = {}
            for port in open_ports:
                banner = banner_grabbing(host, port)
                report[host][port] = banner

        print("\n--- Informe de Reconocimiento ---")
        for host, ports in report.items():
            print(f"\nHost: {host}")
            for port, banner in ports.items():
                print(f"  Puerto {port}: {banner}")

    except KeyboardInterrupt:
        print("\nDeteniendo...")
        time.sleep(2)
        sys.exit(0)

if __name__ == "__main__":
    main()

