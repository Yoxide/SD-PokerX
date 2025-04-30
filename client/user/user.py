from client.stub import interface as processar, INT_SIZE



class User:
    def __init__(self, inter: processar):
        self.processar = inter


    def bet_value(self):
        valor_aposta = int(input("Introduz o valor da aposta: "))
        return valor_aposta

    def exec(self):
        turn = 0
        num = self.processar.receive_int(INT_SIZE)
        hand = self.processar.receive_object()
        print(f"O teu número de jogador: {num}")
        while True:
            turn += 1
            print("Espera pela tua vez!\n")

            if turn == 4:
                result = self.processar.receive_str(100)  # O vencedor
                print(result)
                return  # Se o prog não acabar, fica sempre à espera do "é a tua vez"

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
                    print(f"Aqui estão as tuas cartas: {hand}\n")
                case 2:
                    print("Desististe da rodada! Agora espera pela próxima!")
                    self.processar.fold()


                case 3:
                    print("Passaste a tua vez.")
                    self.processar.pass_turn()

                case _:
                    print("Escolha inválida!")


