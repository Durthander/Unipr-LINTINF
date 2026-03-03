def somma(lst: list[int]) -> int:
    if not lst:
        return 0
    first, *other = lst 
    return first + somma(other) 

def main():
    lst = [1,2,3]
    r = somma(lst)
    print(r)

main()