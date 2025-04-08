class Player:
    """
    Classe que representa um jogador
    """
    def __init__(self):
        self._state =""
        self._bets = []
        self._name = ""

    def set_state(self, state:int):
        self._state = state

    def set_bet(self, value:int):
        self._bets.append(value)

    def get_name(self) -> str:
        return self._name

    def set_name(self, name:str):
        self._name = name