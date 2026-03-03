import g2d
from random import randrange


H, W = 400, 400
R = 5


g2d.init_canvas((H, W))


p1x = float(input("Inserisci la coordinata x del primo punto: "))
p1y = float(input("Inserisci la coordinata y del primo punto: "))
p2x = float(input("Inserisci la coordinata x del secondo punto: "))
p2y = float(input("Inserisci la coordinata y del secondo punto: "))

n = int(input("Inserisci il numero di punti da generare: "))

r1 = int(input("Inserisci il valore massimo per i componenti R (0-255) del primo punto: "))
g1 = int(input("Inserisci il valore massimo per i componenti G (0-255) del primo punto: "))
b1 = int(input("Inserisci il valore massimo per i componenti B (0-255)del primo punto: "))

r2 = int(input("Inserisci il valore massimo per i componenti R (0-255) del secondo punto: "))
g2 = int(input("Inserisci il valore massimo per i componenti G (0-255) del secondo punto: "))
b2 = int(input("Inserisci il valore massimo per i componenti B (0-255)del secondo punto: "))

    

def posizione_punti(P1x, P1y, P2x, P2y, n):
    punti = []
    if n == 1:
        punti.append((P1x, P1y))
    else:
        dx = (P2x - P1x) / (n - 1)
        dy = (P2y - P1y) / (n - 1)
        for i in range(n):
            x = P1x + i * dx
            y = P1y + i * dy
            punti.append((x, y))
    return punti


def main():
    punti = posizione_punti(p1x, p1y, p2x, p2y, n)

    for i, (x, y) in enumerate(punti):
        if n > 1:
            r = int(r1 + i * (r2 - r1) / (n - 1))
            g = int(g1 + i * (g2 - g1) / (n - 1))
            b = int(b1 + i * (b2 - b1) / (n - 1))
        else:
            r, g, b = r1, g1, b1
        colore = (r,g,b)    
        g2d.set_color((colore))
        g2d.draw_circle((x, y), R)
        
    

main()
g2d.main_loop()


    
    

