import g2d
import math

H, W = 400, 400
g2d.init_canvas((W, H))

x, y0 = 200, H // 2
dx = 2 
a = 10 # ampiezza dell'oscillazione
p = 80 # periodo dell'oscillazione

def tick():
    global x, y, dx

    y = y0 + a * math.sin(2 * math.pi * x / p)

    g2d.clear_canvas()
    g2d.draw_image("ball.png", (x, y))
    
    x += dx

    if x > W:
        x = 0

g2d.main_loop(tick)
