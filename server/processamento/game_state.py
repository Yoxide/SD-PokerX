from threading import Condition
from server.processamento.player import Player

class GameState:
    def __init__(self):
        self.current_players = []
        self.current_player = 0
        self.turn_lock = Condition()
        self.actions_this_round = 0
        self.community_dealt = 0
        self.total_players = 0

    def add_player(self, player: Player):
        with self.turn_lock:
            self.current_players.append(player)
            self.total_players = len(self.current_players)

    def actual_player(self):
        return self.current_player

    def increment_state(self):
        with self.turn_lock:
            self.actions_this_round += 1
            self.current_player = (self.current_player + 1) % len(self.current_players)
            if self.actions_this_round >= self.total_players:
                self.actions_this_round = 0
                return True  # Já todos jogaram
            self.turn_lock.notify_all()
            return False  # Ainda não jogaram todos

