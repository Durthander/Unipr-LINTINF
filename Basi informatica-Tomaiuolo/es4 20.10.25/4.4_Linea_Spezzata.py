from math import sin, cos, radians
from random import randint
import g2d

Point = tuple[float, float]  # Pt in cartesian coords (x, y)
Polar = tuple[float, float]  # Pt in polar coords (r, angle)

g2d.init_canvas((400, 400))

def from_polar(plr: Polar) -> Point:
    r, ang = plr
    a = radians(ang)
    return (r * cos(a), r * sin(a))

def move_around(p1: Point, length: float, ang: float) -> Point:
    x0, y0 = p1
    dx, dy = from_polar((length, ang))
    return (x0 + dx, y0 + dy)

def randline(p1: Point):
    length = 100
    ang = randint(0, 360)

    # Calcola p2 a distanza 100 da p1
    p2 = move_around(p1, length, ang)

    g2d.draw_line(p1, p2)
    return p2

  

def main():
    n = int(input("numero: "))
    p = (200, 200)  # punto iniziale casuale
    for _ in range(n):
        p = randline(p)
    g2d.main_loop()

main()
