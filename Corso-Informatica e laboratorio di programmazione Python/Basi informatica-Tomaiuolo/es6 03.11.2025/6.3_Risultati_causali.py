from random import randint
n = int(input("numero a caso: "))

result = [0] * 13

for _ in range(n):
    r1 = randint(0, 6)
    r2 = randint(0, 6)

    add = r1 + r2
    result[add] += 1
    
print(f"Risultati: {result}")




