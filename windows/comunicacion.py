from __future__ import annotations

from queue import Queue
import socket
import threading
import time

from .modelo.configuración import OpcionesUsuario

from .discover import Direccion, get_ip_range, scan_lan

class Enum:
    pass

class TipoMensaje(Enum):
    TEXTO = 0x00
    FICHERO = 0x01
    CONTINUACION_FICHERO = 0x02
    IDENTIFICACION = 0x03
    PEDIR_IDENTIFICACION = 0x04
    SOLICITAR_PERMISO_ARCHIVO = 0x05
    RESPUESTA_PERMISO_ARCHIVO = 0x06

class SolicitarPermisoArchivo:
    def __init__(self) -> None:
        raise NotImplementedError
        pass

    def from_bytes(data: bytes) -> PedirIdentificacion:
        raise NotImplementedError
        if len(data) > 0:
            raise Exception("SolicitarPermisoArchivo es un mensaje de tamaño 0")
        return PedirIdentificacion()

    def to_bytes(self) -> bytes:
        raise NotImplementedError
        return bytes()
    
    def bytes_con_cabecera(self) -> bytes:
        raise NotImplementedError
        return Cabecera(None, TipoMensaje.PEDIR_IDENTIFICACION, 0).to_bytes()

class RespuestaPermisoArchivo:
    def __init__(self) -> None:
        raise NotImplementedError
        pass

    def from_bytes(data: bytes) -> PedirIdentificacion:
        raise NotImplementedError
        if len(data) > 0:
            raise Exception("RespuestaPermisoArchivo es un mensaje de tamaño 0")
        return PedirIdentificacion()

    def to_bytes(self) -> bytes:
        raise NotImplementedError
        return bytes()
    
    def bytes_con_cabecera(self) -> bytes:
        raise NotImplementedError
        return Cabecera(None, TipoMensaje.PEDIR_IDENTIFICACION, 0).to_bytes()

class Texto:
    def __init__(self, data: bytes | None, mensaje: str) -> None:
        self.mensaje = str

    def from_bytes(data: bytes) -> Texto:
        cursor = 0
        tamaño_mensaje = data[cursor:cursor+2] # 2 bytes: tamaño del mensaje
        cursor += 2
        mensaje = data[cursor:cursor+tamaño_mensaje].decode("utf-8")
        cursor += tamaño_mensaje

        return Texto(data, mensaje)

class Fichero:
    def __init__(self, data: bytes | None, mensaje: str, contenido) -> None:
        self.nombre = str
        self.mensaje

    def from_bytes(data: bytes) -> Fichero:
        cursor = 0
        tamaño_mensaje = data[cursor:cursor+2] # 2 bytes: tamaño del mensaje
        cursor += 2
        mensaje = data[cursor:cursor+tamaño_mensaje].decode("utf-8")
        cursor += tamaño_mensaje

        return Fichero(data, mensaje)
class CabeceraFichero:
    TAMAÑO_MINIMO: int = 4
    def __init__(self, data: bytes | None, metadata: str) -> None:
        self.data = data
        self.metadata = metadata
    
    def read_from_socket(conn: socket.socket) -> CabeceraFichero:
        data = conn.recv(CabeceraFichero.TAMAÑO_MINIMO)
        cursor = 0
        metadata_size = data[cursor:cursor+4]
        cursor += 4

        metadata = conn.recv(metadata_size).decode("utf-8")

        return CabeceraFichero(data, metadata_size, metadata)
    
    def to_bytes(self) -> bytes:
        metadata_size = len(self.metadata).to_bytes(4)
        metadata = self.metadata.encode("utf-8")

        return metadata_size + metadata

class Cabecera:
    TAMAÑO: int = 5
    def __init__(self, data: bytes | None, type: TipoMensaje, message_size: int) -> None:
        self.data = data
        self.type = type
        self.message_size = message_size

    def read_from_socket(conn: socket.socket) -> Cabecera:
        data = conn.recv(Cabecera.TAMAÑO)
        cursor = 0
        type = data[cursor] # 1 byte: tipo
        cursor += 1
        message_size = int.from_bytes(data[cursor:cursor+4]) # 4 bytes: tamaño del cuerpo
        # Tamaño máximo de mensaje: casi 4 GiB
        cursor += 4
        return Cabecera(data, type, message_size)

    def to_bytes(self) -> bytes:
        type = self.type.to_bytes(1)
        message_size = self.message_size.to_bytes(4)

        return type + message_size

class Identificacion:
    def __init__(self, data: bytes | None, alias: str, id: str) -> None:
        self.alias = str
        self.id = str

    def from_bytes(data: bytes) -> Identificacion:
        cursor = 0
        tamaño_alias = data[cursor:cursor+2] # 2 bytes: tamaño del alias
        cursor += 2
        tamaño_id = data[cursor:cursor+2] # 2 bytes: tamaño del id
        cursor += 2
        alias = data[cursor:cursor+tamaño_alias].decode("utf-8")
        cursor += tamaño_alias
        id = data[cursor:cursor+tamaño_id].decode("utf-8")
        cursor += tamaño_id

        return Identificacion(data, alias, id)
    
    def to_bytes(self) -> bytes:
        tamaño_alias = len(self.alias).to_bytes(2)
        tamaño_id = len(self.id).to_bytes(2)
        alias = self.alias.encode("utf-8")
        id = self.id.encode("utf-8")

        return tamaño_alias + tamaño_id + alias + id

    def bytes_con_cabecera(self) -> bytes:
        auto_bytes = self.to_bytes()
        cabecera = Cabecera(None, TipoMensaje.IDENTIFICACION, len(auto_bytes)).to_bytes()

        return cabecera + auto_bytes

