import random
from server.processamento.player import Player
from collections import Counter
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

RANK_ORDER = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
              '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
HAND_RANKING = {
    "Royal Flush": 10,
    "Straight Flush": 9,
    "Four of a Kind": 8,
    "Full House": 7,
    "Flush": 6,
    "Straight": 5,
    "Three of a Kind": 4,
    "Two Pair": 3,
    "One Pair": 2,
    "Sem par": 1
}

class DataStructure:
    def __init__(self):
        """ Classe com as estruturas de dados básicas do jogo"""
        self._ranks = "23456789TJQKA"
        self._suits = "CDHS"
        self._deck = [f"{rank}-{suit}" for rank in self._ranks for suit in self._suits]
        self._players = {}
        self._community_cards = []
        self._min_bet = 0
        self._game = {}
        self._players["0"] = Player()
        self._players["1"] = Player()


    def return_data(self):
        """Retorna o estado do jogo"""
        return self._game

    def add_name(self, name):
        pass


    def add_player(self, player_id):
        """Adiciona um jogador"""
        if player_id not in self._players:
            self._players[player_id] = Player()

    def shuffle_deck(self):
        """ Método para baralhar as cartas"""
        random.shuffle(self._deck)

    def deal_hand(self, p: int, n: int):
        """ Método para "dar" n cartas a um jogador """
        player = self._players[f"{p}"]
        for _ in range(n):
            player.add_to_hand(self._deck.pop())
        return player.hand

    def deal_community_cards(self, n: int):
        """ Método para "dar" as 5 cartas comunitárias"""
        chosen_cards = [self._deck.pop() for _ in range(n)]
        self._community_cards.extend(chosen_cards) # n cartas comunitárias
        return chosen_cards

    def player_choice(self, pl:int, choice: int):
        """ Método para verificar a ação do jogador"""
        self._players[chr(pl)].set_state(choice)
        if choice == HIT:
            pass
        elif choice == FOLD:
            pass
        elif choice == PASS:
            pass

    def evaluate_hand(self, hand):
        if self.is_royal_flush(hand):
            return HAND_RANKING["Royal Flush"], self.get_sorted_rank_values(hand)
        elif self.is_straight_flush(hand):
            return HAND_RANKING["Straight Flush"], self.get_sorted_rank_values(hand)
        elif self.is_four_of_a_kind(hand):
            return HAND_RANKING["Four of a Kind"], self.get_sorted_rank_values(hand)
        elif self.is_full_house(hand):
            return HAND_RANKING["Full House"], self.get_sorted_rank_values(hand)
        elif self.is_flush(hand):
            return HAND_RANKING["Flush"], self.get_sorted_rank_values(hand)
        elif self.is_straight(hand):
            return HAND_RANKING["Straight"], self.get_sorted_rank_values(hand)
        elif self.is_three_of_a_kind(hand):
            return HAND_RANKING["Three of a Kind"], self.get_sorted_rank_values(hand)
        elif self.is_two_pair(hand):
            return HAND_RANKING["Two Pair"], self.get_sorted_rank_values(hand)
        elif self.is_one_pair(hand):
            return HAND_RANKING["One Pair"], self.get_sorted_rank_values(hand)
        else:
            return HAND_RANKING["Sem par"], self.get_sorted_rank_values(hand)

    def get_ranks(self, hand):
        return [card.split('-')[0] for card in hand]

    def get_suits(self, hand):
        return [card.split('-')[1] for card in hand]

    def get_rank_counts(self, hand):
        ranks = self.get_ranks(hand)
        return Counter(ranks)

    def get_sorted_rank_values(self, hand) -> list:
        return sorted([RANK_ORDER[rank] for rank in self.get_ranks(hand)], reverse=True)

    def is_royal_flush(self, hand) -> bool:
        return self.is_straight_flush(hand) and set(self.get_ranks(hand)) == {'A', 'K', 'Q', 'J', 'T'}

    def is_straight_flush(self, hand) -> bool:
        return self.is_flush(hand) and self.is_straight(hand)

    def is_four_of_a_kind(self, hand) -> bool:
        return 4 in self.get_rank_counts(hand).values()

    def is_full_house(self, hand) -> bool:
        counts = self.get_rank_counts(hand).values()
        return 3 in counts and 2 in counts

    def is_flush(self, hand) -> bool:
        suits = self.get_suits(hand)
        return len(set(suits)) == 1

    def is_straight(self, hand) -> bool:
        values = self.get_sorted_rank_values(hand)
        if values == [14, 5, 4, 3, 2]:  # Handle wheel straight (A-2-3-4-5)
            return True
        return all(values[i] - 1 == values[i + 1] for i in range(len(values) - 1))

    def is_three_of_a_kind(self, hand) -> bool:
        return 3 in self.get_rank_counts(hand).values() and not self.is_full_house(hand)

    def is_two_pair(self, hand) -> bool:
        counts = self.get_rank_counts(hand).values()
        return list(counts).count(2) == 2

    def is_one_pair(self, hand) -> bool:
        counts = self.get_rank_counts(hand).values()
        return list(counts).count(2) == 1

    def is_high_card(self, hand) -> bool:
        return not any([
            self.is_one_pair(hand),
            self.is_two_pair(hand),
            self.is_three_of_a_kind(hand),
            self.is_straight(hand),
            self.is_flush(hand),
            self.is_full_house(hand),
            self.is_four_of_a_kind(hand),
            self.is_straight_flush(hand),
            self.is_royal_flush(hand)
        ])

    def compare_hands(self, hand1, hand2):
        rank1, kicker1 = self.evaluate_hand(hand1)
        rank2, kicker2 = self.evaluate_hand(hand2)

        # Comparar os pares
        if rank1 > rank2:
            return 1  # hand1 ganha
        elif rank2 > rank1:
            return -1  # hand2 ganha
        else:
            # Comparar os kickers
            for k1, k2 in zip(kicker1, kicker2):
                if k1 > k2:
                    return 1 # hand1 ganha
                elif k2 > k1:
                    return -1 # hand2 ganha
            return 0  # Empate

    def get_hand_name(self, rank_value):
        for name, value in HAND_RANKING.items():
            if value == rank_value:
                return name
        return "Mão desconhecida"



