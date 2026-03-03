n = float(input("Inserisci un numero: "))

divisori = []
for i in range(1, int(n) + 1):
    if n % i == 0:
        divisori.append(i)
print(f"I divisori di {n} sono: {divisori}")