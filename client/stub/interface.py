#import socket
import middleware.middleware as middle
import client
import json

from client.stub import COMMAND_SIZE, INT_SIZE, HIT_OP, PAS_OP, FLD_OP, BYE_OP, LIST_SIZE


class Interface:
    def __init__(self, address, port):
        #Socket & ligação
        #self.connection = socket.socket()
        #self.connection.connect((address,port))
        self._socket = middle.Socket.start_socket_client(address,port)

    # def interface_soma(self)->tuple:
    #     res1 = int(input("Introduz o primeiro valor para somar:"))
    #     res2 = int(input("Introduz o segundo valor para somar:"))
    #     return (res1, res2)
    #
    # def interface_subtracao(self)->tuple:
    #     res1 = int(input("Introduz o primeiro valor para subtrair:"))
    #     res2 = int(input("Introduz o segundo valor para subtrair:"))
    #     return (res1, res2)

    def send_str(self,s: str):
        print("Sending str:",s)
        self._socket.send_str(s)

    def receive_str(self,n_bytes:int)-> str:
        return self._socket.receive_str(n_bytes)

    def send_int(self, i: int,n_bytes: int):
        self._socket.send_int(i,n_bytes)

    def receive_int(self,n_bytes: int) -> int:
        return self._socket.receive_int(n_bytes)

    def send_object(self, obj: any):
        # Convert the list to a JSON string
        return self._socket.send_object(obj)

    def receive_object(self):
        # Receive the string from the server
        return self._socket.receive_object()

        # Convert the string back into a list using JSON

    # ----- enviar e receber strings ----- #
    # def receive_str(self,connect, n_bytes: int) -> str:
    #     """
    #     :param n_bytes: The number of bytes to read from the current connection
    #     :return: The next string read from the current connection
    #     """
    #     data = connect.recv(n_bytes)
    #     return data.decode()
    #
    # def send_str(self,connect, value: str) -> None:
    #     connect.send(value.encode())
    #
    # def send_int(self,connect:socket.socket, value: int, n_bytes: int) -> None:
    #     connect.send(value.to_bytes(n_bytes, byteorder="big", signed=True))
    #
    # def receive_int(self,connect: socket.socket, n_bytes: int) -> int:
    #     data = connect.recv(n_bytes)
    #     return int.from_bytes(data, byteorder='big', signed=True)


    def bet(self, b_value: int) -> int:
        self.send_str(HIT_OP)
        self.send_int(b_value, INT_SIZE)
        res = self.receive_int(INT_SIZE)
        return res

    def cards_received(self):
        received_cards = self.receive_object()
        return received_cards

    def fold(self) -> int:
        self.send_str(FLD_OP)
        #self.send_int(a, INT_SIZE)
        #res = self.receive_int(INT_SIZE)
        return 0

    # def exec(self):
    #     # Operação de soma
    #     print("Olá. Queres somar?")
    #     (a, b) = self.interface_soma()
    #     #self.send_str(self.connection,ADD_OP)
    #     #self.send_int(self.connection,a, INT_SIZE)
    #     #self.send_int(self.connection,b, INT_SIZE)
    #     #res = self.receive_int(self.connection,INT_SIZE)
    #     self.send_str(client.ADD_OP)
    #     self.send_int(a,client.INT_SIZE)
    #     self.send_int(b,client.INT_SIZE)
    #     res = self.receive_int(client.INT_SIZE)
    #     print("O resultado da soma é:",res)
    #     # Operação de subtração
    #     print("Olá. Queres subtrair?")
    #     (a, b) = self.interface_subtracao()
    #
    #     #self.send_str(self.connection,SUB_OP)
    #     #self.send_int(self.connection,a, INT_SIZE)
    #     #self.send_int(self.connection,b, INT_SIZE)
    #     #res = self.receive_int(self.connection,INT_SIZE)
    #     self.send_str(client.SUB_OP)
    #     self.send_int(a,client.INT_SIZE)
    #     self.send_int(b,client.INT_SIZE)
    #     res = self.receive_int(client.INT_SIZE)
    #     print("O resultado da subtração é:",res)
    #     # Fechar a conexão
    #     self.send_str(client.BYE_OP)
    #     self._socket.close()


