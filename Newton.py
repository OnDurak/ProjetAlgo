#----------------------------------------------------------------------------
# Created By  : 
# Created Date: 
# version ='1.0'
# coding=utf-8
# ---------------------------------------------------------------------------
# This module contains the implementation of the Newton-Raphson algorithm"
# ---------------------------------------------------------------------------
import random as rand

import math
import numpy as np
import random
from polynomials import *
from trigono import *
from multivariate_systems import *
import sys
#import matplotlib.pyplot as plt

# Epsilon to check if value found by Naive Newton is correct
EPS = 0.1
# Max iteration allowed for Naive Newton
MAX_ITER = 40

# ---------------------------------------------------------------------------
# Start of functions related to newton-method for simple equation


# Function that output on the screen the evolution of the convergence to a solution given the steps
def compute_convergence(steps):
    s = ""
    i = 1
    pre_list = []
    for step in steps:
        if step[1] == "N":
            m = "Newton"
        else:
            m = "Bisection"

        try:
            pre_won = round(math.log10(abs(step[0]/step[2])), 1)
            pre_list.append(pre_won)
        except:
            pre_won = 0

        if pre_won < 0:
            l = "lost"
        else:
            l = "won"
        s += f'{i}-th step, precision {l} : 10^{-pre_won} using {m}. '
        i += 1

    print(s)

    # allow to show a plot of the convergence (uncomment matplotlib as well to use)
    #plt.plot(range(1, len(pre_list)+1), pre_list)
    #plt.show()


# Function that given function f and point a will try to find a value b such that f(a) * f(b) < 0
def bisect_starting_point(f, a):
    a_sign = np.sign(f.evaluate(a))

    # If after 20 iterations we couldn't find a value for b of opposite sign we stop
    for i in range(20):
        # generate random value for b
        b = rand.random() * math.pow(10, i % 5)

        # using -b and b to test with f
        if np.sign(f.evaluate(-b)) != a_sign:
            return -b
        elif np.sign(f.evaluate(b)) != a_sign:
            return b

    return None


# Function computing a step of the Newton method
def newton_step(f, deriv, a):
    x = deriv.evaluate(a)
    if x == 0:
        return None
    return a - f.evaluate(a) / x


# Function computing a step of the bisection method
def bisection_step(a, b):
    return float(a+b)/2.0


# Function used only if f(a) * f(b) < 0 and a < b, this precondition must be respected
def newton_bisect_notsys(f, a, b):
    # We chose bisection as the first value of x
    x = bisection_step(a, b)

    deriv = f.derivate()

    steps = []
    while abs(f.evaluate(x)) > pow(10, -14):
        step = [f.evaluate(x)]
        x = newton_step(f, deriv, x)
        step.append("N")

        if x is None or x <= a or x >= b:
            x = bisection_step(a, b)
            step[1] = "B"

        step.append(f.evaluate(x))

        # Updating [a,b] for the potential next bisection step
        if f.evaluate(a) * f.evaluate(x) > 0:
            a = x
        else:
            b = x

        steps.append(step)

    return x, steps


# Function implementing naive Newton method, convergence not assured
def naive_newton_notsys(f, a):
    deriv = f.derivate()

    steps = []
    # No guarantee of convergence so we're forced to iterate for a given number of steps, else we risk infinite loop
    for i in range(MAX_ITER):
        step = [f.evaluate(a)]
        a = newton_step(f, deriv, a)
        step.append("N")
        step.append(f.evaluate(a))
        if a is None:
            return None, None
        steps.append(step)

    if abs(f.evaluate(a)) < EPS:
        return None, None
        
    return a, steps


# Function deciding whether to use naive Newton or Bisect-Newton given two points [a,b] and a function f
# If a,b cannot be used for Bisect-Newton, it will try to find suitable value, if that doesn't work => naive Newton
def newton_notsys(f, a, b):

    if f.evaluate(a) * f.evaluate(b) > 0:
        print("given a,b not valid, attempting to find correct values...")
        b = bisect_starting_point(f, a)

        if b is None:
            print("couldn't find suitable values to use for bisection, naive Newton method to be used with random starting point...")
            return naive_newton_notsys(f, random.randint(-100, 100))

        print("suitable values could be found, Newton-Bisection method to be used...")

    if a < b:
        return newton_bisect_notsys(f, a, b)
    else:
        return newton_bisect_notsys(f, b, a)

# End of functions related to newton-method for simple equation
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Start of functions related to newton-method for multivariate systems


# Apply newton method to multivariate system of equations given the system s and the starting points stored in vector
def newton_sys(s, vector):
    if len(vector) != s.N:
        raise Exception("vector size doesn't match number of unknowns to be used in Newton method")

    for i in range(MAX_ITER):
        J = s.jacobian_matrix_at(vector)
        F = s.evaluate(vector)

        # If the jacobian matrix is singular, newton method cannot work, thus we stop execution
        if linalg.cond(J) >= 1 / sys.float_info.epsilon:
            print("Singular Jacobian matrix encountered, cannot find roots for given vector")
            return None

        X = np.linalg.solve(J, F)

        vector = np.subtract(vector, X)

    if not all(abs(i) < EPS for i in s.evaluate(vector)):
        print("Newton method couldn't converge for the given vector, systems might not have solution in real set")
        return None

    return vector

# End of functions related to newton-method for multivariate systems
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Start of functions related to handling input and user interface


