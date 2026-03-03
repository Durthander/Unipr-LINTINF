numbers = {1, 4, 5}
numbers.add(4)  # {1, 4, 5}
few = numbers & {4, 5, 6}  # {4, 5}, intersection
many = numbers | {3, 4}  # {1, 3, 4, 5}, union

empty_set = set()  # ⚠️ {} is an empty dict -> rimuove duplicati dalla lista

#DIZIONARIO
# -Raccolta di coppie chiave-valore
# -Chiave: indice per accedere al valore
#   -Le chiavi sono uniche (~ list)
#   -Tipo str, o altro tipo immutabile
tel = {"john": 4098, "terry": 4139}  # dict[str, int]
if "john" in tel:
    print(tel["john"])  # 4098, ⚠️ error for a missing key
tel["graham"] = 4127
for k, v in tel.items():
    print(k, v)  # john 4098 ⏎ terry 4139 ⏎ graham 4127 ⏎

values = {(0, 0): 5, (1, 1): 8,
          (2, 2): 3, (1, 3): 6}  # dict[(int, int), int]

x = int(input("Col? "))
y = int(input("Row? "))
val = values.get((x, y), 0)  # key not found → default 0
print(val)