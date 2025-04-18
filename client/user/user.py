from client.stub import interface as processar, INT_SIZE
from server.processamento.player import Player


class User:
    def __init__(self, inter: processar):
        self.processar = inter
        self.player = Player()


    def bet_value(self):
        valor_aposta = int(input("Introduz o valor da aposta: "))
        return valor_aposta


    """
    def valores_soma(self)->tuple:
        res1 = int(input("Introduz o primeiro valor para somar:"))
        res2 = int(input("Introduz o segundo valor para somar:"))
        return (res1, res2)

    def valores_subtracao(self)->tuple:
        res1 = int(input("Introduz o primeiro valor para subtrair:"))
        res2 = int(input("Introduz o segundo valor para subtrair:"))
        return (res1, res2)
"""
    def exec(self):
        turn = 0
        num = self.processar.receive_int(INT_SIZE)
        while True:
            if turn == 0:
                turn += 1
                print(f"O teu número de jogador: {num}")
                option = int(input("Queres apostar ou desistir?\n1-Apostar\n2-Desistir\n"))
                match option:
                    case 1:
                        print("Vamos apostar? Anda daí!")
                        b_value = self.bet_value()
                        # quero fazer a aposta sem que se saiba que ela não é feita no cliente!
                        res = self.processar.bet(b_value)
                        print(f"Apostaste {res} fichas!")
                        self.player.set_hand(self.processar.cards_received())
                        com_cards = self.processar.community_cards()
                        print(f"Aqui estão as tuas cartas: {self.player.hand}\n"
                              f"Cartas comunitárias: {com_cards}")
                        self.processar.pass_turn()

                    case 2:
                        print("Desististe da rodada! Agora espera pela próxima!")
                        self.processar.fold()

                    case _:
                        print("Escolha inválida!")
            else:
                option = int(input("Queres apostar,desistir ou passar?\n1-Apostar\n2-Desistir\n3-Passar\n"))
                print(f"As tuas cartas: {self.player.hand}\n"
                      f"Cartas comunitárias: {com_cards}")
                match option:
                    case 1:
                        self.processar.more_community_cards()

