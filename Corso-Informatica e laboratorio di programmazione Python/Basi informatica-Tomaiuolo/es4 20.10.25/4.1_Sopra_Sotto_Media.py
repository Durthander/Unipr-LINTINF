numeri = []
def media(numeri):
    sum = 0    
    for i in numeri:
        sum += i
    return sum / len(numeri)

    
def sopra_o_sotto_media():
    m = media(numeri)
    sopra_media = []
    sotto_media = []
    for a in numeri:
        if a >= m:
            sopra_media.append(a)
        else:
            sotto_media.append(a)
    return sopra_media , sotto_media

def main():
    n = int(input("Scegli una serie di numeri(0 per annullare):"))
    tot = []
    while n != 0:
        numeri.append(n)
        n = int(input("Scegli una serie di numeri(0 per annullare):"))
    
    m = media(numeri)
    ab , cd = sopra_o_sotto_media()
    print(f"La media è {m}")
    print(f"I numeri sopra la media sono {ab}")
    print(f"I numeri sotto la media sono {cd}")

main()
    
        