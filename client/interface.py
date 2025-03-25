import socket
import json

class Interface:
    def __init__(self, address, port):
        # Socket & ligação
        self.connection = socket.socket()
        self.connection.connect((address, port))

    def receive_str(self,connect, n_bytes: int) -> str:
        """
        :param n_bytes: The number of bytes to read from the current connection
        :return: The next string read from the current connection
        """
        data = connect.recv(n_bytes)
        return data.decode()

    def send_str(self,connect, value: str) -> None:
        connect.send(value.encode())

    def send_int(self,connect:socket.socket, value: int, n_bytes: int) -> None:
        connect.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_int(self,connect: socket.socket, n_bytes: int) -> int:
        data = connect.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def send_obj(self,connection,value: object, n_bytes:int)-> None:
        """
        :param value:
        :param n_bytes:
        :return:
        """
        msg = json.dumps(value)
        size = len(msg)
        self.send_int(connection,size, n_bytes)
        self.send_str(connection,msg)

    def receive_obj(self, connection, n_bytes: int) -> object:
        """
        :param n_bytes:
        :return:
        """
        size  = self.receive_int(connection,n_bytes)
        obj =  self.receive_str(connection,size)
        return json.loads(obj)
