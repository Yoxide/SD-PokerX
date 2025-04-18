from threading import Condition
from server.processamento.player import Player

class GameState:
    def __init__(self):
        self._current_players = []
        self.current_player = 0
        self.turn_lock = Condition()

    def add_player(self, player: Player):
        with self.turn_lock:
            self._current_players.append(player)

    def actual_player(self):
        return self.current_player

    def increment_state(self):
        with self.turn_lock:
            if len(self._current_players) > 0:
                self.current_player = (self.current_player + 1) % len(self._current_players)
                self.turn_lock.notify_all()

