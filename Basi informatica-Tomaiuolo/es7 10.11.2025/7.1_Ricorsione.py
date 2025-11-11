def recursive_pow(x: int, n: int)->int:
    if n == 0:
        return 1
    else:
        return x*recursive_pow(x, n-1)

def main():
    x = int(input("scegli un numero: "))
    n = int(input("scegli la potenza: "))

    a = recursive_pow(x, n)
    print(a)

main()