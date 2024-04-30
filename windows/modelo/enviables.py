from __future__ import annotations
from datetime import datetime

class Enum:
    pass

class Dirección(Enum):
    Entrante = 1
    Saliente = 2

    def __init__(self, i: int) -> None:
        if self == Dirección.Entrante:
            self.dir = Dirección.Entrante
        elif self == Dirección.Saliente:
            self.dir = Dirección.Saliente
        else:
            raise ValueError


    def to_int(self) -> int:
        return self.dir

    def from_int(i: int) -> Dirección:
        return Dirección(i)

class Enviable:
    def __init__(self, dirección: Dirección) -> None:
        self.fecha = datetime.now()
        self.dirección = dirección

    def mostrar_en_pantalla(self):
        raise NotImplementedError

    def get_fecha(self) -> datetime:
        return self.fecha

    def get_dirección(self) -> Dirección:
        return self.dirección

    def inicializar(id: str) -> Enviable:
        raise NotImplementedError

class Fichero(Enviable):
    def __init__(self, nombre: str, tamaño: int, dirección: Dirección) -> None:
        self.nombre = nombre
        self.tamaño = tamaño

        super().__init__(dirección)

    def get_nombre(self) -> str:
        return self.nombre

class Mensaje(Enviable):
    def __init__(self, msg: str, dirección: Dirección) -> None:
        self.msg = msg
        super().__init__(dirección)
