from scapy.all import ARP, Ether, srp, conf, get_if_addr

class Direccion:
    def __init__(self, ip: str, mac: str) -> None:
        self.ip = ip
        self.mac = mac

def scan_lan(ip_range) -> list[Direccion]:
    # Crea un paquete ARP para descubrir dispositivos en la LAN
    arp_request = ARP(pdst=ip_range)

    # Crea un paquete Ethernet
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    # Concatena los paquetes Ethernet y ARP
    packet = ether / arp_request

    # Envía y recibe paquetes
    result = srp(packet, timeout=3, verbose=False)[0]

    # Lista para almacenar direcciones MAC e IPs
    devices: list[Direccion] = []

    for sent, received in result:
        # Agrega la dirección MAC e IP de cada dispositivo descubierto a la lista
        devices.append(Direccion(str(received.psrc), str(received.hwsrc)))

    found_self = False
    ip = str(get_if_addr(conf.iface))
    for dev in devices:
        if ip == dev.ip:
            found_self = True

    if not found_self:
        devices.append(Direccion(ip, "No Mac"))

    return devices


#una mejora posible es buscar poder seleccionar el interfaz en esta función, de momento solo funiona con la principal por default
def get_ip_range() -> str:
    ip = get_if_addr(conf.iface)  # default interface
    print(ip)
    ip = ip + "/24"
    return ip

#se obtiene la IP del equipo y se busca en el /24 de esa dirección
#discover()

# Imprime los dispositivos encontrados
