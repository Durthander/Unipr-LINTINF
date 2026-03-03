
def clamp(lst: list, t: float) -> list:

    if t == None:
        return lst
    
    result = [min(v,t) for v in lst]
    # for v in lst:
    #     if v >= t:
    #         result.append(t)
    #     else:
    #         result.append(v)

    return result


def main():
    s = [2, 3, 5, 1, 4]
    t = 3
    r = clamp(s, t)
    print(r)

main()

