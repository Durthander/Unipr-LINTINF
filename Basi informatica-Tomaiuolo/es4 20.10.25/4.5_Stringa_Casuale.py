import random
import string

s = input("Inserisci un testo: ")
def add_letter(s):
    return s + random.choice(string.ascii_lowercase)

def main():
    global s
    n = int(input("numero: "))
    for _ in range(n):
        s = add_letter(s)
    print(s)
main()