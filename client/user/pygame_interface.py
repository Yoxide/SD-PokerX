import sys
import pygame
import socket
import json
from client.stub import COMMAND_SIZE, INT_SIZE, BYE_OP

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class InterfacePyGame:
    def __init__(self, address, port):
        # --- Socket & ligação ---
        self.connection = socket.socket()
        self.connection.connect((address,port))
        # --- Game configuration ---
        self.window_size = 400
        self.grid_size = 4
        self.cell_size = self.window_size // self.grid_size

        # --- Colors ---
        self.white = (255, 255, 255)
        self.grey = (200, 200, 200)
        self.red = (255, 0, 0)
        self.blue =(0,0,255)
        self.other = (130,50,200)

        # --- Pygame setup ---
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("4x4 Jogo Simples")
        #self.clock = pygame.time.Clock()

        # --- Game state ---
        self.running = True
        self.piece_x = 0
        self.piece_y = 0


    # --------------------------------------------------------------------
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
    # ------------------------------------------------------------

    #Escolha uma jogada: UP 0 RIGHT 1 DOWN 2 LEFT 3
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.send_str(self.connection,PLAY_OP)
                    self.send_int(self.connection,LEFT,INT_SIZE)

                    #self.piece_x -= 1
                elif event.key == pygame.K_RIGHT:
                    self.send_str(self.connection,PLAY_OP)
                    self.send_int(self.connection,RIGHT,INT_SIZE)

                    #self.piece_x += 1
                elif event.key == pygame.K_UP:
                    #self.piece_y -= 1
                    self.send_str(self.connection,PLAY_OP)
                    self.send_int(self.connection,UP,INT_SIZE)

                elif event.key == pygame.K_DOWN:
                    self.send_str(self.connection,PLAY_OP)
                    self.send_int(self.connection,DOWN,INT_SIZE)

                #self.piece_y += 1

    def draw(self):
        self.screen.fill(self.white)

        # Draw grid
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size,
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.grey, rect, width=1)
        pygame.display.flip()


    def draw_players(self):
        # Draw piece
        piece_rect = pygame.Rect(
            self.piece_x * self.cell_size,
            self.piece_y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        pygame.draw.rect(self.screen, self.other, piece_rect)
        pygame.display.flip()


    def update(self):
        dados = self.receive_obj(self.connection,INT_SIZE)
        dados = dict(dados)
        print("Dados:", dados)

    def obtem_nome(self) -> str:
        print("Por favor, introduza o seu nome:")
        nome = input()
        return nome


    def exec(self):
        # Conexão
        nome = self.obtem_nome()
        self.send_str(self.connection,nome)
        self.num_jogador = self.receive_int(self.connection,INT_SIZE)
        print("O meu número é:", self.num_jogador)
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()
