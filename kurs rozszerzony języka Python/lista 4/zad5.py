import itertools
import operator

def kryptarytm(A,B,C,f):
    litery = set()
    w = []
    for l in A+B+C:
        litery.add(l)
    
    for perm in itertools.permutations(range(0,10), len(litery)):
        d = {}
        for l,v in zip(litery,perm):
            d[l] = v
        
        a,b,c=0,0,0
        for l in A:
            a = 10*a + d[l]
        for l in B:
            b = 10*b + d[l]
        for l in C:
            c = 10*c + d[l]

        if f(a,b) == c:
            w.append(d) 
    return w

print("kioto + osaka = tokio")
for s in kryptarytm("kioto","osaka","tokio",operator.add):
    print(s)
print()
print("a * b = c")
for s in kryptarytm("a","b","c",operator.mul):
    print(s)
