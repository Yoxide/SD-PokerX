import threading

class Contador:
    def __init__(self):
        self.lock = threading.Lock()  # Ensure thread-safe access to the client count
        self.count = 0

    def incrementa(self):
        with self.lock:
            self.count += 1

    def decrementa(self):
        with self.lock:
            self.count -= 1

    def retorna_contagem(self):
        with self.lock:
            return self.count
