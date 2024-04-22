from __future__ import annotations

from .database import DbHelper
from .database.contracts import FicheroContract, EnviableContract, MensajeContract, UsuarioContract, ChatContract, EnviablesChatContract
from .enviables import Enviable, Fichero, Mensaje, Dirección
from ..comunicacion import Identificacion
import time

class HistorialChat:
    def __init__(self) -> None:
        self.lista_enviables: list[Enviable] = []

    def añadir_fichero(self, fichero: Fichero, id_usuario: str):
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
        self.añadir_enviable(fichero, env_id, id_usuario)

    def añadir_mensaje(self, mens: Mensaje, id_usuario: str):
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

        self.añadir_enviable(mens, env_id, id_usuario)

    def añadir_enviable(self, enviable: Enviable, env_id: int, id_usuario: str):
        self.lista_enviables.append(enviable)
        self.mostar_en_pantalla()

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
    
    def mostrar_en_pantalla(self):
        for enviable in self.lista_enviables:
            enviable.mostrar_en_pantalla()

TIEMPO_DESCONEXION = 300.0 # 5 minutos

class ListaUsuarios:
    LISTA: ListaUsuarios = None
    def __init__(self) -> None:
        if ListaUsuarios.LISTA is None:
            ListaUsuarios.LISTA = self
            self.usuarios: list[Usuario] = []
        else:
            raise SystemError

    def get_lista() -> ListaUsuarios:
        if ListaUsuarios.LISTA is None:
            ListaUsuarios()
        return ListaUsuarios.LISTA
    
    def añadir_usuario(self, usr: Usuario):
        self.usuarios.append(usr)
    
    def quitar_usuario(self, id: str):
        remove_index = None
        for (index, usuario) in enumerate(self.usuarios):
            if usuario.id == id:
                remove_index = index
                break
        if remove_index is not None:
            self.usuarios.pop(remove_index)
    
    def obtener_usuario(self, id: str) -> Usuario | None:
        for usuario in self.usuarios:
            if usuario.id == id:
                return usuario
        return None

    def identificar(self, mensaje: Identificacion, ip):
        id = mensaje.id
        alias = mensaje.alias
        usuario_registrado = self.obtener_usuario(id)

        if usuario_registrado is None:
            usuario = Usuario(alias, ip, id)
            self.usuarios.append(usuario)
            usuario_registrado = usuario

        usuario_registrado.ultima_vez_visto = time.time()
        usuario_registrado.estado.set_disponible(True)
    
    def usuarios_disponibles(self) -> list[Usuario]:
        usuarios_disponibles = []
        tiempo_actual = time.time()

        for usuario in self.usuarios:
            if usuario.estado.get_disponible():
                dt = tiempo_actual - usuario.ultima_vez_visto
                if dt < TIEMPO_DESCONEXION:
                    usuarios_disponibles.append(usuario)
                else:
                    usuario.estado.set_disponible(False)

        return usuarios_disponibles

class Flags:
    pass

class Estado(Flags):
    DISPONIBLE            = 0b00000001
    EN_WHITELIST          = 0b00000010
    SOLICITANDO_WHITELIST = 0b00000100

    def __init__(self) -> None:
        self.estado = 0
    
    def get_disponible(self) -> bool:
        return self.estado & Estado.DISPONIBLE > 0

    def set_disponible(self, disponible: bool):
        if disponible:
            self.estado = self.estado | Estado.DISPONIBLE
        else:
            self.estado = self.estado & (~Estado.DISPONIBLE)
    
    def get_en_whitelist(self) -> bool:
        return self.estado & Estado.EN_WHITELIST > 0

    def set_en_whitelist(self, en: bool) -> bool:
        if en:
            self.estado = self.estado | Estado.EN_WHITELIST
        else:
            self.estado = self.estado & (~Estado.EN_WHITELIST)

    def get_solicitando_whitelist(self) -> bool:
        return self.estado & Estado.SOLICITANDO_WHITELIST > 0

    def set_solicitando_whitelist(self, sol: bool) -> bool:
        if bool:
            self.estado = self.estado | Estado.SOLICITANDO_WHITELIST
        else:
            self.estado = self.estado & (~Estado.SOLICITANDO_WHITELIST)

class Usuario:
    def __init__(self, nombre: str, ip: str, id: str) -> None:
        self.nombre = nombre
        self.ip = ip
        self.chat = HistorialChat()
        self.id = id
        self.estado = Estado()
        self.ultima_vez_visto = 0.0
    
    def obtener_confirmacion(nombre: str, tamaño: int):
        pass

    def enviar_fichero(self, fichero: File):
        nombre = fichero.name
        tamaño = fichero.totalSpace
        fichero = Fichero(nombre, tamaño, Dirección(Dirección.Saliente))
        self.chat.añadir_fichero(fichero, id)

    def enviar_mensaje(self, msg: str):
        mens = Mensaje(msg, Dirección.Saliente)
        self.chat.añadir_mensaje(mens)
    
    def obtener_nombre(self) -> str:
        return self.nombre
    
    def obtener_chat(self) -> HistorialChat:
        return self.chat
    
    def obtener_id(self) -> str:
        return self.id
    
    def acepta_conexiones(self) -> bool:
        print("ERROR: acepta_conexiones no está implementado y devuelve siempre True")
        return True
    
    def solicitar_conexion(self) -> bool:
        print("ERROR: solicitar_conexion no está implementado y devuelve siempre True")
        return True
