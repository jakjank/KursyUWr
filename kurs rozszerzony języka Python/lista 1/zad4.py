from math import pi, sqrt
from random import random

def symulacja(ile_rzutow, dokladnosc):
    ltwo = 0
    cltwt = 0
    for i in range(ile_rzutow):
        if sqrt((random()-0.5)**2 + (random()-0.5)**2) < 0.5:
            ltwo += 1
        cltwt += 1
        my_pi = 4 * ltwo / cltwt
        print(i, ": ", my_pi)
        if abs(my_pi-pi) < dokladnosc:
            break
        


symulacja(10000, 0.00001)
