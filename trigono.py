# Idea : an equation is a Sum: (b * trig_function(k * x))
# Representing an equation is representing an array of terms
# The sin function is represented by 0 and the cos function is represented by 1
# Thus a term is an array with the coefficient b as the first element, the function value as the second element
# and the coefficient k as the last element
# Example : [[3, 0, 1], [2, 1, 5], 5 ] => 3 sin(X) + 2 cos (5x) = 5

# We suppose that the equation given to this class are represented using this encoding
from numpy import *
from copy import deepcopy
import random as rand


class TrigoEquation:
    SIN = 0
    COS = 1

    B_INDEX = 0
    FUN_INDEX = 1
    K_INDEX = 2

    def __init__(self, equation, result):
        self.equation = equation
        self.result = result

    def get_equation(self):
        return self.equation

    def get_result(self):
        return self.result

    def set_equation(self, equation):
        self.equation = equation

    def set_result(self, result):
        self.result = result

    # Function returning the derivative of the calling equation
    def derivate(self):
        derivative = TrigoEquation(deepcopy(self.equation), 0)

        for eq in derivative.equation:
            if eq[self.FUN_INDEX] == self.SIN:
                eq[self.B_INDEX] *= eq[self.K_INDEX]
                eq[self.FUN_INDEX] = self.COS
            else:
                eq[self.B_INDEX] = -eq[self.B_INDEX] * eq[self.K_INDEX]
                eq[self.FUN_INDEX] = self.SIN
        
        return derivative

    # Function evaluating an equation at point x
    def evaluate(self, x):
        value = 0
        for eq in self.equation:
            if eq[self.FUN_INDEX] == self.SIN:
                value += eq[self.B_INDEX] * sin(eq[self.K_INDEX] * x)
            else:
                value += eq[self.B_INDEX] * cos(eq[self.K_INDEX] * x)

        return value

    # Class method that returns a random equation given the number of terms
    @classmethod
    def random_equation(cls, n):
        eq = []
        for i in range(n):
            eq.append([rand.randint(-10, 10), rand.randint(0, 1), rand.randint(0, 10)])

        return TrigoEquation(eq, rand.randint(-n, n))

    # Class method that reads equation from file and return the equation
    @classmethod
    def read_equation_trigo(cls, file_equation):

        res = file_equation.split('; ')
        result = res.pop()
        result = int(result)
        for i in range(len(res)):
            res[i] = res[i].strip('][').split(',')
            res[i][0] = int(res[i][0])
            res[i][1] = int(res[i][1])
            res[i][2] = int(res[i][2])

        trigoEQ = res
        return TrigoEquation(trigoEQ, result)

    # Function printing the equation in a pretty way
    def __str__(self):
        s = ""
        for i in range(len(self.equation)):
            if i == len(self.equation)-1:
                if self.equation[i][1] == 0:
                    s += f' {self.equation[i][0]}sin({self.equation[i][2]}x) = {self.result}'
                else:
                    s += f' {self.equation[i][0]}cos({self.equation[i][2]}x) = {self.result}'
            else:
                if self.equation[i][1] == 0:
                    s += f' {self.equation[i][0]}sin({self.equation[i][2]}x) +'
                else:
                    s += f' {self.equation[i][0]}cos({self.equation[i][2]}x) +'
            
        return s
