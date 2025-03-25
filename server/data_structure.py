import random

class Data_Structure:
    def __init__(self):
        """ Classe com as estruturas de dados básicas do jogo"""
        self._ranks = "23456789TJQKA"
        self._suits = "CDHS"
        self._deck = [f"{rank}-{suit}" for rank in self._ranks for suit in self._suits]
        self._players = []
        self._community_cards = []

    def shuffle_deck(self):
        """ Método para baralhar as cartas"""
        random.shuffle(self._deck)

    def deal_hand(self):
        """ Método para "dar" duas cartas a um jogador """
        return [self._deck.pop(), self._deck.pop()]

    def deal_community_cards(self):
        """ Método para "dar" as 5 cartas comunitárias"""
        return [self._deck.pop() for _ in range(5)]  # 5 cartas comunitárias



