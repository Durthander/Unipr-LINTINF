
import g2d
from random import randrange


H = W = 400
positions = []  

g2d.init_canvas((H, H))

while True:
    color = (randrange(256), randrange(256), randrange(256))
    posx, posy = randrange(W - 20), randrange(H - 20)

    # Controlla direttamente se il nuovo quadrato toccherebbe uno precedente
    overlaps = False
    for px, py in positions:
        separated = (
            px + 20 <= posx or posx + 20 <= px or
            py + 20 <= posy or posy + 20 <= py
        )
        if not separated:
            overlaps = True
            break

    if overlaps:
        break

    positions.append((posx, posy))
    g2d.set_color(color)
    g2d.draw_rect((posx, posy), (20,20))
    g2d.update_canvas()
