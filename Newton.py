#----------------------------------------------------------------------------
# Created By  : 
# Created Date: 
# version ='1.0'
# coding=utf-8
# ---------------------------------------------------------------------------
# This module contains the implementation of the newton raphson algorithm"
# ---------------------------------------------------------------------------
import random as rand

import math
import numpy
from polynomials import *
from trigono import *
from multivariate_systems import *
# ---------------------------------------------------------------------------

# Function that given function f and point a will try to find a value b such that f(a) * f(b) < 0
def bisect_starting_point(f, a):
    a_sign = numpy.sign(a)

    # If after 20 iterations we couldn't find a value for b of opposite sign we stop
    for i in range(20):
        # generate random value for b
        b = rand.random() * math.pow(10, i % 5)

        # using -b and b to test with f
        if numpy.sign(f.evaluate(-b)) != a_sign:
            return -b
        elif numpy.sign(f.evaluate(b)) != a_sign:
            return b

    return None


def newton_step(f, deriv, a):
    return a - f.evaluate(a) / deriv.evaluate(a)


def bisection_step(a, b):
    return (a+b)/2


# Function used only if f(a) * f(b) < 0 and a < b, this precondition must be respected
def newton_bisect_notsys(f, a, b):
    # We chose the value closer to 0 for the first iteration of Newton
    if abs(f.evaluate(a)) < abs(f.evaluate(b)):
        x = a
    else:
        x = b

    deriv = f.derivate()

    for i in range(40):
        x = newton_step(f, deriv, x)

        # If x is outside of a,b using newton, this mean newton diverges, thus we switch to bisection
        if x < a or x > b:
            x = bisection_step(a, b)

        # Updating [a,b] for the potential next bisection step
        if f.evaluate(a) * f.evaluate(x) > 0:
            a = x
        else:
            b = x

    return x


# Function implementing naive Newton method, convergence not assured
def naive_newton_notsys(f, a):
    deriv = f.derivate()

    for i in range(20):
        a = newton_step(f, deriv, a)

    return a


# Function deciding whether to use naive Newton or Bisect-Newton given two points [a,b] and a function f
# If a,b cannot be used for Bisect-Newton, it will try to find suitable value, if that doesn't work => naive Newton
def newton_notsys(f, a, b):

    if f.evaluate(a) * f.evaluate(b) > 0:
        print("given a,b not valid, attempting to find correct values...")
        b = bisect_starting_point(f, a)

        if b is None:
            print("couldn't find suitable values to use for bisection, naive Newton method to be used...")
            return naive_newton_notsys(f, a)

        print("suitable values could be found, Newton-Bisection method to be used...")

    if a < b:
        return newton_bisect_notsys(f, a, b)
    else:
        return newton_bisect_notsys(f, b, a)


# Apply newton method to multivariate system of equations given the system s and the starting points stored in vector
def newton_sys(s, vector):
    if len(vector) != s.N:
        raise Exception("vector size doesn't match number of unknowns to be used in Newton method")

    for i in range(100):
        J = s.jacobian_matrix_at(vector)
        F = np.multiply(s.evaluate(vector), -1)
        #maybe check if matrix are singular
        X = np.linalg.solve(J, F)

        vector = np.add(X, vector)

    return vector




def MenuPolynomial():
    ans = True
    while ans:
        print(""" 
        1.Random equation
        2.Input equation
        """)
        ans = input("What would you like to do? ")
        if ans == "1":
            length = input("How many terms would you like in the equation? ")
            randomEquation = PolynomialEquations(int(length))
            print(randomEquation)
            return

        elif ans == "2":
            print("random")
            return
            
        else:
            print("\n Not Valid Choice Try again\n\n")


def MenuTrigono():
    ans = True
    while ans:
        print(""" 
        1.Random equation
        2.Input equation
        """)
        ans = input("What would you like to do? ")
        if ans == "1":
            length = input("How many terms would you like in the equation? ")
            randomEquation = TrigoEquation(int(length))
            print(randomEquation)
            return

        elif ans == "2":
            print("random")
            return
            
        else:
            print("\n Not Valid Choice Try again\n\n")


if __name__ == '__main__':
    N = 3
    # x+y-z = 0 || 1+2-3 = 0
    # xyz+3xy+5yz = 0 || 1*2*3 + 3*2 + 5 * 2 * 3 = 42
    # x^2 + y^2 + z^2 = 0 || 1 + 4 + 9 = 14
    '''
    J = [ [[1], [1], [-1]],
          [[yz + 3y], [xz + 3x + 5z], [xy+5y]],
          [[2x], [2y], [2z]]
        ]   
    '''
    m1 = MultivariateEquations([[1, [1, 0, 0]], [1, [0, 1, 0]], [-1, [0, 0, 1]]], 1, N)
    m2 = MultivariateEquations([[2, [1, 0, 0]], [1, [0, 0, 1]]], 5, N)
    m3 = MultivariateEquations([[1, [0, 2, 0]], [1, [0, 0, 2]]], 13, N)

    s = MultivariateSystem(m1, m2, m3)
    
    J = s.jacobian_matrix_at([1, 2, 3])
    for line in J:
        for eq in line:
            print(eq)
        print("end of line\n")

    F = np.multiply(s.evaluate([1, 2, 3]), -1)

    print(F)

    X = np.linalg.solve(J, F)
    print(X)

    print(np.add(X, [1, 2, 3]))

    r = newton_sys(s, [2, -2, 0])
    print(r)

    s = MultivariateSystem(m1, m2, m3)
    print(s.evaluate(r))
    '''



    
    p = TrigoEquation([[1, 1, 1], [-1,0,1]], 1)

    r = newton_notsys(p, -10, 5)

    print(r)
    print(p.evaluate(r))
    '''


    '''
    ans=True
    while ans:
        print ("""
        1.Approximate solution for polynomial equations
        2.Approximate solution for trigonometric equations
        4.Exit/Quit
        """)
        ans=input("What would you like to do? ") 
        if ans=="1": 
            MenuPolynomial()
        elif ans=="2":
            MenuTrigono()
    
        elif ans=="4":
            ans = False
    
        elif ans !="":
            print("\n Not Valid Choice Try again\n\n")
    '''