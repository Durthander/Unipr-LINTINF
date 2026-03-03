def select_char(s: str) -> str:
    result = ""
    for a in range(len(s)):
        if ord(s[a]) < ord(s[a-1]) or ord(s[a]) < ord(s[a+1]):
            result += ""
        else:
            result += s[a]
    return result

def main():
    t = "testo di prova"
    r = select_char(t)
    print(r)

main()