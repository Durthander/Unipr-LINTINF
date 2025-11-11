#CONTEGGIO NORMALE DI LEVEL
# import g2d

# def draw_sierp(x, y, w, h, level):
#     if w <= 5 or h <= 5 or level == 5:
#         return
#     w2 = w/2
#     h2 = h/2
#     size2 = (w2, h2)
#     g2d.draw_rect((x, y), size2)

#     draw_sierp(x + w2, y, w2, h2, level + 1)
#     draw_sierp(x, y+ h2, w2, h2, level + 1)
#     draw_sierp(x + w2, y + h2, w2, h2, level + 1)


# W, H = 512, 512
# g2d.init_canvas((W, H))
# g2d.set_color((0, 0, 0))
# g2d.draw_rect((0, 0), (W, H))
# g2d.set_color((255, 255, 255))
# draw_sierp(0, 0, W, H, 0)
# g2d.main_loop() 

'''CONTEGGIO ALLA ROVESCIA'''   
import g2d

def draw_sierp(x, y, w, h, level):
    if w <= 5 or h <= 5 or level == 0:
        return
    w2 = w/2
    h2 = h/2
    size2 = (w2, h2)
    g2d.draw_rect((x, y), size2)

    draw_sierp(x + w2, y, w2, h2, level - 1)
    draw_sierp(x, y+ h2, w2, h2, level - 1)
    draw_sierp(x + w2, y + h2, w2, h2, level - 1)


W, H = 512, 512
g2d.init_canvas((W, H))
g2d.set_color((0, 0, 0))
g2d.draw_rect((0, 0), (W, H))
g2d.set_color((255, 255, 255))
draw_sierp(0, 0, W, H, 5)
g2d.main_loop()    
