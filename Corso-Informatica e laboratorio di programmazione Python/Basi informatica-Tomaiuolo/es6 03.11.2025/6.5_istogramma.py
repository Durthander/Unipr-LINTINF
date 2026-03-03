import g2d

H = W = 500


n = int(input("Serie di numeri positivi (inserirne uno negativo per fermare): "))
seq = []
while n >= 0:
    seq.append(n) 
    n = int(input("Serie di numeri positivi (inserirne uno negativo per fermare): "))

g2d.init_canvas((H,H))

max_val = max(seq)
bar_h = H / len(seq)
y = 0

for v in seq:
    bar_w = (v / max_val) * W
    g2d.set_color((0, 0, 255))
    g2d.draw_rect((0, y), (bar_w, bar_h))
    y += bar_h

g2d.main_loop()