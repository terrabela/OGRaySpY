# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""

import numpy as np
import matplotlib.pyplot as pl 
from scipy import optimize

def eq1(b):
    return 391 - 40*b + b**2
    
def eq2(b):
    return (500-b) * (b-350) + 150*(500-b)

def eqsys(b):
    return [ (24-b[0]-b[1])*(b[0]-13) + 39 - 3*b[0],
             (24-b[0]-b[1])*(b[1]-13) + 72 - 3*(b[0]+b[1]) ]

sol = optimize.root( eqsys, [5, 2] )
print( sol )
