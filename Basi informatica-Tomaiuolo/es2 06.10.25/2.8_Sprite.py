import g2d
import math
from random import randrange

H, W = 400, 400
g2d.init_canvas((W, H))

x, y0 = 200, H // 2
dx = 2 
a = 30 # ampiezza dell'oscillazione
p = 30 # periodo dell'oscillazione

sprite1 = (20 , 0)
sprite2 = (20 , 20)

visibile = True

def casuale():
    global visibile, x
    if (x - dx) % 20 >= x % 20 and randrange(3) == 0:
        visibile = not visibile


def tick():
    global x, y, dx, sprite1, sprite2, visibile
    g2d.clear_canvas()
    y = y0 + a * math.sin(2 * math.pi * x / p)

    casuale()
    
    if visibile:
        sprite = sprite1
    
    else:
        sprite = sprite2

    
    g2d.draw_image("sprites.png", (x , y) , (sprite), (20 ,20))
    
    x += dx

    if x > W:
        x = 0

g2d.main_loop(tick)
