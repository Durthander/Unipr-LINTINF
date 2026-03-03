import g2d
from random import randrange
g2d.init_canvas((500,500))

def quadrati(x, y, lato, livello):
    if livello == 0:
        pass
    else:
        g2d.set_color((randrange(256),randrange(256),randrange(256)))
        g2d.draw_rect((x, y), (lato, lato))
    
        quadrati(x + lato/4, y + lato/4, lato/2, livello-1)

def main():
    quadrati(100,100,80,3)
    g2d.main_loop()

main()
        