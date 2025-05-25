import threading
import time
import json
import middleware.middleware as middle
from server.processamento.data_structure import DataStructure
from server.processamento.game_state import GameState
from server.skeleton.clientes import Clientes
from server.skeleton import INT_SIZE
# ------------------------------------------------------------------------- #
# Esta classe vai fazer "broadcast" da mensagem de atualização do estado do
# jogo para cada um dos clientes.
# Os sockets de cada um dos clientes são obtidos na nova classe clientes.
# ------------------------------------------------------------------------- #
class ThreadUpdate(threading.Thread):
    def __init__(self,estrutura: DataStructure, clientes: Clientes, socket: middle.Socket, game_state: GameState):
        threading.Thread.__init__(self)
        self.fim = False
        self.estrutura = estrutura
        self.clientes = clientes
        self.game_state = game_state
        self.sleeping = 0.1
        self._socket = socket

    def send_update_obj(self, connection, value, n_bytes) -> None:
        self._socket.send_update_object(connection, value, n_bytes)

    def run(self):
        while not self.fim:
            time.sleep(self.sleeping)
            # Testa o número de clientes ligados
            #if self.clientes.get_nr_clients() == 0:
            #    self.fim == True
            #else:
            for connection in self.clientes.get_clients()            :
                # Broadcasting messages to all clients
                self.send_update_obj(connection, self.estrutura._community_cards, INT_SIZE)
                print("Thread_update:Sent message to client!")

        print("Update Thread stopped!")
