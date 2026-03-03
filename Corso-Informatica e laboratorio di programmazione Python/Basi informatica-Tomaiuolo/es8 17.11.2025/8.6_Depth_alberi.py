class Node:
    def depth(self):
        pass
    pass

class Document(Node):
    def __init__(self, name: str, text: str): 
        self._name = name
        self._text = text
    
    def depth(self):
        return 0

class Folder(Node):
    def __init__(self, name: str, subnodes: list[Node]):
        self._name = name
        self._subnodes = subnodes
    def depth(self):
        return 1 + max(a.depth()for a in self._subnodes)

def main():
    prod = Document("prod.csv", "1,2,3,4")
    data = Folder("data", [prod])
    a1_0 = Document("a1.txt", "bla bla 0")
    work = Folder("Work", [a1_0, data])
    a1_1 = Document("a1.txt", "a different file")
    personal = Folder("Personal", [a1_1])
    desktop = Folder("Desktop", [work, personal])

    # x = desktop.depth()
    # print(x)

if __name__ == "__main__":
    main()
