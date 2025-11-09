import g2d

H , W = 400, 400

g2d.init_canvas((H,W))
countdown = 0
dx = 2
x , y = 200, 200
    

def tick():
    global countdown, dx, x, y
    g2d.clear_canvas()
    g2d.draw_image("ball.png", (x,y))
    x += dx

    if countdown > 0:
        countdown -= 1
    else:
        dx = 2
    
    if countdown <= 0 and g2d.mouse_clicked():
        dx = 0
        countdown = 30

    elif countdown == 0:
        dx = 2



g2d.main_loop(tick)

