from __future__ import annotations

from socket import socket

from .chat import Enum

class TipoMensaje(Enum):
    TEXTO = 0x00
    FICHERO = 0x01
    CONTINUACION_FICHERO = 0x02

class CabeceraFichero:
    TAMAÑO_MINIMO: int = 4
    def __init__(self, data: bytes, metadata: str) -> None:
        self.data = data
        self.metadata = metadata
    
    def read_from_socket(conn: socket) -> CabeceraFichero:
        data = conn.recv(CabeceraFichero.TAMAÑO_MINIMO)
        cursor = 0
        metadata_size = data[cursor:cursor+4]
        cursor += 4

        metadata = conn.recv(metadata_size).decode("utf-8")

        return CabeceraFichero(data, metadata_size, metadata)

class Cabecera:
    TAMAÑO: int = 5
    def __init__(self, data: bytes, type: TipoMensaje, message_size: int) -> None:
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
