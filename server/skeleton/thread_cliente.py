import threading
import middleware.middleware as middle
from server.processamento import game_state
from server.skeleton import COMMAND_SIZE, INT_SIZE, HIT_OP, PAS_OP, FLD_OP, BYE_OP, OK_OP
from server.processamento.data_structure import DataStructure
from server.processamento.player import Player
from time import sleep
from server.skeleton.clientes import Clientes
from server.skeleton.thread_update import ThreadUpdate
active_threads = []


class ThreadCliente(threading.Thread):

    def __init__(self, socket: middle.Socket, contador, gamestate: game_state.GameState, data_structure: DataStructure, clientes: Clientes, update: ThreadUpdate):

        threading.Thread.__init__(self)
        active_threads.append(self)
        self._socket = socket
        self.contador = contador
        self.gamestate = gamestate
        #self.player = None
        self.data_structure = data_structure
        self.address = self._socket.get_address()
        self.port = self._socket.get_port()
        self.player_number = str(len(self.gamestate.current_players)) # Rever
        self.data_structure.add_player(self.player_number) # Rever
        self.clientes = clientes
        self.update = update

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

    def evaluate_and_announce_winner(self):
        best_player = None
        best_hand = None
        best_eval = None
        best_eval_name = None

        print("\n--- Avaliação Final das Mãos ---")

        for pid, player in self.data_structure._players.items():

            if player.is_folded():
                continue

            full_hand = player.hand + self.data_structure._community_cards
            print(f"Jogador {pid}: Mão completa -> {full_hand}")
            rank_value, kickers = self.data_structure.evaluate_hand(full_hand)

            if best_hand is None:
                best_hand = full_hand
                best_player = pid
                best_eval = (rank_value, kickers)
                best_eval_name = self.data_structure.get_hand_name(rank_value)

            else:
                if self.data_structure.compare_hands(full_hand, best_hand) == 1:
                    best_hand = full_hand
                    best_player = pid
                    best_eval = (rank_value, kickers)
                    best_eval_name = self.data_structure.get_hand_name(rank_value)

        print(f"\n🎉 Jogador vencedor: {best_player} com {best_eval_name} (Ranking: {best_eval})")
        result_str = f"Jogador {best_player} venceu com {best_eval_name}!"
        self.update.broadcast_result(result_str)
        # Reinicia a ronda
        self.reset_round()

        self.data_structure.shuffle_deck()

    def check_auto_win(self):
        active = self.data_structure.get_active_players_ids()

        print(f"Jogadores ativos: {active}")

        if len(active) == 1:
            winner = active[0]
            result_str = f"Jogador {winner} venceu por desistência dos outros jogadores!"
            print(f"[AUTO-WIN] {result_str}")
            self.broadcast_result(result_str)
            self.reset_round()
            return True  # O jogo acaba

        return False  # continuar

    def reset_round(self):
        # Limpa todos os dados do servidor
        self.data_structure._community_cards.clear()
        self.gamestate.community_dealt = 0
        self.gamestate.actions_this_round = 0

        # Limpa todos os dados do jogador
        for player in self.data_structure._players.values():
            player.clear_hand()

        # Acorda todas as threads
        with self.gamestate.turn_lock:
            self.gamestate.turn_lock.notify_all()


    def broadcast_result(self, result_str):
        for t in active_threads:
            try:
                t.send_str(result_str)
            except Exception as e:
                print(f"Aviso: Erro ao enviar resultado para o jogador {t.player_number}: {e}")

    def run(self):
        last_request = False

        player = self.data_structure.get_player(self.player_number)
        self.gamestate.current_players.append(player)
        self.player_number = self.gamestate.current_players.index(player)
        self.send_int(int(self.player_number), INT_SIZE)
        self.data_structure.shuffle_deck()
        # Na primeira ronda quando o jogador ainda não tem cartas
        self.data_structure.deal_hand(self.player_number, 2) # O servidor envia 2 cartas ao jogador
        self.send_obj(player.hand)
        #self.clientes.add_client(player)
        print(player.hand)
        # Recebe messagens...
        while not last_request:
            with (self.gamestate.turn_lock):
                while (self.player_number != self.gamestate.actual_player()
                or self.data_structure._players[str(self.player_number)].is_folded()):
                    self.gamestate.turn_lock.wait()
                    print("Waiting!")
            # Turno do cliente
            self.send_str(OK_OP)
            self.send_obj(self.data_structure._community_cards)

            # Ação do jogador
            request_type = self.receive_str(COMMAND_SIZE)

            if request_type == HIT_OP:
                print("O jogador vai a jogo")
                b_value = self.receive_int(INT_SIZE)
                aposta = player.bet(b_value)
                print(f"O jogador apostou {aposta} fichas")
                self.send_int(aposta, INT_SIZE)
                print("Enviámos o valor da aposta para o jogador")

                print(self.data_structure.evaluate_hand(player.hand))

                new_cards = self.gamestate.increment_state(self.data_structure)

                if self.check_auto_win():
                    return

                if new_cards:
                    print(f"Novas cartas comunitárias: {new_cards}")

                if self.gamestate.community_dealt == 5 and self.gamestate.actions_this_round == 0:
                    self.evaluate_and_announce_winner()

            elif request_type == PAS_OP:
                print(f"O Jogador {self.player_number} passou.")
                new_cards = self.gamestate.increment_state(self.data_structure)

                if self.check_auto_win():
                    return

                if new_cards:
                    print(f"Novas cartas comunitárias: {new_cards}")

                if self.gamestate.community_dealt == 5 and self.gamestate.actions_this_round == 0:
                    self.evaluate_and_announce_winner()

            elif request_type == FLD_OP:
                print(f"Jogador {self.player_number} desistiu da rodada.")
                player.fold()
                self.gamestate.increment_state_fold()

                if self.check_auto_win():
                    return

                if self.gamestate.community_dealt == 5 and self.gamestate.actions_this_round == 0:
                    self.evaluate_and_announce_winner()

            elif request_type == BYE_OP:
                print("Client ",self.address," disconnected!")
                self.contador.decrementa()
                last_request = True
        self._socket.close()