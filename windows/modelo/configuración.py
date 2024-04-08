from __future__ import annotations
from .crypt import generar_claves, serializar_claves
from .database.DbHelper import DbHelper
from .database.contracts import OpcionesContract

class OpcionesUsuario:
    OPCIONES: OpcionesUsuario = None
    def __init__(self) -> None:
        if OpcionesUsuario.OPCIONES is None:
            self.OPCIONES = self
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
        if OpcionesUsuario.LISTA is None:
            OpcionesUsuario()
        return OpcionesUsuario.LISTA

    def cambiar_alias(self, nuevo_alias: str):
        self.alias = nuevo_alias
        # TODO: Update database
        print("ERROR: cambiar_alias (OpcionesUsuario) no está terminado (mirar seq_cambiar_alias para más detalles)")
    
    def cambiar_id(self, nuevo_id: str):
        self.id = nuevo_id
        # TODO: Update database
        print("ERROR: cambiar_id (OpcionesUsuario) no está terminado (mirar seq_cambiar_identificador para más detalles)")
