import threading
import time
import json
from server.processamento.data_structure import DataStructure
from server.skeleton.clientes import Clientes
# ------------------------------------------------------------------------- #
# Esta classe vai fazer "broadcast" da mensagem de atualização do estado do
# jogo para cada um dos clientes.
# Os sockets de cada um dos clientes são obtidos na nova classe clientes.
# ------------------------------------------------------------------------- #
class ThreadUpdate(threading.Thread):

    def __init__(self,estrutura: DataStructure, clientes: Clientes):
        threading.Thread.__init__(self)
        self.fim = False
        self.estrutura = estrutura
        self.clientes = clientes
        self.sleeping = 0.1

    def run(self):
        while not self.fim:
            time.sleep(self.sleeping)
            # Testa o número de clientes ligados
            #if self.clientes.get_nr_clients() == 0:
            #    self.fim == True
            #else:
            for connection in self.clientes.get_clients():
                # Broadcasting messages to all clients
                self.send_obj(connection, self.estrutura.retorna_dados(),INT_SIZE)
                print("Thread_update:Sent message to client!")
        print("Update Thread stopped!")
