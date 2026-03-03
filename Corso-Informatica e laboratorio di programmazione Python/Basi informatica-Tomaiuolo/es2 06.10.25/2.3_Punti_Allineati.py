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
    
    for (x, y) in punti:
        g2d.draw_circle((x, y), R)
        g2d.set_color((randrange(256), randrange(256), randrange(256)
))

main()
g2d.main_loop()


    
    

