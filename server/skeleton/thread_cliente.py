import threading
from server.processamento import somar, subtracao
import middleware.middleware as middle
import server
from server.skeleton import COMMAND_SIZE, INT_SIZE, HIT_OP, PAS_OP, FLD_OP, BYE_OP

class ThreadCliente(threading.Thread):

#    def __init__(self,connection, address, contador):
    def __init__(self,socket: middle.Socket, contador):

        threading.Thread.__init__(self)
        self._socket = socket
        self.contador = contador
        #self.connection = connection
        self.address = self._socket.get_address()
        self.port = self._socket.get_port()
        #self.address = address
        self.som = somar.Somar()
        self.sub = subtracao.Subtracao()


    def receive_int(self,n_bytes: int) -> int:
        return self._socket.receive_int(n_bytes)

    def send_int(self,i: int,n_bytes: int):
        self._socket.send_int(i,n_bytes)

    def receive_str(self, n_bytes: int) -> str:
        return self._socket.receive_str(n_bytes)

    def send_str(self):
        self._socket.send_str()
# ---------------------- interaction with sockets ------------------------------
#     def receive_int(self,connection, n_bytes: int) -> int:
#         """
#         :param n_bytes: The number of bytes to read from the current connection
#         :return: The next integer read from the current connection
#         """
#         data = connection.recv(n_bytes)
#         return int.from_bytes(data, byteorder='big', signed=True)
#
#     def send_int(self,connection, value: int, n_bytes: int) -> None:
#         """
#         :param value: The integer value to be sent to the current connection
#         :param n_bytes: The number of bytes to send
#         """
#         connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))
#
#     def receive_str(self,connection, n_bytes: int) -> str:
#         """
#         :param n_bytes: The number of bytes to read from the current connection
#         :return: The next string read from the current connection
#         """
#         data = connection.recv(n_bytes)
#         return data.decode()

    # def send_str(self,connection, value: str) -> None:
    #     """
    #     :param value: The string value to send to the current connection
    #     """
    #     connection.current_connection.send(value.encode())

    def run(self):
        last_request = False
        # Recebe messagens...
        while not last_request:
            #request_type = self.receive_str(self.connection,COMMAND_SIZE)
            request_type = self.receive_str(COMMAND_SIZE)
            if request_type == HIT_OP:
                a = self.receive_int(INT_SIZE)
                print("O jogador vai a jogo")
                #result = self.som.operacao(a,b)
                #self.send_int(result,INT_SIZE)
            elif request_type == PAS_OP:
                a = self.receive_int(INT_SIZE)
                b = self.receive_int(INT_SIZE)
                print("O jogador vai passar")
                result = self.sub.operacao(a,b)
                self.send_int(result,INT_SIZE)
                #self.send_int(self.connection,result, INT_SIZE)
            elif request_type == FLD_OP:
                print("O jogador desistiu da rodada!")
            elif request_type == BYE_OP:
                print("Client ",self.address," disconnected!")
                self.contador.decrementa()
                last_request = True
        #print("Ficam:",self.contador.retorna_contagem()," clientes!")
        #self.connection.close()
        self._socket.close()
