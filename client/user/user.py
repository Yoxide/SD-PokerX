from client.stub import interface as processar
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
        option = int(input("Queres apostar ou desistir?\n1-Apostar\n2-Desistir\n"))
        match option:
            case 1:
                print("Vamos apostar? Anda daí!")
                b_value = self.bet_value()
                # quero fazer a aposta sem que se saiba que ela não é feita no cliente!
                res = self.processar.bet(b_value)
                print(f"Apostaste {res} fichas!")
                print(f"Aqui estão as tuas cartas: {self.player.hand}")
            case 2:
                print("Desististe da rodada! Agora espera pela próxima!")
                self.processar.fold()

            case _:
                print("Escolha inválida!")
        """
        print("O tua aposta é:", res)
        print("Olá. Queres subtrair?")
        (a, b) = self.valores_subtracao()
        # quero fazer  soma sem que se saiba que ela não é feita no cliente!
        res = self.processar.subtrai(a,b)
        print("O valor da soma é:", res)
"""