import g2d
from random import randrange , choice

H, W = 400, 400


x, y = 200, 200
dx, dy = 2, 0 

class RandomWalker:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 2
        self.dy = 0

    def nuova_direzione(self):
        direzione = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        direzione.remove(self.direzione_opposta())
        return choice(direzione)
    
    def direzione_opposta(self):
        return (-self.dx, -self.dy)
    
    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x % 20 == 0 and self.y % 20 == 0:
            self.dx, self.dy = self.nuova_direzione()
    
    def pos(self):
        return (self.x, self.y)

walker = RandomWalker(200, 200)

def tick():
    g2d.clear_canvas()
    g2d.draw_image("ball.png", walker.pos())
    walker.move()
    
    
def main():
    g2d.init_canvas((W, H))
    g2d.main_loop(tick)

main()