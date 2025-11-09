import g2d

def draw_figure(centro, r, n):
    x, y = centro
    for i in range(n):
        r = r * (1 - i / n)
        gray = int(255 * i / (n - 1)) if n > 1 else 0
        color = (gray, gray, gray)
        g2d.set_color(color)
        g2d.draw_circle((x, y), r)

def main():
    n = int(input("Inserisci il numero di cerchi concentrici per figura: "))
    g2d.init_canvas((500, 500))

    step = (500 / n)
    r = step / 2 

    for i in range(n):
        centro = (step * i + step / 2, 250)
        draw_figure(centro, r, n)

    g2d.main_loop()

main()
