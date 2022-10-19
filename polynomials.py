from numpy import *
#Idée : Une équation est Somme: (b * Produit pow(x_i, k))
# Représenter une équation, c'est représenter un tableau de terme
# Représenter un terme est un tableau avec la constante b en premier élément et la puissance k en second élément du terme
# Exemple: [[2, 3], [-3, 5], [1, 2]] => 2(x^3) - 3(x^5) + x^2

# Supposer que les équations sont passées sous la forme décrite au dessus (ou faire une fonction transformant vers ce format (parse_equations))
class PolynomialEquations:


    def __init__(self, equation):
        self.equation = array(equation)

    def get_equation(self):
        return self.equation

    def set_equation(self, equation):
        self.equation = equation

    #Compute the derivatie of the polynomial equation 
    def derivate(self):
        derivate = PolynomialEquations(self.equation.copy())
        for eq in derivate.equation:
            if eq[1] == 0:
                eq[0] = 0
            else:
                eq[0]*=eq[1]
                eq[1]-=1
        
        return derivate

    def evaluate(self, x):
        value = 0
        for term in self.equation:
            value = term[0] * x ** term[1]
        
        return value
        

    #toString function
    def __str__(self):
        s = ""
        for i in range(len(self.equation)):
            if i == len(self.equation) - 1:
                s += f'{self.equation[i][0]}x^{self.equation[i][1]}\n'
            else:
                s += f'{self.equation[i][0]}x^{self.equation[i][1]} + '
        return s
        
            
            
            


equation = PolynomialEquations([[6, 1], [-3, 2], [1, 0], [5, 1]])
print(equation)
print(equation.derivate())
print(equation)

