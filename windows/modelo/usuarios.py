from __future__ import annotations
from .database import DbHelper
from .database.contracts import FicheroContract, EnviableContract, MensajeContract, UsuarioContract, ChatContract, EnviablesChatContract
from .enviables import Enviable, Fichero, Mensaje, Dirección
from ..discover import discover

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

class ListaUsuarios:
    LISTA: ListaUsuarios = None
    def __init__(self) -> None:
        if ListaUsuarios.LISTA is None:
            self.usuarios: list[Usuario] = []
            self.counter = 0
            self.LISTA = self
            self.scan_lan()
        else:
            raise SystemError

    def get_lista() -> ListaUsuarios:
        if ListaUsuarios.LISTA is None:
            ListaUsuarios.LISTA = ListaUsuarios()
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
    
    def scan_lan(self):
        usuarios_disponibles = []
        direcciones = discover()
        # Añade los usuarios nuevos descubiertos
        for direccion in direcciones:
            id = direccion.mac
            usuario_registrado = self.obtener_usuario(id)
            if usuario_registrado is None:
                usuario = Usuario(str(self.counter), direccion.ip, direccion.mac)
                self.usuarios.append(usuario)
                self.counter += 1
                usuarios_disponibles.append(id)
            else:
                usuarios_disponibles.append(usuario_registrado.id)
        
        # Elimina los usuarios antiguos que no han respondido (ya no están disponibles)
        indices_a_eliminar = []
        for (i, usuario) in enumerate(self.usuarios):
            if usuario.id not in usuarios_disponibles:
                indices_a_eliminar.append(i)
        # Se eliminan desde el final hacia el inicio para conservar los índices
        indices_a_eliminar.reverse()
        for i in indices_a_eliminar:
            self.usuarios.pop(i)

class Usuario:
    def __init__(self, nombre: str, ip: str, id: str) -> None:
        self.nombre = nombre
        self.ip = ip
        self.chat = HistorialChat()
        self.id = id
    
    def obtener_confirmacion(nombre: str, tamaño: int):
        pass

    def enviar_fichero(self, fichero: File):
        nombre = fichero.name
        tamaño = fichero.totalSpace
        fichero = Fichero(nombre, tamaño, Dirección(Dirección.Saliente))
        self.chat.añadir_fichero(fichero, id)
    
    def obtener_nombre(self) -> str:
        return self.nombre
    
    def obtener_chat(self) -> HistorialChat:
        return self.chat
    
    def obtener_id(self) -> str:
        return self.id
    
    def acepta_conexiones(self) -> bool:
        raise NotImplementedError
    
    def solicitar_conexion(self) -> bool:
        raise NotImplementedError
