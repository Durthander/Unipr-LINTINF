from math import cos, radians, sin
from os import name
from random import randint

import g2d

Point = tuple[float, float]  # Pt in cartesian coords (x, y)
Polar = tuple[float, float]  # Pt in polar coords (r, angle)

def from_polar(plr: Polar) -> Point:
    r, ang = plr
    a = radians(ang)
    return (r * cos(a), r * sin(a))

def move_around(p1: Point, length: float, ang: float) -> Point:
    x0, y0 = p1
    dx, dy = from_polar((length, ang))
    return (x0 + dx, y0 + dy)

def poly_vertices(p, r, n, a0 = 0):
    result = []
    delta = 360 / n
    for i in range(n):
        a = i * delta + a0
        v = move_around(p, r, a)
        result.append(v)
    return result

angle0 = 0

def tick():
    global angle0
    g2d.clear_canvas()
    vs = poly_vertices((200, 200), 150, 6, angle0)
    # g2d.set_color((0, 0, 0))
    # g2d.draw_polygon(vs)
    n = len(vs)
    for i in range(n):
        pt1 =  vs[i] #vs[i - 1]
        # j = i + 1
        # if j >= n:
        #     j = 0
        pt2 = vs[(i + 1) % n]
        #pt2 = vs[i]
        g2d.draw_line(pt1, pt2)
        g2d.draw_text(str(i), pt1, 20)
    angle0 += 1
def main():
    g2d.init_canvas((400,400))
    g2d.main_loop(tick)

if __name__ == "__main__":
    main()