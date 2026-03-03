type T = int | list[T]

def compute_tree(t: T) -> int:
    if isinstance(t, int):
        return t 
    result = 0
    for n in t:
        v = compute_tree(n)
        result += v
    
    return result

def count_in_tree(t: T, v0) -> int:
    if isinstance(t, int):
        if t == v0:
            return 1
        else:
            return 0
    counts = 0
    
    for n in t:
        v = count_in_tree(n, v0)
        counts += v
    
    return counts


print(compute_tree([1, [2, 3], [3]]))
print(count_in_tree([1, [2, 3], [3]], 3))