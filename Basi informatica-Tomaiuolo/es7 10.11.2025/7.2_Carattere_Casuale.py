from random import randrange
def randchar(a: str, b: str)->str:
    a0 = ord(a)
    b0 = ord(b)
    if a0 <= b0:
        y = randrange(a0, b0 + 1)
        return chr(y)
    else:
        y = randrange(b0, a0 + 1)
        return chr(y)

def main():
    a = input("primo carattere: ")
    b = input("secondo carattere: ")
    x = randchar(a, b)
    print(x)

main()