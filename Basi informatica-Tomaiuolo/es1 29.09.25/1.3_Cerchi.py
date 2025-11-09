import g2d
from random import randrange

# Chiedi all'utente quanti cerchi disegnare
n = int(input("Quanti cerchi vuoi disegnare? "))

# Imposta il canvas
g2d.init_canvas((500, 500))

raggio = 50

for _ in range(n):
    # Coordinate casuali (centro del cerchio)
    x = randrange(raggio, 500 - raggio)
    y = randrange(raggio, 500 - raggio)

    # Colore casuale (RGB)
    colore = (randrange(256), randrange(256), randrange(256))

    # Disegna il cerchio pieno
    g2d.set_color(colore)
    g2d.draw_circle((x, y), raggio)

# Mostra il disegno e mantiene aperta la finestra
g2d.main_loop()
6