from random import shuffle
import csv

w, h = map(int, input("Dimensioni w(n di colonne) e h(n di righe:\nw h: ").split())

nums = [a + 1 for a in range(w * h)]
shuffle(nums)

matrix = [nums[i*w:(i+1)*w] for i in range(h)]

with open("Basi informatica-Tomaiuolo/es9 24.11.2025/Matrix.csv", "w", newline="") as mat:
    writer = csv.writer(mat)
    for row in matrix:
        writer.writerow(row)