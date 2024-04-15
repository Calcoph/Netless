from __future__ import annotations
from .database.DbHelper import DbHelper
from .database.contracts import UsuarioContract, WhiteListContract

class Whitelist:
    LISTA: Whitelist = None
    def __init__(self) -> None:
        if Whitelist.LISTA is None:
            Whitelist.LISTA = self
            self.lista_ids: list[str] = []
        else:
            raise SystemError
    
    def get_whitelist() -> Whitelist:
        if Whitelist.LISTA is None:
            Whitelist()
        return Whitelist.LISTA
    
    def añadir_usuario(self, id: str):
        self.lista_ids.append(id)
        db_helper = DbHelper.get()

        columns = [
            UsuarioContract.COLUMN_NAME_ID
        ]
        where = f"{UsuarioContract.COLUMN_NAME_ID} = ?"
        where_values = (id,)
        usr_id = db_helper.select(UsuarioContract.TABLE_NAME, column_names=columns, where=where, where_values=where_values).fetch_one()[0]

        columns = [
            WhiteListContract.COLUMN_NAME_USR_ID
        ]
        db_helper.insert(WhiteListContract.TABLE_NAME, (usr_id,), column_names=columns)
    
    def quitar_usuario(self, id: str):
        remove_index = None
        for (index, stored_id) in enumerate(self.lista_ids):
            if stored_id == id:
                remove_index = index
                break
        if remove_index is not None:
            self.lista_ids.pop(remove_index)

        db_helper = DbHelper.get()

        where = f"{WhiteListContract.COLUMN_NAME_USR_ID} = ?"
        where_values = (id,)
        db_helper.delete(WhiteListContract.TABLE_NAME, where, where_values)
    
    def usuario_aceptado(self, id: str) -> bool:
        return id in self.lista_ids
