import tkinter as tk
from tkinter import scrolledtext, filedialog
import socket
import threading
from .modelo.usuarios import Usuario, ListaUsuarios

# No sólo importa discover, si no que además inicializa el descubrimiento
from .discover import discover
#se obtiene la IP del equipo y se busca en el /24 de esa dirección

class Enum:
    pass

class Vistas(Enum):
    MENSAJES = 0
    USUARIOS = 1

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
    
    def cambiar_usuario(self, usuario: Usuario):
        self.usuario = usuario
        self.label2.grid_forget()
        self.label2 = tk.Label(self, text=f"chateando con {usuario.nombre}")
        self.label2.grid(row=1, column=0, padx=5, pady=5)
    
    #al pulsar el botón enviar mensaje se ejecuta esta función
    def send_message(self):
        #de los textos de entrada obtenemos la dirección y el mensaje
        destination_ip = self.entry_to.get()
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

    #al pulsar el botón enviar archivo se ejecuta esta función
    def send_file(self):
        destination_ip = self.entry_to.get()
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
            usuario_button = tk.Button(self.usuarios, text=usuario.nombre, command=lambda x=usuario.id: parent.seleccionar_usuario(x))
            usuario_button.grid(row=row, column=0, padx=5, pady=5)
    
    def scan_lan(self):
        self.usuarios.grid_forget()
        self.usuarios = tk.Frame(self)
        self.usuarios.grid(row=2, column=0, padx=5, pady=5)

        usuarios = ListaUsuarios.get_lista()
        usuarios.scan_lan()
        for (row, usuario) in enumerate(usuarios.usuarios):
            usuario_button = tk.Button(self.usuarios, text=usuario.nombre, command=lambda x=usuario.id: self.parent.seleccionar_usuario(x))
            usuario_button.grid(row=row, column=0, padx=5, pady=5)

class MessageSenderApp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack()
        self.root = root
        self.root.title("Netless")

        self.back_button = tk.Button(self, text="Volver a lista de usuarios", command=self.volver_a_lista_usuarios)
        self.vista_seleccionada = Vistas.USUARIOS
        self.vista_lista_usuarios = GUIPrincipal(self)
        self.vista_lista_usuarios.grid(row=7, column=0, padx=5, pady=5)

        self.vista_mensajes = GUIChat(self)
        
        self.receiver_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receiver_thread.start()

    def seleccionar_usuario(self, id_usuario: str):
        self.vista_lista_usuarios.grid_forget()
        usuarios = ListaUsuarios.get_lista()
        usuario = usuarios.obtener_usuario(id_usuario)
        self.vista_mensajes.cambiar_usuario(usuario)
        self.vista_seleccionada = Vistas.MENSAJES

        self.back_button.grid(row=6, column=0, padx=5, pady=5)
        self.vista_mensajes.grid(row=7, column=0, padx=5, pady=5)
    
    def volver_a_lista_usuarios(self):
        self.vista_seleccionada = Vistas.USUARIOS
        self.back_button.grid_forget()
        self.vista_mensajes.grid_forget()
        self.vista_lista_usuarios.grid(row=7,column=0,padx=5,pady=5)
    
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

    #al pulsar el botón enviar archivo se ejecuta esta función
    def send_file(self):
        destination_ip = self.entry_to.get()
        #a diferencia de send_message el archivo se obtiene de una ventana emergente
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    file_content = file.read()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((destination_ip, 12345))  # se lee el archivo y se envía por el socket
                ##s.sendall(f"FILE\n{file_path.split('/')[-1]}".encode('utf-8'))
                file_name_bytes = file_path.split('/')[-1].encode('utf-8')
                s.sendall(b"FILE\n" + file_name_bytes)

                ##s.sendall(f"FILE\n{file_path.split('/')[-1]}")  #sin codificar
                ##s.sendall(file_content)
                s.close()
                self.text_area.insert(tk.END, f"[You] Sent file: {file_path}\n")
            except Exception as e:
                print(f"An error occurred while sending file: {str(e)}")

def iniciar():
    root = tk.Tk()
    app = MessageSenderApp(root)
    root.mainloop()
