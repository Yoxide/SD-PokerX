import socket
import thread_cliente

class Maquina:
    def __init__(self, server_address, port):
        self.port = port
        self.s = socket.socket()
        self.s.bind(('', self.port))
        self.s.listen(1)

    def exec(self):
        print("Waiting for clients to connect on port " + str(self.port))
        keep_running = True
        first_connection = False
        while keep_running:
            try:
                connection, address = self.s.accept()
                print("Client " + str(address) + " just connected")
                self.contador.incrementa()
                first_connection = True
                # Create and start a new ClientThread for each client connection
                tc = thread_cliente.ThreadCliente(connection, address, self.contador)
                tc.start()

            except BlockingIOError:
                #print("Contagem:",self.contador.retorna_contagem())
                if self.contador.retorna_contagem() == 0 and first_connection == True:
                    keep_running = False

        self.s.close()
        print("Server stopped")
