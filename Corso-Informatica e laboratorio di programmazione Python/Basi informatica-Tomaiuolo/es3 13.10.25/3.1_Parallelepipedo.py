import math

class Parallelepipedo:
    def __init__(self, l, w, h):
        self.__l = l      # larghezza
        self.__w = w      # profondità
        self.__h = h      # altezza

    def volume(self):
        return self.__l * self.__w * self.__h

    def diagonale(self):
        return math.sqrt(self.__l**2 + self.__w**2 + self.__h**2)

def main():
    print("Calcolo volume e diagonale di un parallelepipedo")
    l = float(input("Inserisci la larghezza (l): "))
    w = float(input("Inserisci la profondità (w): "))
    h = float(input("Inserisci l'altezza (h): "))

    p = Parallelepipedo(l, w, h)

    print(f"\nVolume = {p.volume()}")
    print(f"Diagonale = {p.diagonale():.2f}")

main()
