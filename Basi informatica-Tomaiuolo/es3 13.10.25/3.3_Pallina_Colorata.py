ARENA_W, ARENA_H, BALL_W, BALL_H = 480, 360, 20, 20
from random import randrange

class quadrati_colorati:
    def __init__(self, x0: int, y0: int):
        self._x = x0
        self._y = y0
        self._dx, self._dy = 4, 4
        self.color = (randrange(256), randrange(256), randrange(256))

    def colore(self):
        return self.color  

    def move(self):
        if not 0 <= self._x + self._dx <= ARENA_W - BALL_W:
            self._dx = -self._dx
            self.color = (randrange(256), randrange(256), randrange(256))
        if not 0 <= self._y + self._dy <= ARENA_H - BALL_H:
            self._dy = -self._dy
            self.color = (randrange(256), randrange(256), randrange(256))
        self._x += self._dx
        self._y += self._dy
    

    def pos(self):
        return self._x, self._y


def tick():
    g2d.clear_canvas()  # BG
    g2d.set_color(q1.colore())
    g2d.draw_rect(q1.pos(), (20, 20))

    g2d.set_color(q2.colore())
    g2d.draw_rect(q2.pos(), (20, 20)) 

    g2d.set_color(q3.colore())
    g2d.draw_rect(q3.pos(), (20, 20))
    
    q1.move()
    q2.move()
    q3.move()    
    
def main():
    global g2d , q1 , q2 , q3
    import g2d  # Ball does not depend on g2d
    q1 = quadrati_colorati(50, 50)
    q2 = quadrati_colorati(200, 150)
    q3 = quadrati_colorati(300, 250)

    g2d.init_canvas((ARENA_W, ARENA_H))
    g2d.main_loop(tick)

main()
