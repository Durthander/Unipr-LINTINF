class Expression:
    def eval(self) -> float:
        raise NotImplementedError("Abstract Method")

class Literal(Expression):
    def __init__(self, v):
        self._val = v

    def eval(self) -> float:
        return self._val

class Sum(Expression):
    def __init__(self, a: Expression, b: Expression):
        self._a = a
        self._b = b
    
    def eval(self) -> float:
        av = self._a.eval()
        bv = self._b.eval()
        return av + bv

class Product(Expression):
    def __init__(self, a: Expression, b: Expression):
        self._a = a
        self._b = b
    
    def eval(self) -> float:
        av = self._a.eval()
        bv = self._b.eval()
        return av * bv

# 5 * ((3 * 2) +4) 
l2 = Literal(2)   
l3 = Literal(3)
l5 = Literal(5)
l4 = Literal(4)

p32 = Product(l3, l2)
sum_ = Sum(p32, l4)
prod = Product(l5, sum_)

print(f"fa {prod.eval()}")