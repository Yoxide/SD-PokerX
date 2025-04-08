class Player:
    def __init__(self):
        self._state =""
        self._bets = []
    def set_state(self, state:int):
        self._state = state
    def set_bet(self, value:int):
        self._bets.append(value)