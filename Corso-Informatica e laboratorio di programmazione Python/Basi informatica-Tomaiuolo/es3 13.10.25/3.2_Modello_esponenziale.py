import math

class ExpoModel:
    def __init__(self, a, b, c):
        self.__a = a
        self.__b = b
        self.__c = c

    def estimate(self, x):
        return self.__a * math.exp(self.__b * x) + self.__c


def main():
    print("Modello esponenziale: y = a * e^(b*x) + c")

    a = float(input("Inserisci coefficiente a: "))
    b = float(input("Inserisci coefficiente b: "))
    c = float(input("Inserisci coefficiente c: "))

    model = ExpoModel(a, b, c)

    x = input("\nInserisci valore di x (Invio per terminare): ")
    while x != "":
        print(f"y = {model.estimate(float(x))}")
        x = input("\nInserisci valore di x (Invio per terminare): ")

    print("Fine programma.")

main()
