a = float(input("Inserisci il coefficiente a: "))
b = float(input("Inserisci il coefficiente b: "))
c = float(input("Inserisci il coefficiente c: "))

d = b**2 - 4*a*c

if d < 0:
    print("L'equazione non ha soluzioni reali.")
elif d == 0:
    print(f"L'equazione ha una soluzione reale doppia")
else:
    print(f"L'equazione ha due soluzioni reali distinte")