class PedirIdentificacion:
    def __init__(self) -> None:
        pass

    def from_bytes(data: bytes) -> PedirIdentificacion:
        if len(data) > 0:
            raise Exception("PedirIdentificación es un mensaje de tamaño 0")
        return PedirIdentificacion()

    def to_bytes(self) -> bytes:
        return bytes()
    
    def bytes_con_cabecera(self) -> bytes:
        return Cabecera(None, TipoMensaje.PEDIR_IDENTIFICACION, 0).to_bytes()


class Comunicacion:

    def __init__(self) -> None:
        pass

    def enviar_mensaje(self, usuario, chat, mensaje: str):
        
        destination_ip = usuario.ip
        message = chat.entry_message.get()
        
        #se cofigura un socket para el envío
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((destination_ip, 12345))
            #s.sendall(f"TEXT\n{message}".encode('utf-8'))


            #se crea la cabecera
            cabecera = Cabecera()
            cabecera.to_bytes()
            
            #se envía el contenido del paquete
            s.sendall(cabecera)
            
            s.close()
            
            #self.text_area.insert(tk.END, f"[You] {message}\n")
        except Exception as e:
            print(f"An error occurred while sending message: {str(e)}")

    def send_file(self):
        destination_ip = self.usuario.ip
        #a diferencia de send_message el archivo se obtiene de una ventana emergente
        

        #guichat llama esta función para enviar mensaje/archivo
        #file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    file_content = file.read()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((destination_ip, 12345))  # se lee el archivo y se envía por el socket
                s.sendall(f"FILE\n{file_path.split('/')[-1]}".encode('utf-8'))
                s.sendall(file_content)
                s.close()
                self.text_area.insert(tk.END, f"[You] Sent file: {file_path}\n")
            except Exception as e:
                print(f"An error occurred while sending file: {str(e)}")
    
    def receive_messages(self,):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', 12345)) 
        s.listen(1)

        while True:
            conn, addr = s.accept()
            
            with conn:

                #se selecciona el tipo a recibir
                data = conn.recv(1024)
                message_type, *rest = data.decode('utf-8').split('\n')

                if message_type == 'TEXT':
                        message = '\n'.join(rest)
                        self.text_area.insert(tk.END, f"[{addr[0]}] {message}\n")

                elif message_type == 'FILE':
                        file_name = rest[0]
                        print(file_name)
                        with open(file_name, 'wb') as file:
                            while True:
                                data = conn.recv(1024)
                                if not data:
                                    break
                                file.write(data)
                                file.write(conn.recv(1024))
                        self.text_area.insert(tk.END, f"[{addr[0]}] Received file: {file_name}\n")
                        break

def discover() -> list[Identificacion]:
    ip_range = get_ip_range()
    devices = scan_lan(ip_range)
    print("Dispositivos en la LAN:")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", 12345))
    sock.listen(len(devices))
    send_threads: list[threading.Thread] = []
    stdout_lock = threading.Lock()
    for device in devices:
        print(f"IP: {device.ip}, MAC: {device.mac}")
        th = threading.Thread(target=lambda : pedir_identificacion(device, stdout_lock))
        th.start()
        send_threads.append(th)
    for th in send_threads:
        th.join(5.0)
    print("joined all")
    q = Queue()
    identificaciones = []
    th = threading.Thread(target=lambda : response_listener(sock, q, identificaciones))
    th.start()

    time.sleep(5)
    q.put(True)
    th.join(5.0)
    if th.is_alive():
        print("Didn't end")
    th.join()

    return identificaciones

def pedir_identificacion(device: Direccion, stdout_lock: threading.Lock):
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_sock.settimeout(3.0)
    try:
        send_sock.connect((device.ip, 12345))
        send_sock.sendall(PedirIdentificacion().bytes_con_cabecera())
    except ConnectionRefusedError:
        stdout_lock.acquire(timeout=1.0)
        print(f"{device.ip}: Ese dispositivo no acepta el protocolo")
        stdout_lock.release()
    except TimeoutError:
        stdout_lock.acquire(timeout=1.0)
        print(f"{device.ip}: Timeout")
        stdout_lock.release()

def response_listener(sock: socket.socket, q: Queue, identificaciones: list[Identificacion]):
    sock.setblocking(False)
    sock.settimeout(3.0)
    while q.empty():
        try:
            (con, addr) = sock.accept()
            cabecera: Cabecera = Cabecera.read_from_socket(con)
            print(cabecera.message_size)
            if cabecera.type == TipoMensaje.IDENTIFICACION:
                if cabecera.message_size == 0:
                    # Un mensaje de tipo identificación tiene que tener cuerpo
                    continue
                cuerpo = con.recv(cabecera.message_size)
                identificacion = Identificacion.from_bytes(cuerpo)
                identificaciones.append(identificacion)
        except TimeoutError:
            # Es para que de vez en cuando mire q.empty()
            pass

    return identificaciones

def responder_identificacion(ip: str):
    """Asumimos que hemos recibido un mensaje PedirIdenificacion"""
    opciones = OpcionesUsuario.get_opciones()
    alias = opciones.get_alias()
    id = opciones.get_display_id()
    mensaje = Identificacion(None, alias, id)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 12345))
    sock.sendall(mensaje.bytes_con_cabecera())

