from random import randrange
import csv

w, h, n = map(int, input("wxh, n: \n").split())


m = [[0 for _ in range(w)] for _ in range(h)]

for _ in range(n):
    r = randrange(h)
    c = randrange(w)
    while m[r][c] == 1:         
        r = randrange(h)
        c = randrange(w)
    m[r][c] = 1

with open("Basi informatica-Tomaiuolo/es8 17.11.2025/matrix.csv", "w", newline="") as mat:
    writer = csv.writer(mat)
    for row in m:
        writer.writerow(row)


pos = input("scegli una posizione, x e y, sulla griglia: \nx y = ")

while pos != "":
    x, y = map(int, pos.split())

    # ricarico la matrice dal csv (stile tuo)
    camp = []
    with open("Basi informatica-Tomaiuolo/es8 17.11.2025/matrix.csv", "r") as mat:
        for row in mat:
            camp.append([int(v) for v in row.strip().split(",")])

    if camp[y][x] == 1:
        print("💣  BOOM! Hai preso una bomba!\n")
    else:
        h2 = len(camp) #-> quante righe ci sono ->ALTEZZA
        w2 = len(camp[0]) #-> quanti elementi ha la prima riga -> LARGHEZZA
        count_1 = 0 # conteggio bombe

        #(-1,-1), (-1,0), (-1,1), (0,-1), (0,0), (0,1), (1,-1), (1,0), (1,1)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1): 
                if dx == 0 and dy == 0:
                    continue #salto cella centrale
                ny = y + dy
                nx = x + dx
                if 0 <= ny < h2 and 0 <= nx < w2: #controllo che siamo nella griglia, caso bordo
                    if camp[ny][nx] == 1:
                        count_1 += 1
        print(f"Nessuna bomba qui. Bombe intorno: {count_1}\n")

    pos = input("x y = ")