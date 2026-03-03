class CodiciPariDispari:
    def __init__(self, testo):
        self.testo = testo
        self._pari = 0
        self._dispari = 0
        
    def _calcola(self):
        """Conta le minuscole con codice pari e dispari"""
        self._pari = 0
        self._dispari = 0
        for c in self.testo:
            if c.islower():
                if ord(c) % 2 == 0:
                    self._pari += 1
                else:
                    self._dispari += 1

    def mostra_risultati(self):
        self._calcola()
        print(f"Minuscole con codice pari: {self._pari}")
        print(f"Minuscole con codice dispari: {self._dispari}")
    
    def pari(self):
        return self._pari
    
    def dispari(self):
        return self._dispari


def main():
    tot_pari = 0
    tot_dispari = 0

    testo = input("Inserisci una stringa (vuota per terminare): ")
    while testo != "":
        analisi = CodiciPariDispari(testo)
        analisi.mostra_risultati()
        tot_pari += analisi.pari()
        tot_dispari += analisi.dispari()
        testo = input("Inserisci una stringa (vuota per terminare): ")
    
    print(f"Totale minuscole con codice pari: {tot_pari}")
    print(f"Totale minuscole con codice dispari: {tot_dispari}")


main()
