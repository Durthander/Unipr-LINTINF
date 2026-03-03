def main():
    t = input("Inserisci un testo: ")
    print(all_alpha(t))

def all_alpha(t):
    """Restituisce True se tutti i caratteri della stringa t sono alfabetici (lettere), False altrimenti."""
    for testo in t:
        if not testo.isalpha():
            return False
    return True

main()