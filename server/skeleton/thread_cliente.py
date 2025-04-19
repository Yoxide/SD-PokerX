import threading
import middleware.middleware as middle
from server.processamento import game_state
from server.skeleton import COMMAND_SIZE, DIST_OP, INT_SIZE, HIT_OP, PAS_OP, FLD_OP, BYE_OP, OK_OP
from server.processamento.data_structure import Data_Structure
from server.processamento.player import Player
from time import sleep

class ThreadCliente(threading.Thread):

    def __init__(self,socket: middle.Socket, contador, gamestate: game_state.GameState, data_structure: Data_Structure, player: Player):

        threading.Thread.__init__(self)
        self._socket = socket
        self.contador = contador
        self.gamestate = gamestate
        self.player = player
        self.data_structure = data_structure
        self.address = self._socket.get_address()
        self.port = self._socket.get_port()

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

    def run(self):
        last_request = False
        # Recebe messagens...
        while not last_request:
            # CONEXAO  Recebem o nome do jogador e retornam o número
            self.gamestate.current_players.append(self.player)
            self.player_number = self.gamestate.current_players.index(self.player)
            self.send_int(self.player_number, INT_SIZE)

            with self.gamestate.turn_lock:
                while self.player_number != self.gamestate.actual_player():
                    self.gamestate.turn_lock.wait()

            # Turno do cliente
            self.send_str(OK_OP)

            # Ação do jogador
            request_type = self.receive_str(COMMAND_SIZE)

            if request_type == HIT_OP:
                print("O jogador vai a jogo")
                b_value = self.receive_int(INT_SIZE)
                aposta = self.player.bet(b_value)
                print(f"O jogador apostou {aposta} fichas")
                self.send_int(aposta, INT_SIZE)
                print("Enviámos o valor da aposta para o jogador")
                self.data_structure.shuffle_deck()
                # O servidor envia 2 cartas ao jogador
                cards_received = self.data_structure.deal_hand(self.player_number, 2)
                self.send_obj(cards_received)
                # O servidor revela 3 cartas comunitárias
                community_cards = self.data_structure.deal_community_cards(3)
                self.send_obj(community_cards)
                cards_received.extend(community_cards)
                print(cards_received)
                print(self.data_structure.evaluate_hand(cards_received))
                self.gamestate.increment_state()
                print("Relembramos que o número do jogador é", self.player_number)


            elif request_type == PAS_OP:
                print("O jogador vai passar")
                self.gamestate.increment_state()

            elif request_type == FLD_OP:
                print("O jogador desistiu da rodada!")
                self.gamestate.increment_state()

            elif request_type == BYE_OP:
                print("Client ",self.address," disconnected!")
                self.contador.decrementa()
                last_request = True
        self._socket.close()
