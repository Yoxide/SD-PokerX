import random

"""
_ p2 _
p3 _ p4
_ p1_
Aonde p1, p2, p3, p4 são jogadores

#Jogadores ligam-se
#O jogo começa e os jogadores recebem as suas cartas após o baralho das mesmas
#Inicialmente cada jogador deve apostar um valor, por turnos
#Uma vez estando uma aposta feita, os jogadores decidem se vão a jogo ou não
#Quem decidir ir a jogo recebe mais uma carta 
#O mesmo processo repete-se mais uma vez, até todos desistirem ou as cartas reveladas serem 5 
#O jogador com a melhor mão vence

"""


HIT = 0
FOLD = 1
PASS = 2
class Data_Structure:
    def __init__(self):
        """ Classe com as estruturas de dados básicas do jogo"""
        self._ranks = "23456789TJQKA"
        self._suits = "CDHS"
        self._deck = [f"{rank}-{suit}" for rank in self._ranks for suit in self._suits]
        self._players = []
        self._community_cards = []
        self._bet = 0
        self._game = {}
        self._p1 = ""
        self._p2 = ""

    def return_data(self):
        """Retorna o estado do jogo"""
        return self._game

    def add_name(self, name:str):
        if len(self._players) == 0:
            self._p1 = name
            self._players.append(name)
        else:
            self._p2 = name
            self._players.append(name)


    def shuffle_deck(self):
        """ Método para baralhar as cartas"""
        random.shuffle(self._deck)

    def deal_hand(self):
        """ Método para "dar" duas cartas a um jogador """
        return [self._deck.pop(), self._deck.pop()]

    def deal_community_cards(self):
        """ Método para "dar" as 5 cartas comunitárias"""
        return [self._deck.pop() for _ in range(5)]  # 5 cartas comunitárias

    def player_choice(self, choice: int):
        """ Método para verificar a ação do jogador"""
        if choice == HIT:
            pass
        elif choice == FOLD:
            pass
        elif choice == PASS:
            pass


