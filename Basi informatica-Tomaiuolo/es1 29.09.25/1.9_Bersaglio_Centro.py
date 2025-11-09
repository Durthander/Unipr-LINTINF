import g2d
from random import randrange, randint
canvas = 500

g2d.init_canvas((canvas , canvas))

n = randint(0,200)
r = 20

centro = (canvas //2, canvas //2)

while True:
    x = randrange(r, canvas - r)
    y = randrange(r, canvas - r)
    rgb = (randint(0,255), randint(0,255), randint(0,255))
    g2d.set_color(rgb)
    g2d.draw_circle((x,y), r)

    distanza = ((x - centro[0])**2 + (y - centro[1])**2)**0.5
    if distanza <= r:
        print(f"Hai colpito il bersaglio! Il cerchio è centrato in {centro} con raggio {r}.")
        break

g2d.main_loop()
    

