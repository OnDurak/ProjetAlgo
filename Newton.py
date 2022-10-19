#----------------------------------------------------------------------------
# Created By  : 
# Created Date: 
# version ='1.0'
# ---------------------------------------------------------------------------
# This module contains the implementation of the newton raphson algorithm"
# ---------------------------------------------------------------------------
import random as rand
from numpy import *
from polynomials import *
from trigono import *
# ---------------------------------------------------------------------------

def NewtonRaphsonNotSystem(f):
    a = 2.5
    for i in range(20):
        a = a - f.evaluate(a)/f.derivate().evaluate(a)
        print(a)


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