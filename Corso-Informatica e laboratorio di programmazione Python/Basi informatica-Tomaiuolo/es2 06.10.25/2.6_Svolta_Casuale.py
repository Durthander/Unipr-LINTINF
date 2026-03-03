import g2d
from random import randrange

H, W = 400, 400
g2d.init_canvas((W, H))

x, y = 200, 200
dx, dy = 2, 0 

def nuova_direzione():
    direzione = randrange(4)  # numero casuale 0, 1, 2 o 3
    if direzione == 0:
        return (2, 0)   # destra
    elif direzione == 1:
        return (-2, 0)  # sinistra
    elif direzione == 2:
        return (0, 2)   # giù
    else:
        return (0, -2)  # su

def tick():
    global x, y, dx, dy

    g2d.clear_canvas()
    g2d.draw_image("ball.png", (x, y))
    
    x += dx
    y += dy


    if x % 20 == 0 and y % 20 == 0:
        dx, dy = nuova_direzione()  

g2d.main_loop(tick)
