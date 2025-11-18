import g2d
from actor import Point

with open("/Users/thiam/Unipr-LINTINF/Basi informatica-Tomaiuolo/es8 17.11.2025/colori.txt") as color:
    colors = []
    for row in color:
        splitted = row.split(",")
        col = [int(v) for v in splitted]
        r, g, b = col
        colors.append((r, g, b))

def rec_circles(p: Point, r: float, level: int, skip_dir=(0,0)):
    if r <= 5 or level == 0:
        return

    color_index = level % len(colors)
    g2d.set_color(colors[color_index])

    g2d.draw_circle(p, r)

    px, py = p
    new_r = r * (2**0.5 - 1)

    directions = [(1,1),(-1,1),(1,-1),(-1,-1)]

    for dx, dy in directions:
        if (dx, dy) == skip_dir:
            continue

        new_p = (px + dx*r, py + dy*r)
        rec_circles(new_p, new_r, level-1, skip_dir=(-dx, -dy))


def main():
    g2d.init_canvas((500,500))
    p = (500/2,500/2)
    r = float(input("Raggio: "))
    MAX_level = 4
    rec_circles(p, r, MAX_level)
    g2d.main_loop()

main()