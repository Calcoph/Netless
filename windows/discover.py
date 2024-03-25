from scapy.all import ARP, Ether, srp, conf, get_if_addr

def scan_lan(ip_range):
    # Crea un paquete ARP para descubrir dispositivos en la LAN
    arp_request = ARP(pdst=ip_range)

    # Crea un paquete Ethernet
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    # Concatena los paquetes Ethernet y ARP
    packet = ether / arp_request

    # Envía y recibe paquetes
    result = srp(packet, timeout=3, verbose=False)[0]

    # Lista para almacenar direcciones MAC e IPs
    devices = []

    for sent, received in result:
        # Agrega la dirección MAC e IP de cada dispositivo descubierto a la lista
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices


#una mejora posible es buscar poder seleccionar el interfaz en esta función, de momento solo funiona con la principal por default
def get_ip_range():
    ip = get_if_addr(conf.iface)  # default interface
    print(ip)
    ip = ip + "/24"
    return ip


def discover():
    ip_range = get_ip_range()
    devices = scan_lan(ip_range)
    print("Dispositivos en la LAN:")
    for device in devices:
        print(f"IP: {device['ip']}, MAC: {device['mac']}")
    return devices

#se obtiene la IP del equipo y se busca en el /24 de esa dirección
discover()

# Imprime los dispositivos encontrados

