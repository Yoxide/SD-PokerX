
class Somar:
    def __init__(self):
        a: int = 0
        b: int = 0

    def operacao(self,a: int, b: int) -> int:
        self.a = a
        self.b = b
        return self.a + self.b
