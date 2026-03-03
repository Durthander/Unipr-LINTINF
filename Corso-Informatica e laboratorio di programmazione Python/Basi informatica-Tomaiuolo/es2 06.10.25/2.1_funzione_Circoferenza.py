import math 

def circonferenza(r):
    if r < 0:
        print("Value Error")
    else:
        return 2 * math.pi * r

def main():
    r = float(input("Inserisci il raggio della circonferenza: "))
    c = circonferenza(r)
    print(f"La circonferenza di raggio {r} è {c}")    

main()
