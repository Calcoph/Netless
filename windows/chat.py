from __future__ import annotations

import time
import tkinter as tk
from tkinter import scrolledtext, filedialog
import socket
import threading

from .comunicacion import Comunicacion, TipoMensaje
from .modelo.enviables import Fichero, Dirección
from .modelo.whitelist import Whitelist
from .modelo.usuarios import Usuario, ListaUsuarios
from .modelo.configuración import OpcionesUsuario

class Enum:
    pass

class Vistas(Enum):
    MENSAJES = 0
    USUARIOS = 1
    OPCIONES = 2

class GenericGUI(tk.Frame):
    def __init__(self, parent, row: int, column: int=0, padx: int=5, pady: int=5):
        super().__init__(parent)
        self.parent = parent
        self.row = row
        self.column = column
        self.padx = padx
        self.pady = pady
    
    def show(self):
        self.grid(row=self.row, column=self.column, padx=self.padx, pady=self.pady)

    def hide(self):
        self.grid_forget()
    
    def destroy_children(self) -> GenericGUI:
        self.hide()
        new_instance = GenericGUI(self.parent, self.row, self.column, self.padx, self.pady)
        new_instance.show()
        return new_instance

class GUIOpciones(GenericGUI):
    def __init__(self, parent: MessageSenderApp):
        super().__init__(parent, row=2)
        self.label = tk.Label(self, text="Hello world (GUIOpciones)")
        self.label.grid(row=0, column=0, padx=5, pady=5)

        #Label y entradas alias
        self.label_alias = tk.Label(self, text=f"Alias: SI ESTÁS LEYENDO ESTO ALGO HA IDO MAL")
        self.label_alias.grid(row=1, column=0, padx=5, pady=5)
        self.entry_alias = tk.Entry(self, width=50)
        self.entry_alias.grid(row=1, column=1, padx=5, pady=5)
        self.button_alias = tk.Button(self, text="Cambiar alias", command=self.cambiar_alias)
        self.button_alias.grid(row=1, column=2, padx=5, pady=5)

        #Label y entradas id
        self.label_id = tk.Label(self, text=f"Id: SI ESTÁS LEYENDO ESTO ALGO HA IDO MAL")
        self.label_id.grid(row=2, column=0, padx=5, pady=5)
        self.button_id = tk.Button(self, text="Generar un nuevo id", command=self.cambiar_id)
        self.button_id.grid(row=2, column=1, padx=5, pady=5)

        self.mostrar_en_pantalla()

    def cambiar_alias(self):
        nuevo_alias = self.entry_alias.get()
        opciones = OpcionesUsuario.get_opciones()
        opciones.cambiar_alias(nuevo_alias)

        self.mostrar_en_pantalla()
    
    def cambiar_id(self):
        opciones = OpcionesUsuario.get_opciones()
        opciones.cambiar_id()

        self.mostrar_en_pantalla()
    
    def mostrar_en_pantalla(self):
        opciones = OpcionesUsuario.get_opciones()
        alias = opciones.get_alias()
        id = opciones.get_display_id()

        self.label_alias.config(text=f"Alias: {alias}")
        self.label_id.config(text=f"Id: {id}")

