from random import choice, randrange
from actor import Actor, Arena, Point
arena_w , arena_h = 900 , 506
VIEW_W , VIEW_H = 400 , 400
view_x , view_y = 0, 0


class Ball(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 20, 20
        self._dx, self._dy = 4, 4

    def move(self, arena: Arena):
        for other in arena.collisions():
            if not isinstance(other, Ball):
                x, y = other.pos()
                if x < self._x:
                    self._dx = abs(self._dx)
                else:
                    self._dx = -abs(self._dx)
                if y < self._y:
                    self._dy = abs(self._dy)
                else:
                    self._dy = -abs(self._dy)

        arena_w, arena_h = arena.size()
        if self._x + self._dx < 0:
            self._dx = abs(self._dx)
        elif self._x + self._dx > arena_w - self._w:
            self._dx = -abs(self._dx)
        if self._y + self._dy < 0:
            self._dy = abs(self._dy)
        elif self._y + self._dy > arena_h - self._h:
            self._dy = -abs(self._dy)

        self._x += self._dx
        self._y += self._dy

    def pos(self) -> Point:
        return self._x - view_x, self._y - view_y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return 0, 0

def tick():
    global view_x, view_y
    g2d.clear_canvas()
    
    g2d.draw_image("completo.jpg", (-view_x,-view_y))
    for a in arena.actors():
        if a.sprite() != None:
            g2d.draw_image("sprites.png", a.pos(), a.sprite(), a.size())
    
    keys = g2d.current_keys()
    if "ArrowLeft" in keys:
        view_x -= 10
    elif "ArrowRight" in keys:
        view_x += 10
    if "ArrowUp" in keys:
        view_y -= 10
    elif "ArrowDown" in keys:
        view_y += 10
    
    view_x = max(0, min(view_x, arena_w - VIEW_W))
    view_y = max(0, min(view_y, arena_h - VIEW_H))


    arena.tick(keys)  # Game logic


def main():
    global g2d, arena
    import g2d  # game classes do not depend on g2d

    arena = Arena((arena_w , arena_h ))
    arena.spawn(Ball((40, 80)))
    arena.spawn(Ball((80, 40)))
    

    g2d.init_canvas((VIEW_W , VIEW_H))
    g2d.main_loop(tick)

if __name__ == "__main__":
    main()
