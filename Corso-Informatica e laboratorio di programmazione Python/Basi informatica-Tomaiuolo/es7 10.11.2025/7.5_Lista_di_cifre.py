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

    while n != "":
        r = digits(int(n))
        print(r)
        print()
        n = input("n: ")

main()
