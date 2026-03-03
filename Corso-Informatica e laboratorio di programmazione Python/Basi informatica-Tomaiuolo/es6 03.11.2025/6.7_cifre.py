

def digits(t: int) -> list[int]:

    result = []
    for ch in str(t):
        result.append(int(ch))

    result.sort()
    return result


def main():
    t = 8765
    r = digits(t)
    print(r)

main()

