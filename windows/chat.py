import tkinter as tk
from tkinter import scrolledtext, filedialog
import socket
import threading

# No sólo importa discover, si no que además inicializa el descubrimiento
import discover


class MessageSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Netless")

        #Label y entradas IP destino
        self.label_to = tk.Label(root, text="IP destino:")
        self.label_to.grid(row=0, column=0, padx=5, pady=5)
        self.entry_to = tk.Entry(root, width=50)
        self.entry_to.grid(row=0, column=1, padx=5, pady=5)
        #Label y entradas Mensaje
        self.label_message = tk.Label(root, text="Mensaje:")
        self.label_message.grid(row=1, column=0, padx=5, pady=5)
        self.entry_message = tk.Entry(root, width=50)
        self.entry_message.grid(row=1, column=1, padx=5, pady=5)
        ###################################################################################################
        #boton de  de las redes disponibles
        self.button_send_message = tk.Button(root, text="Escanear Lan", command=self.scan_lan)
        self.button_send_message.grid(row=2, column=0, padx=5, pady=5)
        ###################################################################################################

        #Boton enviar mensaje
        self.button_send_message = tk.Button(root, text="Enviar mensaje", command=self.send_message)
        self.button_send_message.grid(row=3, column=1, padx=5, pady=5)
        #Boton enviar archivo
        self.button_send_file = tk.Button(root, text="Enviar archivo", command=self.send_file)
        self.button_send_file.grid(row=3, column=0, padx=5, pady=5)

        ###################################################################################################
        #hacer label y entradas de las direcciones que se encuentran
        #primero averiguar cuántas hay
        #segundo label
        #tercero botones

        ####################################################################################################

        #area de texto
        self.text_area = scrolledtext.ScrolledText(root, width=60, height=10)
        self.text_area.grid(row=4, columnspan=2, padx=5, pady=5)

        #area de texto para direcciones
        #self.directions_area = scrolledtext.ScrolledText(root, width=60, height=10)
        #self.directions_area.grid(row=4, columnspan=1, padx=5, pady=5)


        #hilo de receptor
        self.receiver_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receiver_thread.start()


    def scan_lan(self):
        devices = discover.discover()
        self.text_area.insert(tk.END, f"Imprimiento Direcciones:\n")
        for device in devices:
            #imprimimos por pantalla los dispositivos
            self.text_area.insert(tk.END, f"IP: {device['ip']}, MAC: {device['mac']}\n")
        self.text_area.insert(tk.END, f"Fin Direcciones\n")


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
                s.sendall(f"FILE\n{file_path.split('/')[-1]}".encode('utf-8'))
                s.sendall(file_content)
                s.close()
                self.text_area.insert(tk.END, f"[You] Sent file: {file_path}\n")
            except Exception as e:
                print(f"An error occurred while sending file: {str(e)}")


#opcione de recibir mensaje alternativa, falta solucionar la recepcion de ficheros (mejor formato binario)
"""""
    def receive_messages(self):
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.bind(('0.0.0.0', 12345)) 
        #s.listen(1)
        
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                if data.startswith(b"file|"):
                    file_info, file_data = data.split(b'\n', 1)
                    file_name, file_size = file_info.decode().split('|')[1:]
                    file_name = file_name.strip()
                    file_size = int(file_size.strip())
                    received_data = file_data
                    while len(received_data) < file_size:
                        chunk = self.socket.recv(min(1024, file_size - len(received_data)))
                        if not chunk:
                            break
                        received_data += chunk
                    with open(file_name, 'wb') as file:
                        file.write(received_data)
                    messagebox.showinfo("File Received", f"File '{file_name}' received successfully.")
                else:
                    message = data.decode()
                    self.text_area.insert(tk.END, f"{message}\n")
            except ConnectionResetError:
                break
"""""
    

if __name__ == "__main__":
    root = tk.Tk()
    app = MessageSenderApp(root)
    root.mainloop()
