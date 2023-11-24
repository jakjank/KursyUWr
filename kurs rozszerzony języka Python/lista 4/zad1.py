import timeit

def pierwsze_imperatywna(n):
    i = 2
    w = []
    pierwsza = True
    while i <= n:
        for p in w:
            if i%p == 0:
                pierwsza = False
                break
        if pierwsza:
            w.append(i)
        i+=1
        pierwsza = True
    return w

def pierwsze_skladana(n):
    return [p for p in range(2,n+1) if (all([p%i for i in range(2, n//2)]) or p<4)]

def pierwsze_funkcyjna(n):
    return list(filter(lambda x: (all([x%i for i in range(2, n//2)]) or x<4), range(2,n+1)))

print("| %7s | %10s | %10s | %10s |" % ("n","imperatywna","skladana","funkcyjna"))
for i in range(1000,5000,500):
    print("| {:7d} ".format(i),end="")
    print("| {:10.5f}  ".format(timeit.timeit("pierwsze_imperatywna({})".format(i), setup="from __main__ import pierwsze_imperatywna", number=1)),end="")
    print("| {:10.5f} ".format(timeit.timeit("pierwsze_skladana({})".format(i), setup="from __main__ import pierwsze_skladana", number=1)),end="")
    print("| {:10.5f} |".format(timeit.timeit("pierwsze_funkcyjna({})".format(i), setup="from __main__ import pierwsze_funkcyjna", number=1)),end="")
    print()