def estrai(text: str) -> str:
    result = ""
    writing = False
    
    for a in text:
        if a == "[" or a == "]":
            writing = not writing
        else:
            if writing:
                result += a
            elif a == " ":
                result += "\n"
    return result
                
def main():
    inp = "ciao [uno] testo [due]"
    r = estrai(inp)
    print(r)

main()