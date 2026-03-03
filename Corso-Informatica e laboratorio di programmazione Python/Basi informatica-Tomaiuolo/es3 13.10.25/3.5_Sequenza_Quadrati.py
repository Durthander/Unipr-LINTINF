import g2d

W, H = 500, 500

class SeqQuadrati:
    def __init__(self, n):
        self._n = n

    def lato(self, i):
        """Ritorna il lato del quadrato i-esimo (decrescente)"""
        return W * (self._n - i) / self._n

    def colore(self, i):
        """Ritorna il colore del quadrato i-esimo (gradiente nero->verde)"""
        t = i / (self._n - 1) if self._n > 1 else 1
        green = int(255 * t)
        return (0, green, 0)

    def draw(self):
        """Disegna tutti i quadrati sul canvas"""
        g2d.clear_canvas()
        for i in range(self._n):
            lato = self.lato(i)
            g2d.set__color(self.colore(i))
            g2d.draw_rect((0, 0), (lato, lato))


def main():
    n = int(input("Inserisci un numero intero positivo: "))
    seq = SeqQuadrati(n)
    g2d.init_canvas((W, H))
    seq.draw()
    g2d.main_loop()

main()
