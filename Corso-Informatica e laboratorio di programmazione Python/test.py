class Num():
    def __init__(self, x):
        _x = x
    def sum(self):
        return self._x +self._x 

def main():
    a = Num(10)
    r = a.sum()
    print(r)
    
main()