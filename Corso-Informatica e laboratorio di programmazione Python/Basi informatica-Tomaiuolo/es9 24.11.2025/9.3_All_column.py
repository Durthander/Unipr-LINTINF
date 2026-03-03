from random import randrange

w, h = map(int, input("Dimensioni w(n di colonne) e h(n di righe:\nw h: ").split())

matrix = []

for y in range(h):
    for x in range(w):
        matrix.append(randrange(10))
        end_ = "\n" if x == w - 1 else ","
        print(matrix[x + y * w], end=end_)

# Trova i numeri presenti in tutte le colonne
common_0 = []

# numeri possibili che potrebbero essere in tutte le colonne
for r in range(h):
    v = matrix[0 + r * w]
    if v not in common_0:
        common_0.append(v)

# confronta con ogni colonna successiva
for col in range(1, w):
    col_vals = [matrix[col + r * w] for r in range(h)]
    common = []
    for v in common_0:
        if v in col_vals:
            common.append(v)
    common = common

print("Numeri presenti in tutte le colonne:", common)

#counts = Counter(re.split(r"\W+", file.read()))
#print(counts.most_common(10))