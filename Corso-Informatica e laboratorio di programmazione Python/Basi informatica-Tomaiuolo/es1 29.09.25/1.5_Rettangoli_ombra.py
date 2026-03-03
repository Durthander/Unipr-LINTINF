import g2d
from random import randrange, randint

n = int(input("Quanti rettangoli vuoi disegnare? "))

g2d.init_canvas((500, 500))

lato = randint(101, 200)

for i in range(n):
    x = randrange(lato, 500 - lato)
    y = randrange(lato, 500 - lato)

    colore = (randrange(256), randrange(256), randrange(256))

    g2d.set_color((128, 128, 128))
    g2d.draw_rect((x + 5, y + 5), (lato, lato))

    g2d.set_color(colore)
    g2d.draw_rect((x, y), (lato, lato))

g2d.main_loop()
