""" 
to add more
consider using numpy
"""
from dataclasses import dataclass
from math import *
@dataclass
class Vector:
    x: int = 0
    y: int = 0

V = Vector

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