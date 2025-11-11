import g2d
from actor import Point

def rec_circles(p: Point, r: float):
    if r <= 5:
        return None
    else:
        g2d.draw_circle(p , r)
        px ,py = p
        rec_circles((px+r,py+r), (r*(2**(1/2)-1)))           
        rec_circles((px-r,py-r), (r*(2**(1/2)-1)))
        rec_circles((px+r,py-r), (r*(2**(1/2)-1)))
        rec_circles((px-r,py+r), (r*(2**(1/2)-1)))   

    

def main():
    g2d.init_canvas((500,500))
    p = (500/2,500/2)
    r = float(input("Raggio: "))
    rec_circles(p,r)
    g2d.main_loop()

main()