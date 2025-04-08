from server.processamento.player import Player


class GameState:
    def __init__(self):
        self._current_players = []
        self._actual_player = 0

    def add_player(self, player: Player):
        self._current_players.append(player)

    def actual_player(self):
        return self._actual_player

    def increment_state(self):
        if len(self._current_players) - 1 == self._actual_player:
            self._actual_player = 0
        else:
            self._actual_player += 1