class GUIChat(GenericGUI):
    def __init__(self, parent: MessageSenderApp):
        super().__init__(parent, row=2)
        self.label = tk.Label(self, text="Hello world (GUIChat)")
        self.label.grid(row=0, column=0, padx=5, pady=5)
        self.label2 = tk.Label(self, text="ESTE MENSAJE NO DEBERÍA SER POSIBLE VERLO, ALGO HA SALIDO MAL (GUIChat)")
        self.label2.grid(row=1, column=0, padx=5, pady=5)
        self.usuario = None

        #Label y entradas Mensaje
        self.label_message = tk.Label(self, text="Mensaje:")
        self.label_message.grid(row=2, column=0, padx=5, pady=5)
        self.entry_message = tk.Entry(self, width=50)
        self.entry_message.grid(row=2, column=1, padx=5, pady=5)

        #Boton enviar mensaje
        self.button_send_message = tk.Button(self, text="Enviar mensaje", command=self.send_message)
        self.button_send_message.grid(row=3, column=1, padx=5, pady=5)
        #Boton enviar archivo
        self.button_send_file = tk.Button(self, text="Enviar archivo", command=self.send_file)
        self.button_send_file.grid(row=3, column=0, padx=5, pady=5)

        #area de texto
        self.text_area = scrolledtext.ScrolledText(self, width=60, height=10)
        self.text_area.grid(row=4, columnspan=2, padx=5, pady=5)

        self.receiver_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receiver_thread.start()
    
    def abrir_chat(self, usuario: Usuario):
        self.usuario = usuario
        acepta_conexiones = self.usuario.acepta_conexiones()
        nombre = self.usuario.obtener_nombre()
        chat = self.usuario.obtener_chat()
        chat.mostrar_en_pantalla()
        if True:#acepta_conexiones:
            self.activar_envio()
        else:
            self.desactivar_envio()
            self.usuario.solicitar_conexion()
        self.label2.grid_forget()
        self.label2 = tk.Label(self, text=f"chateando con {usuario.nombre}")
        self.label2.grid(row=1, column=0, padx=5, pady=5)

        self.show()

    def activar_envio(self):
        self.button_send_message["state"] = "normal"
        self.button_send_file["state"] = "normal"
    
    def desactivar_envio(self):
        self.button_send_message["state"] = "disabled"
        self.button_send_file["state"] = "disabled"

    #al pulsar el botón enviar mensaje se ejecuta esta función
    def send_message(self):
        #de los textos de entrada obtenemos la dirección y el mensaje
        destination_ip = self.usuario.ip
        message = self.entry_message.get()
        #se cofigura un socket para el envío
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((destination_ip, 12345))
            s.sendall(f"TEXT\n{message}".encode('utf-8'))
            s.close()
            #se añade un mensaje en el área de texto
            self.text_area.insert(tk.END, f"[You] {message}\n")
        except Exception as e:
            print(f"An error occurred while sending message: {str(e)}")
        
    def enviar_fichero(self):
        fichero = self.seleccionar_fichero()
        nombre = fichero.obtener_nombre()
        tamaño = fichero.obtener_tamaño()

        self.usuario.obtener_confirmacion(nombre, tamaño)
        fichero = Fichero(nombre, tamaño, Dirección.Saliente)
        self.usuario.enviar_fichero(fichero)
    
    def seleccionar_fichero(self):# -> File:
        raise NotImplementedError

    def enviar_mensaje(self):
        mensaje = self.entry_message.get()
        self.usuario.enviar_mensaje(mensaje)

    def eliminar_de_whitelist(self):
        id = self.usuario.obtener_id()
        wl = Whitelist.get_whitelist()
        wl.quitar_usuario(id)

    #al pulsar el botón enviar archivo se ejecuta esta función
    def send_file(self):
        destination_ip = self.usuario.ip
        #a diferencia de send_message el archivo se obtiene de una ventana emergente
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    file_content = file.read()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((destination_ip, 12345))  # se lee el archivo y se envía por el socket
                s.sendall(f"FILE\n{file_path.split('/')[-1]}".encode('utf-8'))
                s.sendall(file_content)
                s.close()
                self.text_area.insert(tk.END, f"[You] Sent file: {file_path}\n")
            except Exception as e:
                print(f"An error occurred while sending file: {str(e)}")
    
    def receive_messages(self,):
        """s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', 12345)) 
        s.listen(1)

        while True:
            conn, addr = s.accept()
            
            with conn:

                #se selecciona el tipo a recibir
                data = conn.recv(1024)
                message_type, *rest = data.decode('utf-8').split('\n')

                if message_type == 'TEXT':
                        message = '\n'.join(rest)
                        self.text_area.insert(tk.END, f"[{addr[0]}] {message}\n")

                elif message_type == 'FILE':
                        file_name = rest[0]
                        print(file_name)
                        with open(file_name, 'wb') as file:
                            while True:
                                data = conn.recv(1024)
                                if not data:
                                    break
                                file.write(data)
                                file.write(conn.recv(1024))
                        self.text_area.insert(tk.END, f"[{addr[0]}] Received file: {file_name}\n")
                        break
"""


        """"
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    print(data)
                    if not data:
                        break
                    message_type, *rest = data.decode('utf-8').split('\n')
                    if message_type == 'TEXT':
                        message = '\n'.join(rest)
                        
                        self.text_area.insert(tk.END, f"[{addr[0]}] {message}\n")
                    elif message_type == 'FILE':
                        file_name = rest[0]
                        with open(file_name, 'wb') as file:
                            while True:
                                data = conn.recv(1024)
                                if not data:
                                    break
                                file.write(data)
                                file.write(conn.recv(1024))
                        self.text_area.insert(tk.END, f"[{addr[0]}] Received file: {file_name}\n")
                        break
                        """
        
