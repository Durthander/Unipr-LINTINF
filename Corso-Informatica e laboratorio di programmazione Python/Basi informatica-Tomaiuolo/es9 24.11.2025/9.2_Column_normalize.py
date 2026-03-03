import csv

m = []

with open("Basi informatica-Tomaiuolo/es9 24.11.2025/Matrix.csv", "r") as mat:
        for row in mat:
            m.append([int(v) for v in row.strip().split(",")])

m2 = [[0 for _ in range(len(m[0]))] for _ in range(len(m))]

for i in range(len(m[0])):
    col = [row[i] for row in m]
    print("Colonna", i, ":", col)
    print("Max =", max(col))
    print("Min =", min(col))

    for a in range(len(m)):
        b = m[a][i]
        v_n = (b - min(col)) / (max(col) - min(col))
        #v_n = min(max(0, (b - min(col))/(max(col) - min(col))), 1)
        m2[a][i] = v_n

with open("Basi informatica-Tomaiuolo/es9 24.11.2025/Matrix_norm.csv", "w", newline="") as out:
    writer = csv.writer(out)
    for row in m2:
        writer.writerow(row)