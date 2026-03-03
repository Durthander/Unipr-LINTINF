import g2d

with open("/Users/thiam/Unipr-LINTINF/Basi informatica-Tomaiuolo/es8 17.11.2025/colori.txt") as color:
    colors = []
    for row in color:
        splitted = row.split(",")
        col = [int(v) for v in splitted]
        r, g, b = col
        colors.append((r, g, b))

def main():
    H = W = 400
    r = 200
    g2d.init_canvas((H, W))
    n = int(input("Scegli un numero: "))
    for i in range(4):
        g2d.set_color(colors[(i+1)%3])
        g2d.draw_circle((H/2,H/2), r - (200/n)*i)
    g2d.main_loop()
main()
