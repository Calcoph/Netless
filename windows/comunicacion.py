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
    SOLICITAR_CONEXION = 0x07
    CONEXION_ACEPTADA = 0x08

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
        self.mensaje = mensaje

    def from_bytes(data: bytes) -> Texto:
        mensaje = data.decode("utf-8")

        return Texto(data, mensaje)

    def to_bytes(self) -> bytes:
        mensaje = self.mensaje.encode("utf-8")
        return mensaje

    def bytes_con_cabecera(self) -> bytes:
        auto_bytes = self.to_bytes()
        cabecera = Cabecera(None, TipoMensaje.TEXTO, len(auto_bytes)).to_bytes()

        return cabecera + auto_bytes

class Fichero:
    def __init__(self, data: bytes | None, mensaje: bytes) -> None:
        self.mensaje = mensaje

    def from_bytes(data: bytes) -> Fichero:
        mensaje = data.decode("utf-8")
        return Fichero(data, mensaje)

    def to_bytes(self) -> bytes:
        #no hace falta codificar ya que los datos serán enviados como bytes
        #datos = self.mensaje.encode("utf-8")
        return self.mensaje

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
        print(len(data))
        cursor = 0
        type = data[cursor] # 1 byte: tipo
        cursor += 1
        message_size = int.from_bytes(data[cursor:cursor+4], "little") # 4 bytes: tamaño del cuerpo
        # Tamaño máximo de mensaje: casi 4 GiB
        cursor += 4
        return Cabecera(data, type, message_size)

    def to_bytes(self) -> bytes:
        type = self.type.to_bytes(1, "little")
        message_size = self.message_size.to_bytes(4, "little")

        return type + message_size

class Identificacion:
    def __init__(self, data: bytes | None, alias: str, id: str) -> None:
        self.alias = alias
        self.id = id

    def from_bytes(data: bytes) -> Identificacion:
        cursor = 0
        tamaño_alias = int.from_bytes(data[cursor:cursor+2], "little") # 2 bytes: tamaño del alias
        cursor += 2
        tamaño_id = int.from_bytes(data[cursor:cursor+2], "little") # 2 bytes: tamaño del id
        cursor += 2
        alias = data[cursor:cursor+tamaño_alias].decode("utf-8")
        cursor += tamaño_alias
        id = data[cursor:cursor+tamaño_id].decode("utf-8")
        cursor += tamaño_id

        return Identificacion(data, alias, id)

    def to_bytes(self) -> bytes:
        tamaño_alias = len(self.alias).to_bytes(2, "little")
        tamaño_id = len(self.id).to_bytes(2, "little")
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

class SolicitarConexion:
    def __init__(self) -> None:
        pass

    def from_bytes(data: bytes) -> SolicitarConexion:
        if len(data) > 0:
            raise Exception("SolicitarConexion es un mensaje de tamaño 0")
        return SolicitarConexion()

    def to_bytes(self) -> bytes:
        return bytes()

    def bytes_con_cabecera(self) -> bytes:
        return Cabecera(None, TipoMensaje.SOLICITAR_CONEXION, 0).to_bytes()

class ConexionAceptada:
    def __init__(self) -> None:
        pass

    def from_bytes(data: bytes) -> ConexionAceptada:
        if len(data) > 0:
            raise Exception("ConexionAceptada es un mensaje de tamaño 0")
        return ConexionAceptada()

    def to_bytes(self) -> bytes:
        return bytes()

    def bytes_con_cabecera(self) -> bytes:
        return Cabecera(None, TipoMensaje.CONEXION_ACEPTADA, 0).to_bytes()

class ComunicacionListener:
    def __init__(self, rx: Queue, tx: Queue) -> None:
        self.rx = rx
        self.tx = tx
        th = threading.Thread(target=self.listen, daemon=True)
        th.start()

    def listen(self):
        handlers = {
            TipoMensaje.PEDIR_IDENTIFICACION: self.handle_pedir_identificacion,
            TipoMensaje.IDENTIFICACION: self.handle_identificacion,
            TipoMensaje.TEXTO: self.handle_texto,
            TipoMensaje.SOLICITAR_PERMISO_ARCHIVO: self.handle_solicitar_permiso_archivo,
            TipoMensaje.RESPUESTA_PERMISO_ARCHIVO: self.handle_respuesta_permiso_archivo,
            TipoMensaje.CONTINUACION_FICHERO: self.handle_continuacion_fichero,
            TipoMensaje.FICHERO: self.handle_fichero,
            TipoMensaje.SOLICITAR_CONEXION: self.handle_solicitar_conexion,
            TipoMensaje.CONEXION_ACEPTADA: self.handle_conexion_aceptada,
        }
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener_socket.bind(("0.0.0.0", 12345))
        listener_socket.listen(50)
        listener_socket.setblocking(False)
        listener_socket.settimeout(3.0) # Cada 3 segundos mirará la cola

        while True:
            while not self.rx.empty():
                message = self.rx.get()
            try:
                (con, addr) = listener_socket.accept()
                print(f"Aceptado mensaje de {addr[0]}")
                cabecera: Cabecera = Cabecera.read_from_socket(con)
                print(cabecera.type)
                print("\n")
                handlers[cabecera.type](cabecera, con, addr[0])
            except TimeoutError:
                # Es para que de vez en cuando mire self.rx
                pass

    def handle_identificacion(self, cabecera: Cabecera, con: socket.socket, addr):
        if cabecera.message_size == 0:
            # Un mensaje de tipo identificación tiene que tener cuerpo
            return
        cuerpo = con.recv(cabecera.message_size)
        identificacion = Identificacion.from_bytes(cuerpo)
        print(f"Se ha enviado ident a {addr}")
        self.tx.put(((TipoMensaje.IDENTIFICACION, addr), identificacion))

    def handle_texto(self, cabecera: Cabecera, con: socket.socket, addr):
        ###################################################
        cuerpo = con.recv(cabecera.message_size)
        texto = Texto.from_bytes(cuerpo)
        print(f"Se ha enviado ident a {addr}")
        self.tx.put(((TipoMensaje.TEXTO, addr), texto))
        ###################################################raise NotImplementedError

    def handle_pedir_identificacion(self, cabecera: Cabecera, con: socket.socket, addr):
        print(f"Se ha pedido ident desde {addr}")
        self.tx.put(((TipoMensaje.PEDIR_IDENTIFICACION, addr), None))

    def handle_solicitar_permiso_archivo(self, cabecera: Cabecera, con: socket.socket, addr):
        raise NotImplementedError

    def handle_respuesta_permiso_archivo(self, cabecera: Cabecera, con: socket.socket, addr):
        raise NotImplementedError

    def handle_continuacion_fichero(self, cabecera: Cabecera, con: socket.socket, addr):
        raise NotImplementedError

    def handle_fichero(self, cabecera: Cabecera, con: socket.socket, addr):
        raise NotImplementedError

    def handle_solicitar_conexion(self, cabecera: Cabecera, con: socket.socket, addr):
        self.tx.put(((TipoMensaje.SOLICITAR_CONEXION, addr), None))

    def handle_conexion_aceptada(self, cabecera: Cabecera, con: socket.socket, addr):
        print(f"Se ha aceptado conexion ident desde {addr}")
        self.tx.put(((TipoMensaje.CONEXION_ACEPTADA, addr), None))