def menu_polynomial():
    ans = True

    while ans:
        print(""" 
        1.Random equation
        2.Load file
        """)

        ans = input("What would you like to do? ")

        if ans == "1":
            length = input("How many terms would you like in the equation? ")
            random_equation = PolynomialEquations.random_equation(int(length))
            print("generated equation :")
            print(random_equation)
            
            a = int(input("Enter first starting point for Newton-Bisect method (a)"))
            b = int(input("Enter second starting point for Newton-Bisect method (b)"))
            
            print("Solving...")
            r, steps = newton_notsys(random_equation, a, b)
            if r is None:
                print("Couldn't find roots for given equation...")
            else:
                print("Found solution for :" + str(random_equation))
                print("x = " + str(r))
                print("Value of equation for found x : " + str(random_equation.evaluate(r)))
                print("Convergence checking :")
                compute_convergence(steps)
            return

        elif ans == "2":
            nameFile = input("please enter the file name")
            file = open(nameFile, 'r')
            a = int(input("Enter first starting point for Newton-Bisect method (a) "))
            b = int(input("Enter second starting point for Newton-Bisect method (b) "))
            for line in file:

                polyEQ = PolynomialEquations.read_equation_poly(line)
                print(polyEQ)
                print("Solving...")
                r, steps = newton_notsys(polyEQ, a, b)
                if r is None:
                    print("Couldn't find roots for given equation...")
                else:
                    print("Found solution for :" + str(polyEQ))
                    print("x = " + str(r))
                    print("Value of equation for found x : " + str(polyEQ.evaluate(r)))
                    print("Convergence checking :")
                    compute_convergence(steps)
            file.close()
            return
            
        else:
            print("\n Not Valid Choice Try again\n\n")


def menu_trigono():
    ans = True

    while ans:
        print(""" 
        1.Random equation
        2.Load file
        """)

        ans = input("What would you like to do? ")

        if ans == "1":
            length = input("How many terms would you like in the equation? ")
            random_equation = TrigoEquation.random_equation(int(length))
            print("generated equation :")
            print(random_equation)

            a = int(input("Enter first starting point for Newton-Bisect method (a)"))
            b = int(input("Enter second starting point for Newton-Bisect method (b)"))

            print("Solving...")
            r, steps = newton_notsys(random_equation, a, b)
            if r is None:
                print("Couldn't find roots for given equation...")
            else:
                print("Found solution for :" + str(random_equation))
                print("x = " + str(r))
                print("Value of equation for found x : " + str(random_equation.evaluate(r)))
                print("Convergence checking :")
                compute_convergence(steps)
            return

        elif ans == "2":
            nameFile = input("please enter the file name")
            file = open(nameFile, 'r')
            a = int(input("Enter first starting point for Newton-Bisect method (a)"))
            b = int(input("Enter second starting point for Newton-Bisect method (b)"))
            for line in file:

                trigoEQ = TrigoEquation.read_equation_trigo(line)
                print(trigoEQ)
                print("Solving...")
                r, steps = newton_notsys(trigoEQ, a, b)
                if r is None:
                    print("Couldn't find roots for given equation...")
                else:
                    print("Found solution for :" + str(trigoEQ))
                    print("x = " + str(r))
                    print("Value of equation for found x : " + str(trigoEQ.evaluate(r)))
                    print("Convergence checking :")
                    compute_convergence(steps)
            file.close()
            return
            
        else:
            print("\n Not Valid Choice Try again\n\n")


def menu_system():
    ans = True

    while ans:
        print(""" 
            1.Random system
            2.Load file
            """)

        ans = input("What would you like to do? ")

        if ans == "1":
            length = int(input("How many unknowns/equations would you like in the system? "))
            random_system = MultivariateSystem.random_system(length)
            print("generated system :")
            print(random_system)

            vector = []
            for i in range(length):
                vector.append(int(input(f'Enter the {i}-th value for the starting vector')))

            print("Given vector = " + str(vector))
            print("Solving...")
            r = newton_sys(random_system, vector)
            if r is None:
                print("Couldn't find roots for given system...")
            else:
                print("Found solution for system")
                print("x = " + str(r))
                print("Value of system for found solution : " + str(random_system.evaluate(r)))
            return

        elif ans == "2":
            nameFile = input("please enter the file name")
            file = open(nameFile, 'r')
            vector = []
            for line in file:
                nbEq = int(line)
                for i in range(nbEq):
                    vector.append(int(input(f'Enter the {i}-th value for the starting vector')))
                print(vector)
                multiSys = MultivariateSystem.read_system(nbEq, file)
                print(multiSys)
                print("Solving...")
                r = newton_sys(multiSys, vector)
                vector.clear()
                if r is None:
                    print("Couldn't find roots for given equation...")
                else:
                    print("Found solution for system")
                    print("x = " + str(r))
                    print("Value of equation for found x : " + str(multiSys.evaluate(r)))
            file.close()
            
            return

        else:
            print("\n Not Valid Choice Try again\n\n")

# End of functions related to handling input and user interface
# ---------------------------------------------------------------------------


if __name__ == '__main__':
    ans = True

    while ans:
        print("""
        1.Approximate solution for polynomial equations
        2.Approximate solution for trigonometric equations
        3.Approximate solution for system of equations
        4.Exit/Quit
        """)

        ans = input("What would you like to do? ")

        if ans == "1":
            menu_polynomial()
        elif ans == "2":
            menu_trigono()
        elif ans == "3":
            menu_system()
        elif ans == "4":
            ans = False
        elif ans != "":
            print("\n Not Valid Choice Try again\n\n")