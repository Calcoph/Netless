from __future__ import annotations
from .crypt import generar_claves, serializar_claves

class OpcionesUsuario:
    OPCIONES: OpcionesUsuario = None
    def __init__(self) -> None:
        if OpcionesUsuario.OPCIONES is None:
            self.alias = ""
            self.id = ""
            self.OPCIONES = self
        else:
            raise SystemError
    
    def get_opciones() -> OpcionesUsuario:
        if OpcionesUsuario.LISTA is None:
            OpcionesUsuario()
        return OpcionesUsuario.LISTA

    def cambiar_alias(self, nuevo_alias: str):
        self.alias = nuevo_alias
    
    def cambiar_id(self, nuevo_id: str):
        self.id = nuevo_id
    
    def generar_id_aleatorio() -> str:
        c_privada, c_publica = generar_claves()
        c_privada, c_publica = serializar_claves(c_privada, c_publica)
        c_publica = c_publica.decode()
        return c_publica
