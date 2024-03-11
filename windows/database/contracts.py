import sqlite3

class Contract:
    SQL_CREATE_ENTRIES = ""
    SQL_DELETE_ENTRIES = ""

class ChatContract(Contract):
    TABLE_NAME = "Chat"
    SQL_CREATE_ENTRIES = f"""CREATE TABLE {TABLE_NAME} (
_ID INTEGER PRIMARY KEY,
)"""
    SQL_DELETE_ENTRIES = f"DROP TABLE IF EXISTS {TABLE_NAME}"

class FicheroContract(Contract):
    TABLE_NAME = "Fichero"
    COLUMN_NAME_NOMBRE = "nombre"

    SQL_CREATE_ENTRIES = f"""
        CREATE TABLE {TABLE_NAME} (
            _ID INTEGER PRIMARY KEY,
            {COLUMN_NAME_NOMBRE} TEXT,
        )"""
    
    SQL_DELETE_ENTRIES = f"DROP TABLE IF EXISTS {TABLE_NAME}"

class MensajeContract(Contract):
    TABLE_NAME = "Mensaje"
    COLUMN_NAME_MENS = "mens"

    SQL_CREATE_ENTRIES = f"""
        CREATE TABLE {TABLE_NAME} (
            _ID INTEGER PRIMARY KEY,
            {COLUMN_NAME_MENS} TEXT,
        )"""
    
    SQL_DELETE_ENTRIES = f"DROP TABLE IF EXISTS {TABLE_NAME}"

class EnviableContract(Contract):
    TABLE_NAME = "Enviable"
    COLUMN_NAME_FECHA = "fecha"
    COLUMN_NAME_DIRECCION = "direccion"
    COLUMN_NAME_FICH_ID = "fich_id"
    COLUMN_NAME_MENS_ID = "mens_id"

    SQL_CREATE_ENTRIES = f"""
        CREATE TABLE {TABLE_NAME} (
            _ID INTEGER PRIMARY KEY,
            {COLUMN_NAME_FECHA} TEXT,
            {COLUMN_NAME_DIRECCION} INTEGER,
            {COLUMN_NAME_FICH_ID} INTEGER,
            {COLUMN_NAME_MENS_ID} INTEGER,
            CONSTRAINT fk_fich FOREIGN KEY ({COLUMN_NAME_FICH_ID}) REFERENCES {FicheroContract.TABLE_NAME} (_ID)
            CONSTRAINT fk_mens FOREIGN KEY ({COLUMN_NAME_MENS_ID}) REFERENCES {MensajeContract.TABLE_NAME} (_ID)
        )"""
    
    SQL_DELETE_ENTRIES = f"DROP TABLE IF EXISTS {TABLE_NAME}"

class EnviablesChatContract(Contract):
    TABLE_NAME = "EnviablesChat"
    COLUMN_NAME_CHAT_ID = "chat_id"
    COLUMN_NAME_ENV_ID = "env_id"

    SQL_CREATE_ENTRIES = f"""
    CREATE TABLE {TABLE_NAME} (
            {COLUMN_NAME_CHAT_ID} INTEGER,
            {COLUMN_NAME_ENV_ID} INTEGER,
            CONSTRAINT prim_eky PRIMARY KEY ({COLUMN_NAME_CHAT_ID}, {COLUMN_NAME_ENV_ID})
            CONSTRAINT fk_chat FOREIGN KEY ({COLUMN_NAME_CHAT_ID}) REFERENCES {ChatContract.TABLE_NAME} (_ID)
            CONSTRAINT fk_env FOREIGN KEY ({COLUMN_NAME_ENV_ID}) REFERENCES {EnviableContract.TABLE_NAME} (_ID)
    )"""
    
    SQL_DELETE_ENTRIES = f"DROP TABLE IF EXISTS {TABLE_NAME}"

class OpcionesContract(Contract):
    TABLE_NAME = "Opciones"
    COLUMN_NAME_ALIAS = "alias"
    COLUMN_NAME_ID = "id"

    SQL_CREATE_ENTRIES = f"""
        CREATE TABLE {TABLE_NAME} (
            _ID INTEGER PRIMARY KEY,
            {COLUMN_NAME_ALIAS} TEXT,
            {COLUMN_NAME_ID} TEXT,
        )"""
    
    SQL_DELETE_ENTRIES = f"DROP TABLE IF EXISTS {TABLE_NAME}"

class UsuarioContract(Contract):
    TABLE_NAME = "Usuarios"
    COLUMN_NAME_ALIAS = "alias"
    COLUMN_NAME_ID = "id"
    COLUMN_NAME_CHAT_ID = "chat_id"

    SQL_CREATE_ENTRIES = f"""
        CREATE TABLE {TABLE_NAME} (
            _ID INTEGER PRIMARY KEY,
            {COLUMN_NAME_ALIAS} TEXT,
            {COLUMN_NAME_ID} TEXT
            {COLUMN_NAME_CHAT_ID} INTEGER
            CONSTRAINT fk_chat FOREIGN KEY ({COLUMN_NAME_CHAT_ID}) REFERENCES {ChatContract.TABLE_NAME} (_ID)
        )"""
    
    SQL_DELETE_ENTRIES = f"DROP TABLE IF EXISTS ${TABLE_NAME}"

class WhiteListContract(Contract):
    TABLE_NAME = "Whitelist"
    COLUMN_NAME_USR_ID = "usr_id"

    SQL_CREATE_ENTRIES = f"""
        CREATE TABLE {TABLE_NAME} (
            _ID INTEGER PRIMARY KEY,
            {COLUMN_NAME_USR_ID} TEXT,
            CONSTRAINT fk_user FOREIGN KEY ({COLUMN_NAME_USR_ID}) REFERENCES {UsuarioContract.TABLE_NAME} (_ID)
        )"""
    
    SQL_DELETE_ENTRIES = f"DROP TABLE IF EXISTS {TABLE_NAME}"
