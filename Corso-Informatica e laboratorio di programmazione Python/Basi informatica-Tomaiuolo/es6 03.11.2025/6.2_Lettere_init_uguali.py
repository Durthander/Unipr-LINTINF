def len_common_prefix(s: str, t: str) -> int:
    result = 0
    min_len = len(s) if len(s) <= len(t) else len(t)

    for n in range(min_len):
        if s[n] == t[n]:
            result += 1
        else:
            return result
    return result

def main():
    s = "carta"
    t = "carota"
    r = len_common_prefix(s, t)
    print(r)

main()