class GUIPrincipal(GenericGUI):
    def __init__(self, parent: MessageSenderApp):
        super().__init__(parent, row=1)
        self.parent = parent
        self.label = tk.Label(self, text="Hello world (GUIPrincipal)")
        self.label.grid(row=0, column=0, padx=5, pady=5)

        self.button_opciones = tk.Button(self, text="Opciones", command=self.parent.abrir_opciones)
        self.button_opciones.grid(row=1, column=0, padx=5, pady=5)

        self.button_escanear_lan = tk.Button(self, text="Escanear Lan", command=self.scan_lan)
        self.button_escanear_lan.grid(row=2, column=0, padx=5, pady=5)

        self.usuarios = GenericGUI(self, row=3)
        self.usuarios.show()
        self.actualizar_usuarios_disponibles()

    def scan_lan(self):
        Comunicacion.get_com().discover()

    def aceptar_usuario(self, id_usuario: str):
        Whitelist.añadir_usuario(id_usuario)
    
    def actualizar_usuarios_disponibles(self):
        self.usuarios = self.usuarios.destroy_children()

        usuarios = ListaUsuarios.get_lista()
        for (row, usuario) in enumerate(usuarios.usuarios_disponibles()):
            usuario_button = tk.Button(self.usuarios, text=usuario.ip, command=lambda x=usuario.id: self.parent.abrir_chat(x))
            usuario_button.id_usuario = usuario.id
            usuario_button.grid(row=row, column=0, padx=5, pady=5)

            if usuario.estado.get_solicitando_whitelist():
                solicitando_whitelist_text = tk.Label(self.usuarios, text="Solicitando conexión")
                solicitando_whitelist_text.grid(row=row, column=1, padx=5, pady=5)

    def conexion_solicitada(self, id_usuario: str):
        self.actualizar_usuarios_disponibles()

class MessageSenderApp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack()
        self.root = root
        self.root.title("Netless")

        self.back_button = tk.Button(self, text="Volver a lista de usuarios", command=self.volver_a_gui_principal)
        self.vista_seleccionada = Vistas.USUARIOS

        self.gui_principal = GUIPrincipal(self)
        self.gui_principal.show()

        self.gui_chat = GUIChat(self)
        self.gui_opciones = GUIOpciones(self)

        comunicaciones = threading.Thread(target=self.leer_comunicaciones, daemon=True)
        comunicaciones.start()

        autoscan = threading.Thread(target=self.auto_scan, daemon=True)
        autoscan.start()

    def abrir_chat(self, id_usuario: str):
        usuarios = ListaUsuarios.get_lista()
        usuario = usuarios.obtener_usuario(id_usuario)
        self.gui_principal.hide()
        self.gui_chat.abrir_chat(usuario)
        self.vista_seleccionada = Vistas.MENSAJES

        self.back_button.grid(row=1, column=0, padx=5, pady=5)
    
    def volver_a_gui_principal(self):
        self.vista_seleccionada = Vistas.USUARIOS
        self.back_button.grid_forget()
        self.gui_chat.hide()
        self.gui_opciones.hide()
        self.gui_principal.show()
    
    def abrir_opciones(self):
        self.gui_principal.hide()
        self.vista_seleccionada = Vistas.OPCIONES

        self.back_button.grid(row=1, column=0, padx=5, pady=5)
        self.gui_opciones.show()

    def leer_comunicaciones(self):
        comunicaciones = Comunicacion.get_com()
        usuarios = ListaUsuarios.get_lista()

        while True:
            (tipo, direccion), mensaje = comunicaciones.rx.get()
            print(type(direccion))
            print(f"recibido {direccion}")

            if tipo == TipoMensaje.IDENTIFICACION:
                usuarios.identificar(mensaje, direccion)
                self.gui_principal.actualizar_usuarios_disponibles()
            elif tipo == TipoMensaje.PEDIR_IDENTIFICACION:
                Comunicacion.identificarse(direccion)
            elif tipo == TipoMensaje.SOLICITAR_CONEXION:
                print("Se ha solicitado una conexión")
                usuario = usuarios.usuario_ip(direccion)
                usuario.estado.set_solicitando_whitelist(True)
                id_usuario = usuario.id
                self.gui_principal.conexion_solicitada(id_usuario)
    
    def auto_scan(self):
        Comunicacion.get_com().discover()
        while True:
            time.sleep(150) # 2.5 minutos
            Comunicacion.get_com().discover()

def iniciar():
    root = tk.Tk()
    app = MessageSenderApp(root)
    root.mainloop()
