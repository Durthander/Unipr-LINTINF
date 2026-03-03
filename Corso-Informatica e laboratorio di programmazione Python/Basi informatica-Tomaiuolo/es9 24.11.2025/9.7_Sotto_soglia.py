def all_below(data: list[int], n: int):
    if data == []:
        return True
    
    head = data[0]
    tail = data[1:]
    if head > n:
        return False
    else:
        return all_below(tail, n)
    
data = [1, 4, 2, 8, 3, 6, 0, 5]
b = all_below(data, 4)
print(b)