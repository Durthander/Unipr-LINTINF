def digits(n: int) -> list[int]:
    dg = []
    if n == 0:
        return [0]
    while n > 0:
        dg.append(n % 10)
        n //= 10
    return dg

def main():
    n = input("n: ")
    r = digits(int(n))
    print(r)
    checks = 0

    for i, val in enumerate(r):
        checks += val * 10**i

    if checks == int(n):
        print("Sono uguali!")
    else:
        print(f"n è {int(n)} mentre la funzione da {checks} ")

        

main()
