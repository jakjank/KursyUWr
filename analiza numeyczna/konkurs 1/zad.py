import numpy as np
import matplotlib.pyplot as plt
import os

def segment_k(x, xs ,ys, Ms):
    k = 1
    while x > xs[k]:
        k += 1
    
    hk = xs[k]-xs[k-1]

    res = (1/6)*Ms[k-1]*((xs[k]-x)**3)
    res = res + (1/6)*Ms[k]*((x-xs[k-1])**3)
    res = res + (ys[k-1] - (1/6)*Ms[k-1]*(hk**2))*(xs[k]-x)
    res = res + (ys[k] - (1/6)*Ms[k]*(hk**2))*(x-xs[k-1])
    res = (hk**(-1))*res
    return res

def il_rozn(xs, ys):
    n = len(xs)
    if n == 1:
        return ys[0]
    return (il_rozn(xs[1:], ys[1:]) - il_rozn(xs[:n-1],ys[:n-1]))/(xs[n-1] - xs[0])

def oblicz_Ms(xs,ys):
    def H(k):
        return xs[k] - xs[k-1]

    def lmbda(k):
        return H(k)/(H(k)+H(k+1))

    n = len(xs)
    p,q,u = [0],[0],[0]

    for k in range(1,n-1):
        p.append((lmbda(k)*q[k-1]) +2)
        q.append((lmbda(k)-1)/p[k])
        u.append((6*il_rozn([xs[k-1],xs[k],xs[k+1]],[ys[k-1],ys[k],ys[k+1]])-lmbda(k)*u[k-1])/p[k])
    
    Ms = [0]
    for k in range(n-2,0,-1):
        Ms.append(u[k] + q[k]*Ms[n-2-k])
    Ms.append(0)
    Ms.reverse()
    return Ms

class NIFS3:
    xs = []
    ys = []
    Ms = []
    def __init__(self,xs1,ys1):
        self.xs = xs1
        self.ys = ys1
        self.Ms = oblicz_Ms(xs1,ys1)
    
    def oblicz(self, x):
        return segment_k(x,self.xs,self.ys,self.Ms)

plt.rcParams["figure.figsize"] = [14,2]
with open("dane.txt") as d:
    for i in range(15):
        ts = eval(d.readline())
        f = NIFS3(ts, eval(d.readline()))
        g = NIFS3(ts, eval(d.readline()))
        us = eval(d.readline())
        plt.plot([f.oblicz(u) for u in us], [g.oblicz(u) for u in us], color=(0.7682,0.2588,0.4275))


plt.show()