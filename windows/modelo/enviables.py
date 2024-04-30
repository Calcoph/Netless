from __future__ import annotations
from datetime import datetime

from windows.modelo.database.DbHelper import DbHelper
from windows.modelo.database.contracts import EnviableContract, FicheroContract, MensajeContract

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
        db = DbHelper.get()
        columns = [
            EnviableContract.COLUMN_NAME_DIRECCION,
            EnviableContract.COLUMN_NAME_FECHA,
            EnviableContract.COLUMN_NAME_FICH_ID,
            EnviableContract.COLUMN_NAME_MENS_ID,
        ]

        (direccion, fecha, fich_id, mens_id) = db.select(
            EnviableContract.TABLE_NAME,
            column_names=columns,
            where=f"_ID = ?",
            where_values=[id]
        ).fetch_one()
        direccion = Dirección.from_int(direccion)
        if fich_id is not None:
            return Fichero.inicializar(direccion, fecha, fich_id)
        elif mens_id is not None:
            return Mensaje.inicializar(direccion, fecha, mens_id)
        else:
            print("No se ha podido inicializar el enviable porque no es ni mensaje ni fichero")

        return None

class Fichero(Enviable):
    def __init__(self, nombre: str, tamaño: int, dirección: Dirección) -> None:
        self.nombre = nombre
        self.tamaño = tamaño

        super().__init__(dirección)

    def get_nombre(self) -> str:
        return self.nombre

    def inicializar(dirección: Dirección, fecha: datetime, id: str) -> Fichero:
        db = DbHelper.get()
        columns = [
            FicheroContract.COLUMN_NAME_NOMBRE
        ]

        (nombre,) = db.select(
            FicheroContract.TABLE_NAME,
            column_names=columns,
            where=f"_ID = ?",
            where_values=[id]
        ).fetch_one()

        fichero = Fichero(nombre, 0, dirección)
        fichero.fecha = fecha
        return fichero

class Mensaje(Enviable):
    def __init__(self, msg: str, dirección: Dirección) -> None:
        self.msg = msg
        super().__init__(dirección)

    def inicializar(dirección: Dirección, fecha: datetime, id: str) -> Mensaje:
        db = DbHelper.get()
        columns = [
            MensajeContract.COLUMN_NAME_MENS
        ]

        (mens,) = db.select(
            MensajeContract.TABLE_NAME,
            column_names=columns,
            where=f"_ID = ?",
            where_values=[id]
        ).fetch_one()

        mensaje = Mensaje(mens, dirección)
        mensaje.fecha = fecha
        return mensaje
