class CodiciPariDispari:
    def __init__(self, testo):
        self.testo = testo
        self.pari = 0
        self.dispari = 0
        
    def _calcola(self):
        for c in self.testo:
            if c.islower():
                if ord(c) % 2 == 0:
                    self.pari += 1
                else:
                    self.dispari += 1

    def mostra_risultati(self):
        self._calcola()

        print(f"Minuscole con codice pari: {self.pari}")
        print(f"Minuscole con codice dispari: {self.dispari}")


def main():
    testo = input("Inserisci una stringa: ")
    analisi = CodiciPariDispari(testo)
    analisi.mostra_risultati()

main()