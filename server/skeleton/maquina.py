import socket
import thread_cliente
import contador
import middleware.middleware as middle
from server.processamento.game_state import GameState
from server.processamento.data_structure import Data_Structure
from server.processamento.player import Player

class Maquina:
    def __init__(self,server_address,port):
        """
        Runs the server server until the client sends a "terminate" action. The setblocking
        is now false. That means that server will not wait for connection from client.
        As soon as it detects there is no client connecting it raises an exception
        BlockingIOerror. In this way, it is possible to identify if all clients
        have finished its interaction with the server.

        """
        self._socket = middle.Socket.start_socket_server(server_address,port,True)
        #self.port =port
        #self.s = socket.socket()
        #self.s.bind(('', self.port))
        # blocking
        #self.s.setblocking(False)
        #self.s.listen(1)
        self.contador = contador.Contador()
        self.game_state = GameState()
        self.data_structure = Data_Structure()
        self.player = Player()
        self._socket.settimeout(2.0)


    def exec(self):
        #print("Waiting for clients to connect on port " + str(self.port))
        print("Waiting for clients to connect on port " + str(self._socket.get_port()))

        keep_running = True
        first_connection = False
        while keep_running:
            try:
                self._new_socket = self._socket.accept()
                #connection, address = self.s.accept()
                #print("Client " + str(address) + " just connected")
                self.contador.incrementa()
                first_connection = True
                # Create and start a new ClientThread for each client connection
                #tc = thread_cliente.ThreadCliente(connection, address, self.contador)
                tc = thread_cliente.ThreadCliente(self._new_socket, self.contador, self.game_state, self.data_structure, self.player)
                tc.start()

            except socket.timeout:
            #except BlockingIOError:
                print("Contagem:",self.contador.retorna_contagem())
                if self.contador.retorna_contagem() == 0 and first_connection == True:
                    keep_running = False

        self._socket.close()
        print("Server stopped")

