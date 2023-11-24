
class Formula:
    def __add__(w1,w2):
        return Or(w1,w2)
    
    def __mul__(w1,w2):
        return And(w1,w2)

    def tautologia(self):
        if isinstance(self,And):
            return self.w1.tautologia() and self.w2.tautologia()
        if isinstance(self,Or):
            return self.w1.tautologia() or self.w2.tautologia()
        if isinstance(self,Stala):
            return self.wart
        if isinstance(self,Zmienna):
            return False
        if isinstance(self,Not):
            return not self.w1.tautologia()

    def uprosc(self):
        if isinstance(self,And):
            if isinstance(self.w1,Stala):
                if self.w1.wart == True:
                    return self.w2.uprosc() # true i p = p
                else:
                    return Stala(False)     # false i p = false
            if isinstance(self.w2,Stala):
                if self.w2.wart == True:
                    return self.w1.uprosc() # p i true = p
                else:
                    return Stala(False)     # p i false = false
            return And(self.w1.uprosc(),self.w2.uprosc())

        if isinstance(self,Or):
            if isinstance(self.w1,Stala):
                if self.w1.wart == True:
                    return Stala(True)      # true or p = true
                else:
                    return self.w2.uprosc() # false or p = p
            if isinstance(self.w2,Stala):
                if self.w2.wart == True:
                    return Stala(True)      # p or true = true
                else:
                    return self.w1.uprosc() # p or false = p
            return Or(self.w1.uprosc(),self.w2.uprosc())

        if isinstance(self,Not):
            if isinstance(self.w1,Stala):
                return Stala(not self.w1.wart) # ~(true) = false, ~(false) = true
            return Not(self.w1.uprosc())

        if isinstance(self,Zmienna):
            return self

        if isinstance(self,Stala):
            return self

    def uprosc_max(self):
        stare = self
        nowe = self.uprosc()
        while nowe.__str__() != stare.__str__():
            stare = nowe
            nowe = nowe.uprosc()
        return nowe

class Or(Formula):
    def __init__(self,w1,w2):
        self.w1, self.w2 = w1,w2

    def oblicz(self, zmienne):
        return self.w1.oblicz(zmienne) or self.w2.oblicz(zmienne)

    def __str__(self):
        if isinstance(self.w1,And) or isinstance(self.w1,Or):
            s1 = "(" + self.w1.__str__() + ")"
        else:
            s1 = self.w1.__str__()

        if isinstance(self.w2,And) or isinstance(self.w2,Or):
            s2 = "(" + self.w2.__str__() + ")"
        else:
            s2 = self.w2.__str__()

        return s1 + " or " + s2 

class And(Formula):
    def __init__(self,w1,w2):
        self.w1, self.w2 = w1,w2

    def oblicz(self, zmienne):
        return self.w1.oblicz(zmienne) and self.w2.oblicz(zmienne)

    def __str__(self):
        if isinstance(self.w1,And) or isinstance(self.w1,Or):
            s1 = "(" + self.w1.__str__() + ")"
        else:
            s1 = self.w1.__str__()

        if isinstance(self.w2,And) or isinstance(self.w2,Or):
            s2 = "(" + self.w2.__str__() + ")"
        else:
            s2 = self.w2.__str__()

        return s1 + " and " + s2 

class Not(Formula):
    def __init__(self,w1):
        self.w1 = w1
    
    def oblicz(self,zmienne):
        return not self.w1.oblicz(zmienne)

    def __str__(self):
        return "~(" + self.w1.__str__()  + ")"

class Zmienna(Formula):
    def __init__(self,nazwa):
        self.nazwa = nazwa
    
    def oblicz(self, zmienne):
        if self.nazwa not in zmienne:
            raise(WartosciowanieError("brak wartosciowania dla '{}'".format(self.nazwa)))
        return zmienne[self.nazwa]
        

    def __str__(self):
        return self.nazwa

class Stala(Formula):
    def __init__(self,wart):
        if wart != True and wart != False:
            raise WartoscStalejError("wartosc stalej to bool, nie {}".format(wart))
        else:
            self.wart = wart

    def oblicz(self,zmienne):
        return self.wart

    def __str__(self):
        return str(self.wart)

class WartosciowanieError(Exception):
    pass

class WartoscStalejError(Exception):
    pass

print("WYPISYWANIE")
w = And(Or(Stala(True),Zmienna('x')), Not(Stala(True)))
print("w =",w)
print()

print("MUL i ADD")
print("w + zmienna(y):", w + Zmienna('y'))
print("w * Not(Stala(True)):", w * Not(Stala(True)))
print()

print("OBLICZANIE WARTOSCI")
print("Wartosc '{}' dla wartosciowania x=false :".format(w),w.oblicz({'x':False}))
w2 = w + Zmienna('y')
print("Wartosc '{}' dla wartosciowania x=false, y=true :".format(w2), w2.oblicz({'x':False,'y':True}))
print()

print("TAUTOLOGIE")
print("Czy w to tautologia?",w.tautologia())
w3 = Or(Not(Zmienna('x')),Zmienna('x'))
print("Czy '{}' to tautologia?".format(w3),w3.tautologia())
print()

print("UPRASZCZANIE")
print("Uproszczone '{}':".format(w2),w2.uprosc())
print("Podwojnie uproszczone '{}':".format(w2), w2.uprosc().uprosc())
print("Maksymalnie uproszczone '{}':".format(w2), w2.uprosc_max())
w4 = Or(Or(And(Zmienna('x'),Stala(False)),Not(Zmienna('y'))),Not(And(Zmienna('z'),Stala(False))))
print("Maksymalnie uproszczone '{}':".format(w4),w4.uprosc_max())
print()

print("WYJATKI")
try:
    And(Zmienna('x'),Stala(False)).oblicz({})
except WartosciowanieError as e:
    print(e)

try:
    Stala(3)
except WartoscStalejError as e:
    print(e)