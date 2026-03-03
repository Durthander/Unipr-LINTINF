def pari(s: str) -> str:
    result = ""
    for a in range(len(s)):
        if a % 2 == 0:
            result += s[a]
    return result

def main():
    es = "abcdef"
    r = pari(es)
    print(r)

main()