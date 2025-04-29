import threading
import socket

class Clientes:
    def __init__(self):
        self.lock = threading.Lock()  # Ensure thread-safe access to the client count
        self.count = 0
        self.clientes = []
        self._first_connection = False

    def add_client(self, client:socket.socket):
        with self.lock:
            self.clientes.append(client)
            self.count += 1
            self._first_connection = True

    def first_connection(self):
        return self._first_connection

    def remove_client(self,client:socket.socket):
        with self.lock:
            self.clientes.remove(client)
            self.count -= 1

    def get_clients(self):
        with self.lock:
            return self.clientes

    def retorna_contagem(self):
        with self.lock:
            return self.count
