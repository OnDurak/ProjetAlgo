# Idea : an equation is a Sum: (b * pow(x_i, k))
# Representing an equation is representing an array of terms
# Representing a term is representing an array with the coefficient b as the first element and the x exponent value
# as the second element
# Example : [[2, 3], [-3, 5], [1, 2]] => 2(x^3) - 3(x^5) + x^2

# We suppose that the equation given to this class are represented using this encoding
from copy import deepcopy
import random as rand


class PolynomialEquations:
    B_INDEX = 0
    POW_INDEX = 1

    def __init__(self, equation, result):
        self.equation = equation
        self.result = result

    def get_equation(self):
        return self.equation

    def set_equation(self, equation):
        self.equation = equation

    # Function returning the derivative of the calling equation
    def derivate(self):
        derivative = PolynomialEquations(deepcopy(self.equation), 0)

        for eq in derivative.equation:
            if eq[self.POW_INDEX] == 0:
                eq[self.B_INDEX] = 0
            else:
                eq[self.B_INDEX] *= eq[self.POW_INDEX]
                eq[self.POW_INDEX] -= 1

        return derivative

    # Function evaluating an equation at point x
    def evaluate(self, x):
        value = 0
        for term in self.equation:
            value += term[self.B_INDEX] * pow(x, term[self.POW_INDEX])
        
        return value - self.result

    # Class method that returns a random equation given the number of terms
    @classmethod
    def random_equation(cls, n):
        eq = []
        for i in range(n):
            eq.append([rand.randint(-10, 10), rand.randint(0, 10)])

        return PolynomialEquations(eq, rand.randint(-10, 10))

    # Function printing the equation in a pretty way
    def __str__(self):
        s = ""
        SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        for i in range(len(self.equation)):
            x = f'x{self.equation[i][1]}'.translate(SUP)
            if i == len(self.equation) - 1:
                s += f'{self.equation[i][0]}{x} = {self.result}\n'
            else:
                s += f'{self.equation[i][0]}{x} + '
        return s
