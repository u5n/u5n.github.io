from numbers import Number
from math import hypot, nan, inf
# shorthand of vector
class V:
    __slots__ ='x','y'
    def __init__(self, *args):
        if len(args)==2: 
            self.x = args[0]
            self.y = args[1]
        elif len(args)==1:
            self.x = args[0].x
            self.y = args[0].y
        elif len(args)==0:
            self.x = 0
            self.y = 0
    def __repr__(self):
        return f"({self.x},{self.y})"
    def __mul__(self, oth):
        if isinstance(oth, V) or isinstance(oth, tuple):
            return V(self.x*oth[0],self.y*oth[1])
        elif isinstance(oth, Number):
            return V(self.x*oth,self.y*oth)
    def __div__(self, oth):
        if isinstance(oth, V) or isinstance(oth, tuple):
            return V(self.x/oth[0],self.y/oth[1])
        elif isinstance(oth, Number):
            return V(self.x/oth,self.y/oth)
    def __floordiv__(self, oth):
        if isinstance(oth, V) or isinstance(oth, tuple):
            return V(self.x//oth[0],self.y//oth[1])
        elif isinstance(oth, int):
            return V(self.x//oth,self.y//oth)
    def __add__(self, oth):
        if isinstance(oth, V) or isinstance(oth, tuple):
            return V(self.x+oth[0],self.y+oth[1])
        elif isinstance(oth, Number):
            return V(self.x+oth,self.y+oth)
    def __sub__(self, oth):
        if isinstance(oth, V) or isinstance(oth, tuple):
            return V(self.x-oth[0],self.y-oth[1])
        elif isinstance(oth, Number):
            return V(self.x-oth,self.y-oth)
    def __getitem__(self, i):
        if i==0: return self.x
        elif i==1: return self.y
    def __setitem__(self, i ,v):
        if i==0: self.x = v
        elif i==1: self.y = v
    def __iter__(self):
        yield self.x ; yield self.y
    def __lt__(self, oth):
        if self.x != oth.x: return self.x < oth.x
        else: return self.y < oth.y
    def __eq__(self, oth): return not self < oth and not oth < self
    def __le__(self, oth): return not oth < self
    def __gt__(self, oth): return not self <= oth
    def __ge__(self, oth): return not self < oth
    def __hash__(self): return hash((self.x, self.y))
    def mag(self): return hypot(self.x, self.y)
    
    # length as `[,)` interval
    def len(self): return self.y - self.x
    def getAsIndex(self, mat): return mat[self.x][self.y]
    def setAsIndex(self, mat, v): mat[self.x][self.y] = v
    
    def tolist(self): return [self.x, self.y]
    def rotate(self, k=1): 
        # k==1 anti closewise 90 deg
        if k%4==0: return V(self.x, self.y)
        elif k%4==1: return V(self.y, -self.x)
        elif k%4==2: return V(-self.x, -self.y)
        elif k%4==3: return V(-self.y, self.x)
    def colinear(self, oth): return self.x*oth.y == oth.x*self.y
    def slope(self): 
        if self.x != 0:
            return self.y/self.x
        else:
            if self.y == 0 : return nan
            return inf if self.y > 0 else -inf