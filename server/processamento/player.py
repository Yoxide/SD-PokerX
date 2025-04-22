class Player:
    """
    Classe que representa um jogador
    """
    def __init__(self):
        self._state = ""
        self._bets = []
        self._name = ""
        self.chips = 100
        self.hand = []
        self.current_bet = 0

    def set_state(self, state:int):
        self._state = state

    def set_bet(self, value:int):
        self._bets.append(value)

    def get_name(self) -> str:
        return self._name

    def set_name(self, name:str):
        self._name = name

    def get_hand(self):
        return self.hand

    def add_to_hand(self, card:str):
        self.hand.append(card)

    def set_hand(self, hand:list):
        self.hand = hand

    def bet(self, valor_aposta: int) -> int:
        self.chips -= valor_aposta
        return valor_aposta

    def clear_hand(self):
        self.hand = []