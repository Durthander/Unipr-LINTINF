class Person:
    def __init__(self , y , m , d , c , n):
        self._y = int(y)
        self._m = int(m)
        self._d = int(d)
        self._n = n
        self._c = c
    
    def age(self, y_now, m_now, d_now):
        y_now = int(y_now)
        m_now = int(m_now)
        d_now = int(d_now)
        age = y_now - self._y
        if (m_now, d_now) < (self._m, self._d):  # compleanno non ancora passato
            age -= 1
        return age
    
    def maggiorenne(self, y_now, m_now, d_now):
        return self.age(y_now, m_now, d_now) >= 18

    def describe(self, y_now, m_now, d_now):
        return f"{self._n} {self._c}, {self.age(y_now, m_now, d_now)} anni"


def main():
    print("Inserisci dati di 3 persone")
    persone = []
    for i in range(3):
        print(f"\nPersona {i+1}:")
        y, m, d = input("Data di nascita (YYYY-MM-DD): ").split("-")
        c, n = input("Cognome e nome: ").split()
        p = Person(y, m, d, c, n)
        persone.append(p)

    print("\nOra puoi inserire date attuali per calcolare l'età.")
    print("Stringa vuota per terminare.\n")
    
    while True:
        today = input("Data attuale (YYYY-MM-DD): ")
        if today == "":
            print("Programma terminato.")
            break
        y_now, m_now, d_now = today.split("-")

        for p in persone:
            print(p.describe(y_now, m_now, d_now),
                  "- maggiorenne" if p.maggiorenne(y_now, m_now, d_now) else "- minorenne")
        print()


main()

