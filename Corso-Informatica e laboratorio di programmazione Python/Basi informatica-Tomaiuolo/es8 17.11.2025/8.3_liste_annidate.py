def find_max(s: str|list)->str:
    if not isinstance(s, list):
        return s
    max = ""
    for i in s:
        pmax = find_max(i)
        if pmax > max:
            max = pmax
    return(max)

s = ["Ann", ["Bart", ["Carol", "Cindy"], "Bob", "Art"],["Bea"], "Bill"]
print(find_max(s))
