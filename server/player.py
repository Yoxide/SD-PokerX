class Player:
    def __init__(self):
        """Classe que representa um jogador"""
        self._hand = []
        self._tokens = 100

    def hit(self, index: int):
        """O jogador faz uma aposta"""
        if len(self._hand) > 0:
            self._hand.pop(index)

    def fold(self):
        """O jogador desiste da rodada"""
        return self._hand.clear()




