# ciclo per risolvere più equazioni di secondo grado

y = "si"  # inizializza la variabile per entrare nel ciclo

while y == "si":
    # input dei coefficienti
    a = float(input("Inserisci il coefficiente a: "))
    b = float(input("Inserisci il coefficiente b: "))
    c = float(input("Inserisci il coefficiente c: "))

    # calcolo del discriminante
    d = b**2 - 4*a*c

    # analisi dei casi
    if d < 0:
        print("L'equazione non ha soluzioni reali.")
    elif d == 0:
        x = -b / (2*a)
        print(f"L'equazione ha una soluzione reale doppia: x = {x}")
    else:
        x1 = (-b + d**0.5) / (2*a)
        x2 = (-b - d**0.5) / (2*a)
        print(f"L'equazione ha due soluzioni reali distinte: x1 = {x1}, x2 = {x2}")

    # chiede se ripetere
    y = input("Vuoi risolvere un'altra equazione? (si/no) ").lower()
