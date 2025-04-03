from client.stub import interface as processar


class User:
    def __init__(self, inter: processar):
        self.processar = inter
        self.chips = 100
        self.hand = []

    def aposta(self) -> int:
        valor_aposta = int(input("Introduz o valor da aposta:"))
        self.chips -= valor_aposta
        return self.chips


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
        print("Vamos apostar? Anda daí!")
        a = self.aposta()
        # quero fazer  soma sem que se saiba que ela não é feita no cliente!
        res = self.processar.aposta(a)
        print("O tua aposta é:", res)
        print("Olá. Queres subtrair?")
        (a, b) = self.valores_subtracao()
        # quero fazer  soma sem que se saiba que ela não é feita no cliente!
        res = self.processar.subtrai(a,b)
        print("O valor da soma é:", res)
