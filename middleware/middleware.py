import socket
from middleware import COMMAND_SIZE, INT_SIZE, ADD_OP, SYM_OP, SUB_OP, BYE_OP
from typing import Self
import json

class Socket:


    def __init__(self,connection, address, port):
        self.connection = connection
        self.address = address
        self.port = port


    def accept(self) -> Self:
        new_socket, (new_address, new_port) = self.connection.accept()
        print("Client " + str(new_address) +" "+ str(new_port) + " just connected")
        return Socket(new_socket,new_address, new_port )

    def get_address(self):
        return self.address

    def get_port(self):
        return self.port


    # ----- enviar e receber strings ----- #
    def receive_str(self, n_bytes:int) -> str:
        """
        :param n_bytes: The number of bytes to read from the current connection
        :return: The next string read from the current connection
        """
        data = self.connection.recv(n_bytes)
        return data.decode()

    def send_str(self,value: str) -> None:
        self.connection.send(value.encode())

    def send_int(self, value: int, n_bytes:int) -> None:
        self.connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_int(self, n_bytes:int) -> int:
        data = self.connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def send_object(self, obj: any) -> None:
        """
        :param obj: The list of strings to be sent
        :return: None
        """

        data = json.dumps(obj).encode()
        length = len(data)
        self.send_int(length, 4)
        self.connection.send(data)

    def receive_object(self) -> int:
        """
        :param n_bytes: The number of bytes to read from the current connection
        :return: The deserialized list of strings
        """
        length = self.receive_int(4)
        data = self.connection.recv(length)
        return json.loads(data.decode())

    def close(self):
        self.connection.close()

    def settimeout(self, t:int):
        self.connection.settimeout(t)


    @staticmethod
    def start_socket_client(address,port) -> object:
        #Socket & ligação
        connection = socket.socket()
        connection.connect((address,port))
        _socket = Socket(connection, address, port)
        return _socket

    @staticmethod
    def start_socket_server(address,port, blocking) -> object:
        connection = socket.socket()
        connection.bind(('', port))
        # blocking
        if blocking == True:
            connection.setblocking(False)
        connection.listen(1)
        _socket = Socket(connection, address, port)
        return _socket