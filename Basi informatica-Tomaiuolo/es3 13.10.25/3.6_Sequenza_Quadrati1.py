import g2d

W, H = 500, 500
m = 10 # margine

class SeqQuadrati:
    def __init__(self, n):
        self._n = n

    def lato(self, i):
        lato_max = W - 2 * m  # lato massimo considerando il margine destro e sinistro
        lato_min = lato_max / self._n
        if self._n > 1:
            return lato_max - i * (lato_max - lato_min) / (self._n - 1)
        else:
            return lato_max

    def colore(self, i):
    
        t = i / (self._n - 1) if self._n > 1 else 1
        green = int(255 * t)
        return (0, green, 0)

    def draw(self):
       
        g2d.clear_canvas()
        for i in range(self._n):
            lato = self.lato(i)
            x = W - lato - m
            y = m
            g2d.set_color(self.colore(i))
            g2d.draw_rect((x , y), (lato, lato))


def main():
    n = int(input("Inserisci un numero intero positivo: "))
    seq = SeqQuadrati(n)
    g2d.init_canvas((W, H))
    seq.draw()
    g2d.main_loop()

main()

