def sum_digits(n: int)-> int:
    if n < 10:
        return n
    s = 0
    while n > 0:
        s += n % 10
        n //= 10
    
    return sum_digits(s)


n = int(input("Dimmi un numero: "))
print(sum_digits(n)) 
