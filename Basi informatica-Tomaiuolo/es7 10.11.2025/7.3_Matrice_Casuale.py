import random
import string

def main():
    w = int(input("Inserisci la larghezza (w): "))
    h = int(input("Inserisci l'altezza (h): "))
    
    matrice = [random.choice(string.ascii_lowercase) for _ in range(w * h)]
    
    for y in range(w):
        for x in range(h):
            end_ = "\n" if x == h - 1 else ","
            print(matrice[x + y * h], end=end_)
    
    carattere = input("Scelgi un carattere: ")
    count_tot = matrice.count(carattere)
    count_bordo = 0
       
    for i in range(w):
            for j in range(h):
                if i == 0 or i == h - 1 or j == 0 or j == w - 1:
                    if matrice[i + j * h] == carattere:
                        count_bordo += 1    
        
    print(f"Occorrenze totali di '{carattere}': {count_tot}")
    print(f"Occorrenze nel bordo di '{carattere}': {count_bordo}")

main()
