import threading
import json
import data_structure
import pygame
class ThreadCliente(threading.Thread):

    def __init__(self,connection, address):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.data_structure = data_structure.Data_Structure()

        # ---------------------- interaction with sockets ------------------------------
        def receive_int(self, connection, n_bytes: int) -> int:
            """
            :param n_bytes: The number of bytes to read from the current connection
            :return: The next integer read from the current connection
            """
            data = connection.recv(n_bytes)
            return int.from_bytes(data, byteorder='big', signed=True)

        def send_int(self, connection, value: int, n_bytes: int) -> None:
            """
            :param value: The integer value to be sent to the current connection
            :param n_bytes: The number of bytes to send
            """
            connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

        def receive_str(self, connection, n_bytes: int) -> str:
            """
            :param n_bytes: The number of bytes to read from the current connection
            :return: The next string read from the current connection
            """
            data = connection.recv(n_bytes)
            return data.decode()

        def send_str(self, connection, value: str) -> None:
            """
            :param value: The string value to send to the current connection
            """
            connection.current_connection.send(value.encode())

        def send_obj(self, connection, value: object, n_bytes: int) -> None:
            """
            :param value:
            :param n_bytes:
            :return:
            """
            msg = json.dumps(value)
            size = len(msg)
            self.send_int(connection, size, n_bytes)
            self.send_str(connection, msg)

        def receive_obj(self, connection, n_bytes: int) -> object:
            """
            :param n_bytes:
            :return:
            """
            size = self.receive_int(connection, n_bytes)
            obj = self.receive_str(connection, size)
            return json.loads(obj)

        def run(self):
            pygame.init()

            WIDTH, HEIGHT = 800, 600
            GREEN = (34, 139, 34)
            CARD_WIDTH, CARD_HEIGHT = 100, 150

            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Texas Hold'em Poker")
            last_request = False
            # Recebe messagens...
            while not last_request:
                return None # temporário
