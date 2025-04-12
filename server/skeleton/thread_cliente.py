import threading
from server.processamento import somar, subtracao, player
import middleware.middleware as middle
from server.processamento import game_state
import json
from server.skeleton import COMMAND_SIZE, DIST_OP, INT_SIZE, HIT_OP, PAS_OP, FLD_OP, BYE_OP, OK_OP
from server.processamento.data_structure import Data_Structure
from server.processamento.player import Player
from time import sleep

class ThreadCliente(threading.Thread):

#    def __init__(self,connection, address, contador):
    def __init__(self,socket: middle.Socket, contador, gamestate: game_state.GameState, data_structure: Data_Structure, player: Player):

        threading.Thread.__init__(self)
        self._socket = socket
        self.contador = contador
        self.gamestate = gamestate
        self.player = player
        self.data_structure = data_structure
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

    def send_str(self, string: str):
        self._socket.send_str(string)


    def send_obj(self, obj: any) -> None:
        self._socket.send_object(obj)


    def receive_object(self) -> int:
        return self._socket.receive_object()
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

            # CONEXAO  Recebem o nome do jogador e retornam o número
            self.gamestate._current_players.append(self.player)
            self.player_number = self.gamestate._current_players.index(self.player)
            #request_type = self.receive_str(self.connection,COMMAND_SIZE)
            request_type = self.receive_str(COMMAND_SIZE)
            if request_type == DIST_OP:
                self.gamestate.increment_state()
                # Pedir cartas ao data_structure com indicacao do nr_jogador
                self.send_str(self.data_structure.deal_hand())

                while self.player_number != self.gamestate.actual_player() :
                    print("Aguarde a sua vez!")

                self.send_str(OK_OP)
                # waiting for player turn
                sleep(1)
                print("Envio a distribuição")

            if request_type == HIT_OP:
                print("O jogador vai a jogo")
                b_value = self.receive_int(INT_SIZE)
                aposta = self.player.bet(b_value)
                print(f"O jogador apostou {aposta} fichas")
                self.send_int(aposta, INT_SIZE)
                print("Enviámos o valor da aposta para o jogador")
                self.data_structure.shuffle_deck()
                cards_received = self.data_structure.deal_hand(self.player_number, 2)
                self.send_obj(cards_received)
                print(f"Relembramos que o número do jogador é {self.player_number}!")
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
