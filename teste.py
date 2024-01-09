class Animal():
    def __init__(self, especie, nome):
        self.especie = especie
        self.nome = nome
    def apresenta(self):
        print(f"ASaR eu sou o {self.nome} da espécie {self.especie}")


gato = Animal("Gato", "Beto")
cachorro = Animal("cachorro", "Alfredo")

gato.apresenta()
cachorro.apresenta()