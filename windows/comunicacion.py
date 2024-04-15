from __future__ import annotations

from socket import socket

from .chat import Enum

class TipoMensaje(Enum):
    TEXTO = 0x00
    FICHERO = 0x01
    CONTINUACION_FICHERO = 0x02
    IDENTIFICACION = 0x03
    PEDIR_IDENTIFICACION = 0x04

class CabeceraFichero:
    TAMAÑO_MINIMO: int = 4
    def __init__(self, data: bytes | None, metadata: str) -> None:
        self.data = data
        self.metadata = metadata
    
    def read_from_socket(conn: socket) -> CabeceraFichero:
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

    def read_from_socket(conn: socket) -> Cabecera:
        data = conn.recv(Cabecera.TAMAÑO)
        cursor = 0
        type = data[cursor] # 1 byte: tipo
        cursor += 1
        message_size = data[cursor:cursor+4] # 4 bytes: tamaño del cuerpo
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
    
    def butes_con_cabecera(self) -> bytes:
        return Cabecera(None, TipoMensaje.PEDIR_IDENTIFICACION, 0).to_bytes()
