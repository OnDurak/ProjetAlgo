#----------------------------------------------------------------------------
# Created By  : 
# Created Date: 
# version ='1.0'
# ---------------------------------------------------------------------------
# This module contains the implementation of the newton raphson algorithm"
# ---------------------------------------------------------------------------
from numpy import *
from polynomials import *
# ---------------------------------------------------------------------------

def NewtonRaphson(f):
    a = 2.5
    for i in range(20):
        a = a - f.evaluate(a)/f.derivate().evaluate(a)
        print(a)
    