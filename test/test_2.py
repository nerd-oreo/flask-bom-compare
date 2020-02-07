class Item:
    n = 0
    def __init__(self, n):
        self.n = n
    
    def compare(self, item):
        return self.n == item.n
        
dictA = {
    'a': Item(10),
    'z': Item(5),
    'm': Item(2),
    'p': Item(10),
    'r': Item(130),
    'c': Item(68),
    'x': Item(92),
}

listA = ['a','z','m','p','r','c','x']

dictB = {
    'a': Item(10),
    'l': Item(9),
    'z': Item(5),
    'r': Item(130),
    'p': Item(10),
    't': Item(31),
    'b': Item(45),
    'j': Item(57),
    'k': Item(9),
}

listB = ['a','z','l','p','r','c','t', 'b', 'j', 'k']

onlyInA = list()
onlyInB = list()
inAB = list()

lA = len(listA)
lB = len(listB)

# compare A to B
for i in range(lA):
    if listA[i] in listB:
        iB = listB.index(listA[i])
        inAB.append(listA[i])
    else:
        onlyInA.append(listA[i])

for el in listB:
    if el not in inAB:
        onlyInB.append(el)

print('A:', listA)
print('B:', listB)
print('onlyInA:', onlyInA)
print('onlyInB:', onlyInB)
print('inAB:', inAB)