import random
class Node:
    def depth(self):
        pass
    def largest(self):
        pass
    pass

class Document(Node):
    def __init__(self, name: str, text: str): 
        self._name = name
        self._text = text
    
    def depth(self):
        return 0
    
    def largest(self):
        return len(self._text), f"{self._name}"

class Folder(Node):
    def __init__(self, name: str, subnodes: list[Node]):
        self._name = name
        self._subnodes = subnodes
    def depth(self):
        return 1 + max(a.depth()for a in self._subnodes)
    def largest(self):
        max_size = -1
        max_path = ""
        for a in self._subnodes:
            max_size0, max_path0 = a.largest()
            if max_size0 > max_size:
                max_size = max_size0
                max_path = max_path0

        return max_size, f"{self._name}/{max_path}"

def main():
    prod = Document("prod.csv", "1,2,3,4")
    data = Folder("data", [prod])
    a1_0 = Document("a1.txt", "bla bla 0")
    work = Folder("Work", [a1_0, data])
    a1_1 = Document("a1.txt", "a different file")
    personal = Folder("Personal", [a1_1])
    desktop = Folder("Desktop", [work, personal])

    lis = [prod, data, a1_0, work, a1_1, personal, desktop]
    for a in lis:
        x = a.largest()
        print(x)

if __name__ == "__main__":
    main()
