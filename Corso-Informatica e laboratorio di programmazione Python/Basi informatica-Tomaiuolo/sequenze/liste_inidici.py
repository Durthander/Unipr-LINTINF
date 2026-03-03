groceries = ["spam", "egg", "beans", "bacon"]
n = len(groceries)           # 4
groceries[0]                 # "spam"
groceries[1]                 # "egg"
groceries[n-1]               # "bacon"
groceries[1] = "ketchup"     # replace a value, len is still 4
groceries.append("sausage")  # add to the end, len is 5
groceries                    # guess!

print(groceries)

#INDICI NEGATIVI
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
n = len(months)            # 12
months[3]                  # "Apr"
months[-2]                 # "Nov", same as n - 2
spring = months[2:5]       # ["Mar", "Apr", "May"]
quart1 = months[:3]        # ["Jan", "Feb", "Mar"]
quart4 = months[-3:]       # ["Oct", "Nov", "Dec"]
whole_year = months[:]     # Copy of the whole list

# Indici negativi contano dalla fine
# Da -1 (ultimo) a -len(s) (primo)

#INSERIMENTO E RIMOZIONE
groceries = ["spam", "egg", "beans"]

groceries[0] = "sausage"      # replace an element

groceries.append("bacon")     # add an element to the end
groceries.pop()               # remove (and return) last element

groceries.insert(1, "bacon")  # other elements shift
removed = groceries.pop(1)    # remove (and return) element at index

i = groceries.index("egg")    # 1, index of "egg" in groceries
if "egg" in groceries:        # True, groceries contains "egg"
    groceries.remove("egg")   # remove an element by value

groceries.clear()             # remove everything, groceries is empty now

# Uguaglianza e identità
a = ["spam", "egg", "beans"]
b = a[:]         # new list!
b == a           # True, they contain the same values
b is a           # ❗ False, they are two objects in memory
                 # (try and modify one of them...)
c = a
c is a           # ❗ True, same object in memory
                 # (try and modify one of them...)
d = ["sausage", "tomato"]
groceries = c + d  # list concatenation --> new list!

# Lexicographical comparison of lists (or strings, tuples...)
# Compare the first two *different* elements
[2, 0, 0] > [1, 2, 0]  # True: 2 > 1
[2, 1, 0] > [2, 0, 1]  # True: 2 == 2, 1 > 0

#FUNZIONI SU LISTE
def append_fib(data: list[int]):
    val = len(data)
    if val >= 2:
        val = data[-2] + data[-1]
    data.append(val)

def main():
    values = []
    for _ in range(12):
        append_fib(values)
        print(values)  # let's see what's going on

main()

# STRINGHE E LISTE
# - Stringa: sequenza immutabile di caratteri
txt = "Monty Python's Flying Circus"
txt[3]    # "t"
txt[-2]   # "u"
txt[6:12] # "Python"
txt[-6:]  # "Circus"
# - join : da lista di stringhe a stringa unica
# - split : da stringa unica a lista di stringhe -> Separa in base  a caratteri bianchi, o se impostato con " ", "\n" e "\t"
whole = "|".join(["tue", "thu", "sat"])  # "tue|thu|sat"
days = "mon|wed|fri".split("|")  # ["mon", "wed", "fri"]