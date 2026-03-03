def count_groups(s):
    lettere_AM = 0
    lettere_NZ = 0

    for c in s:
        if ('A' <= c <= 'M') or ('a' <= c <= 'm'):
            lettere_AM += 1
        elif 'N' <= c <= 'Z' or 'n' <= c <= 'z':
            lettere_NZ += 1
    return lettere_AM, lettere_NZ

def main():
    s = input("Inserisci una stringa: ")
    
    while s != "":
        am, nz = count_groups(s)
        print(f"Lettere da A a M: {am}")
        print(f"Lettere da N a Z: {nz}")
        s = input("Inserisci una stringa: ")
main()

