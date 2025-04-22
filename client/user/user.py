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
        num = self.processar.receive_int(INT_SIZE)
        print(f"O teu número de jogador: {num}")
        while True:
            print("Espera pela tua vez!\n")
            ok = self.processar.receive_str(9)
            if ok != "okay     ":
                continue
            com_cards = self.processar.receive_object()
            print(f"Cartas comunitárias: {com_cards}")

            print("É a tua vez!")
            option = int(input("Escolhe a opção que pretendes fazer\n1-Apostar\n2-Desistir\n3-Passar\n"))
            match option:
                case 1:
                    print("Vamos apostar? Anda daí!")
                    b_value = self.bet_value()
                    # quero fazer a aposta sem que se saiba que ela não é feita no cliente!
                    res = self.processar.bet(b_value)
                    print(f"Apostaste {res} fichas!")
                    self.player.set_hand(self.processar.cards_received())

                    print(f"Aqui estão as tuas cartas: {self.player.hand}\n")



                case 2:
                    self.processar.fold()
                    print("Desististe da rodada! Agora espera pela próxima!")

                case 3:
                    self.processar.pass_turn()
                    print("Passaste a tua vez.")

                case _:
                    print("Escolha inválida!")


