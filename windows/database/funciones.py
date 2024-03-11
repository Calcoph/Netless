from typing import Generic

from sqlite3 import Cursor
from DbHelper import DbHelper

from contracts import FicheroContract, EnviableContract, UsuarioContract, EnviablesChatContract, MensajeContract, ChatContract, WhiteListContract

############ HistorialChat ########################3

def añadir_fichero(fichero: Fichero, id_usuario: str):
    nombre = fichero.get_nombre()
    fecha = fichero.get_fecha()
    direccion = fichero.get_direccion()

    db_helper = DbHelper.get()
    columns = [
        FicheroContract.COLUMN_NAME_NOMBRE
    ]
    fich_id = db_helper.insert(FicheroContract.TABLE_NAME, nombre, column_names=columns)

    columns = [
        EnviableContract.COLUMN_NAME_FECHA,
        EnviableContract.COLUMN_NAME_DIRECCION,
        EnviableContract.COLUMN_NAME_FICH_ID
    ]
    env_id = db_helper.insert(EnviableContract.TABLE_NAME, (fecha, direccion, fich_id), column_names=columns)
    añadir_enviable(fichero, env_id, id_usuario)

def añadir_mensaje(mens: Mensaje, id_usuario: str):
    msg = mens.msg
    fecha = mens.get_fecha()
    direccion = mens.get_direccion()

    db_helper = DbHelper.get()

    columns = [
        MensajeContract.COLUMN_NAME_MENS
    ]
    mens_id = db_helper.insert(MensajeContract.TABLE_NAME, msg, column_names=columns)

    columns = [
        EnviableContract.COLUMN_NAME_FECHA,
        EnviableContract.COLUMN_NAME_DIRECCION,
        EnviableContract.COLUMN_NAME_MENS_ID
    ]
    env_id = db_helper.insert(EnviableContract.TABLE_NAME, (fecha, direccion, mens_id), column_names=columns)

    añadir_enviable(mens, env_id, id_usuario)


def añadir_enviable(enviable: Enviable, env_id: int, id_usuario: str):
    lista_enviables.append(enviable)
    mostar_en_pantalla()

    db_helper = DbHelper.get()

    columns = [
        f"{UsuarioContract.TABLE_NAME}.{UsuarioContract.COLUMN_NAME_CHAT_ID}"
    ]
    where = f"{UsuarioContract.TABLE_NAME}.{UsuarioContract.COLUMN_NAME_ID} = ?"
    where_values = (id_usuario,)
    chat_id = db_helper.join_select(
        UsuarioContract.TABLE_NAME,
        ChatContract.TABLE_NAME,
        UsuarioContract.COLUMN_NAME_CHAT_ID,
        "_ID",
        column_names=columns,
        where=where,
        where_values=where_values
    ).fetch_one()

    columns = [
        EnviablesChatContract.COLUMN_NAME_CHAT_ID,
        EnviablesChatContract.COLUMN_NAME_ENV_ID
    ]
    db_helper.insert(EnviablesChatContract.TABLE_NAME, (chat_id, env_id), column_names=columns)

##################### Whitelist ######################
def añadir_usuario(id: str):
    listaIds.append(id)
    db_helper = DbHelper.get()

    columns = [
        UsuarioContract.COLUMN_NAME_ID
    ]
    where = f"{UsuarioContract.COLUMN_NAME_ID} = ?"
    where_values = (id,)
    usr_id = db_helper.select(UsuarioContract.TABLE_NAME, column_names=columns, where=where, where_values=where_values).fetch_one

    columns = [
        WhiteListContract.COLUMN_NAME_USR_ID
    ]
    db_helper.insert(WhiteListContract.TABLE_NAME, (usr_id,), column_names=columns)

def quitar_usuario(id: str):
    db_helper = DbHelper.get()

    where = f"{WhiteListContract.COLUMN_NAME_USR_ID} = ?"
    where_values = (id,)
    db_helper.delete(WhiteListContract.TABLE_NAME, where, where_values)
