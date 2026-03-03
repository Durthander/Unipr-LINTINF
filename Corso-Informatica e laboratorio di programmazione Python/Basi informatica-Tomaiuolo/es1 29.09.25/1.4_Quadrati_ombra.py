import g2d
from random import randrange
# Chiedi all'utente quanti quadrati disegnare
n = int(input("Quanti quadrati vuoi disegnare? "))

# Imposta il canvas
g2d.init_canvas((500, 500))

lato = 50

for i in range(n):
    # Coordinate casuali 
    x = randrange(lato, 500 - lato)
    y = randrange(lato, 500 - lato)

    
    colore = (randrange(256), randrange(256), randrange(256)) # Colore casuale (RGB)
    
    g2d.set_color((128, 128, 128))  # Colore grigio per l'ombra
    g2d.draw_rect((x +5, y +5), (lato, lato))  # Disegna l'ombra

    # Disegna il quadrato pieno
    g2d.set_color(colore)
    g2d.draw_rect((x, y), (lato, lato)) 


# Mostra il disegno e mantiene aperta la finestra
g2d.main_loop()