class Comunicacion:
    COMM: Comunicacion = None
    LISTENER: ComunicacionListener = None
    def __init__(self) -> None:
        if Comunicacion.COMM is None:
            Comunicacion.COMM = self
            self.rx = Queue()
            self.tx = Queue()
            Comunicacion.LISTENER = ComunicacionListener(self.tx, self.rx)
        else:
            raise SystemError

    def get_com():
        if Comunicacion.COMM is None:
            Comunicacion()

        return Comunicacion.COMM

    def enviar_mensaje(usuario, mensaje: str):
        destination_ip = usuario.ip

        #se cofigura un socket para el envío
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((destination_ip, 12345))
            texto = Texto(None, mensaje)
            mensaje = texto.bytes_con_cabecera()
            #se envía el contenido del paquete
            print(f"len: {len(mensaje)}")
            s.sendall(mensaje)
            s.close()
            #self.text_area.insert(tk.END, f"[You] {message}\n")
        except Exception as e:
            print(f"An error occurred while sending message: {str(e)}")

    def send_file(self, usuario, chat, mensaje: str):
        destination_ip = self.usuario.ip
        #guichat llama esta función para enviar mensaje/archivo
        file_path = chat.filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    file_content = file.read()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((destination_ip, 12345))  # se lee el archivo y se envía por el socket


                #se envía la cabecera genérica
                cabecera_generica = Cabecera()
                cabecera_generica.type = TipoMensaje.FICHERO
                cabecera_generica_enviar = cabecera_generica.to_bytes()
                #se crea la cabecera del fichero
                cabecera = CabeceraFichero()
                cabecera.metadata = file_path
                envio_cabecera = cabecera.to_bytes()
                contenido = Fichero()
                contenido.mensaje = file_content
                contenido_enviar = contenido.to_bytes()
                s.sendall(cabecera_generica + envio_cabecera + contenido_enviar)
                s.close()
                #self.text_area.insert(tk.END, f"[You] Sent file: {file_path}\n")
            except Exception as e:
                print(f"An error occurred while sending file: {str(e)}")

    def receive_messages(self,):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', 12345))
        s.listen(1)

        while True:
            conn, addr = s.accept()
            with conn:

                #se recibe la cabecera genérica

                data = conn.recv(1024)
                message_type, *rest = data.decode('utf-8').split('\n')
                """""
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
                """""

    def discover(self):
        ip_range = get_ip_range()
        devices = scan_lan(ip_range)
        print("Dispositivos en la LAN:")
        stdout_lock = threading.Lock()
        for device in devices:
            print(f"IP: {device.ip}, MAC: {device.mac}")
            th = threading.Thread(target=lambda : Comunicacion.pedir_identificacion(device, stdout_lock), daemon=True)
            th.start()

    def pedir_identificacion(device: Direccion, stdout_lock: threading.Lock):
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_sock.settimeout(3.0)
        try:
            send_sock.connect((device.ip, 12345))
            send_sock.sendall(PedirIdentificacion().bytes_con_cabecera())
            print(f"enviado a {device.ip}")
        except ConnectionRefusedError:
            stdout_lock.acquire(timeout=1.0)
            print(f"{device.ip}: Ese dispositivo no acepta el protocolo")
            stdout_lock.release()
        except TimeoutError:
            stdout_lock.acquire(timeout=1.0)
            print(f"{device.ip}: Timeout")
            stdout_lock.release()

    def identificarse(ip: str):
        """Respuesta a un mensaje PedirIdenificacion"""
        opciones = OpcionesUsuario.get_opciones()
        alias = opciones.get_alias()
        id = opciones.get_display_id()
        mensaje = Identificacion(None, alias, id)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, 12345))
        sock.sendall(mensaje.bytes_con_cabecera())

    def solicitar_conexion(ip_destino: str):
        mensaje = SolicitarConexion()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip_destino, 12345))
        sock.sendall(mensaje.bytes_con_cabecera())

    def aceptar_conexion(ip: str):
        mensaje = ConexionAceptada()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, 12345))
        sock.sendall(mensaje.bytes_con_cabecera())
