
import math
from random import randrange

class Sprite_Oscillante:
    def __init__(self, x0: int, y0: int, ampiezza: int, periodo: int, velocita: int):
        self._x = x0
        self._y0 = y0
        self._y = y0
        self._ampiezza = ampiezza
        self._periodo = periodo
        self.dx = velocita
        self._visibile = True

    def move(self):
        self._y = self._y0 + self._ampiezza * math.sin(2 * math.pi * self._x / self._periodo)
        self._x += self.dx
        if self._x > W:
            self._x = 0
        self.visibile()
    
    def visibile(self):    
        if (self._x - self.dx) % 20 >= self._x % 20 and randrange(3) == 0:
            self._visibile = not self._visibile   

    def sprite(self):
        if self._visibile:
            sprite = (20, 0)
        else:
            sprite = (20, 20)
        return sprite
    
    def pos(self):
        return self._x, self._y
    
    def size(self):
        return (20, 20 )


def tick():
    g2d.clear_canvas()
   
    g2d.draw_image("sprites.png", (f1.pos()) , (f1.sprite()), (f1.size()))
    
    f1.move()


def main():
    global g2d , f1 , H , W
    import g2d
    H, W = 400, 400

    f1 = Sprite_Oscillante(200, 200, 10, 80, 2)

    g2d.init_canvas((W, H))
    g2d.main_loop(tick)

main()