import numpy as np
from matplotlib import pyplot as plt

def calc_polynomial(x,nodes):
    w = 1
    for node in nodes:
        w = w*(x-node)
    return w

def equidistant_nodes(n):
    return np.linspace(-1,1,n+1)

def chebyshev_nodes(n):
    res = []
    for k in range(n+1):
        res.append(np.cos((2*k+1)/(2*n+2) * np.pi))
    return np.array(res)


n = 15
xs = np.linspace(-1, 1, 1000)

y_chebyshev   = [calc_polynomial(x,chebyshev_nodes(n)) for x in xs]
y_equidistant = [calc_polynomial(x,equidistant_nodes(n)) for x in xs]

plt.plot(xs, y_chebyshev, label="chebyshev")
plt.plot(xs, y_equidistant, label="equidistant")
plt.title(f"chebyshev nodes vs equidistant nodes for {n} nodes")
plt.legend()
plt.show()