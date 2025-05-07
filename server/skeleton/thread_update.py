import threading
import time
import json
import middleware.middleware as middle
from server.processamento.data_structure import DataStructure
from server.skeleton.clientes import Clientes
from server.skeleton import INT_SIZE
# ------------------------------------------------------------------------- #
# Esta classe vai fazer "broadcast" da mensagem de atualização do estado do
# jogo para cada um dos clientes.
# Os sockets de cada um dos clientes são obtidos na nova classe clientes.
# ------------------------------------------------------------------------- #
class ThreadUpdate(threading.Thread):

    def __init__(self,estrutura: DataStructure, clientes: Clientes, socket: middle.Socket):
        threading.Thread.__init__(self)
        self.fim = False
        self.estrutura = estrutura
        self.clientes = clientes
        self.sleeping = 0.1
        self._socket = socket

    def send_obj(self, obj: any) -> None:
        self._socket.send_object(obj)

    def run(self):
        while not self.fim:
            time.sleep(self.sleeping)
            # Testa o número de clientes ligados
            #if self.clientes.get_nr_clients() == 0:
            #    self.fim == True
            #else:
            for _ in self.clientes.get_clients():
                # Broadcasting messages to all clients
                #self.send_obj(self.estrutura.return_data())
                print("Thread_update:Sent message to client!")
        print("Update Thread stopped!")
