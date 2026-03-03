# Richiesta delle coordinate dei due punti
x1 = float(input("Inserisci x1: "))
y1 = float(input("Inserisci y1: "))
x2 = float(input("Inserisci x2: "))
y2 = float(input("Inserisci y2: "))

# Calcolo delle differenze
delta_x = x2 - x1
delta_y = y2 - y1

# Controllo del caso limite (retta verticale)
if delta_x == 0:
    print("La retta è verticale: la pendenza è indefinita (divisione per zero).")
else:
    m = delta_y / delta_x
    print(f"La pendenza della retta è: {m}")
