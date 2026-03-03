from operator import itemgetter
import re

with open("Basi informatica-Tomaiuolo/es9 24.11.2025/g2d.py", "r") as file:
    text = file.read() #tutto il file
    #words = text.split()
    words = re.split(r"\W+", text)
    #creaiamo un dizionario per contare le parole
    counts = {}
    
    for w in words:
        if w in counts:
            counts[w] += 1 #in counts non ci sono parole, quindi count[w] non ha senso
        else:
            counts[w] = 1

results = list(counts.items())
results.sort(key=itemgetter(1), reverse=True) #itemgetter da riguardare

#voglio stampare solo le prime dieci

print(results[:10])
