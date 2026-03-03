def shout(s: str) -> str:
    result = ""
    uppering = False
    for a in s:
        if a == "*":
            uppering = not uppering
        else:
            if uppering:
                result += a.upper()
            else:
                result += a
    return result

def main():
    s = input("Scrivi una stringa con asterischi dove si vuole mettere in uppercase: ")
    x = shout(s)
    print(x)

main()