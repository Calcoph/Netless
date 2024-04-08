import tkinter as tk
from tkinter import scrolledtext, filedialog
import socket
import threading
from .modelo.usuarios import Usuario, ListaUsuarios
from .modelo.whitelist import Whitelist
from .modelo.configuración import OpcionesUsuario
from .modelo.enviables import Fichero, Dirección

# No sólo importa discover, si no que además inicializa el descubrimiento
from .discover import discover
#se obtiene la IP del equipo y se busca en el /24 de esa dirección

class Enum:
    pass

class Vistas(Enum):
    MENSAJES = 0
    USUARIOS = 1
    OPCIONES = 2

class GUIOpciones(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = tk.Label(self, text="Hello world (GUIOpciones)")
        self.label.grid(row=0, column=0, padx=5, pady=5)

        #Label y entradas alias
        self.label_alias = tk.Label(self, text="Alias:")
        self.label_alias.grid(row=1, column=0, padx=5, pady=5)
        self.entry_alias = tk.Entry(self, width=50)
        self.entry_alias.grid(row=1, column=1, padx=5, pady=5)

        #Label y entradas id
        self.label_id = tk.Label(self, text="Id:")
        self.label_id.grid(row=2, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(self, width=50)
        self.entry_id.grid(row=2, column=1, padx=5, pady=5)

    def cambiar_alias(self):
        nuevo_alias = self.entry_alias.get()
        self.mostrar_en_pantalla()
        opciones = OpcionesUsuario.get_opciones()
        opciones.cambiar_alias(nuevo_alias)
    
    def cambiar_id(self):
        nuevo_id = self.entry_id.get()
        self.mostrar_en_pantalla()
        opciones = OpcionesUsuario.get_opciones()
        opciones.cambiar_id(nuevo_id)
    
    def mostrar_en_pantalla(self):
        pass

class GUIChat(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
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
    
    def abrir_chat(self, id_usuario: str):
        usuarios = ListaUsuarios.get_lista()
        usuario = usuarios.obtener_usuario(id_usuario)
        self.usuario = usuario
        acepta_conexiones = self.usuario.acepta_conexiones()
        nombre = self.usuario.obtener_nombre()
        chat = self.usuario.obtener_chat()
        chat.mostrar_en_pantalla()
        if acepta_conexiones:
            self.activar_envio()
        else:
            self.desactivar_envio()
            acepta_conexiones = self.usuario.solicitar_conexion()
            if acepta_conexiones:
                self.activar_envio()
        self.label2.grid_forget()
        self.label2 = tk.Label(self, text=f"chateando con {usuario.nombre}")
        self.label2.grid(row=1, column=0, padx=5, pady=5)
    
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
    
    def seleccionar_fichero(self) -> File:
        raise NotImplementedError

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

class GUIPrincipal(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.label = tk.Label(self, text="Hello world (GUIPrincipal)")
        self.label.grid(row=0, column=0, padx=5, pady=5)

        self.button_send_message = tk.Button(self, text="Escanear Lan", command=self.scan_lan)
        self.button_send_message.grid(row=1, column=0, padx=5, pady=5)

        self.usuarios = tk.Frame(self)
        self.usuarios.grid(row=2, column=0, padx=5, pady=5)
        usuarios = ListaUsuarios.get_lista()
        for (row, usuario) in enumerate(usuarios.usuarios):
            usuario_button = tk.Button(self.usuarios, text=usuario.nombre, command=lambda x=usuario.id: parent.abrir_chat(x))
            usuario_button.grid(row=row, column=0, padx=5, pady=5)
    
    def scan_lan(self):
        self.usuarios.grid_forget()
        self.usuarios = tk.Frame(self)
        self.usuarios.grid(row=2, column=0, padx=5, pady=5)

        usuarios = ListaUsuarios.get_lista()
        usuarios.scan_lan()
        for (row, usuario) in enumerate(usuarios.usuarios):
            usuario_button = tk.Button(self.usuarios, text=usuario.nombre, command=lambda x=usuario.id: self.parent.abrir_chat(x))
            usuario_button.grid(row=row, column=0, padx=5, pady=5)
    
    def aceptar_usuario(self, id_usuario: str):
        Whitelist.añadir_usuario(id_usuario)

class MessageSenderApp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack()
        self.root = root
        self.root.title("Netless")

        self.back_button = tk.Button(self, text="Volver a lista de usuarios", command=self.volver_a_lista_usuarios)
        self.vista_seleccionada = Vistas.USUARIOS
        self.gui_principal = GUIPrincipal(self)
        self.gui_principal.grid(row=7, column=0, padx=5, pady=5)

        self.gui_chat = GUIChat(self)

        #hilo de receptor
        self.receiver_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receiver_thread.start()

    def abrir_chat(self, id_usuario: str):
        self.gui_principal.grid_forget()
        self.gui_chat.abrir_chat(id_usuario)
        self.vista_seleccionada = Vistas.MENSAJES

        self.back_button.grid(row=6, column=0, padx=5, pady=5)
        self.gui_chat.grid(row=7, column=0, padx=5, pady=5)
    
    def volver_a_lista_usuarios(self):
        self.vista_seleccionada = Vistas.USUARIOS
        self.back_button.grid_forget()
        self.gui_chat.grid_forget()
        self.gui_principal.grid(row=7,column=0,padx=5,pady=5)
    
    def receive_messages(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', 12345)) 
        s.listen(1)

        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message_type, *rest = data.decode('utf-8').split('\n')

                    if message_type == 'TEXT':
                        message = '\n'.join(rest)
                        self.text_area.insert(tk.END, f"[{addr[0]}] {message}\n")
                    elif message_type == 'FILE':
                        file_name = rest[0]
                        with open(file_name, 'wb') as file:
                            file.write(conn.recv(1024))
                        self.text_area.insert(tk.END, f"[{addr[0]}] Received file: {file_name}\n")
                        break

def iniciar():
    root = tk.Tk()
    app = MessageSenderApp(root)
    root.mainloop()
