from __future__ import annotations
from .crypt import generar_id_aleatorio
from .database.DbHelper import DbHelper
from .database.contracts import OpcionesContract

class OpcionesUsuario:
    OPCIONES: OpcionesUsuario = None
    def __init__(self) -> None:
        if OpcionesUsuario.OPCIONES is None:
            OpcionesUsuario.OPCIONES = self
            db = DbHelper.get()
            columns = [
                OpcionesContract.COLUMN_NAME_ALIAS,
                OpcionesContract.COLUMN_NAME_ID,
            ]
            alias, id = db.select(OpcionesContract.TABLE_NAME, columns).fetch_one()
            self.alias = alias
            self.id = id
        else:
            raise SystemError
    
    def get_opciones() -> OpcionesUsuario:
        if OpcionesUsuario.OPCIONES is None:
            OpcionesUsuario()
        return OpcionesUsuario.OPCIONES

    def cambiar_alias(self, nuevo_alias: str):
        self.alias = nuevo_alias
        db = DbHelper.get()
        column_names = [
            OpcionesContract.COLUMN_NAME_ALIAS
        ]
        column_values = (nuevo_alias,)
        db.update(OpcionesContract.TABLE_NAME, column_names, column_values)

    def cambiar_id(self):
        nuevo_id = generar_id_aleatorio() 
        self.id = nuevo_id
        db = DbHelper.get()
        column_names = [
            OpcionesContract.COLUMN_NAME_ID
        ]
        column_values = (nuevo_id,)
        db.update(OpcionesContract.TABLE_NAME, column_names, column_values)

    def get_alias(self) -> str:
        return self.alias

    def get_id(self) -> str:
        return self.id
    
    def get_display_id(self) -> str:
        """Sólo muestra los primeros 20 caracteres de la 3ª línea de la clave"""
        return self.id.split("\n")[3][0:20] + "..."
