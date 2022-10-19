import random as rand
from numpy import *
#Idée : Une équation est Somme: (b * fonctionTrigo(k * x))
# Représenter une équation, c'est représenter un tableau de terme
# la fonction sinus est representé par la valeur 0 et la fonction sinus par la valeur 1
# Représenter un terme est un tableau avec la constante b en premier élément et la fonction trigonometrique  en second élément et la constante k en troisieme du terme
# Exemple : [[3, 0, 1], [2, 1, 5], 5 ] => 3 sin(X) + 2 cos (5x) = 5

# Supposer que les équations sont passées sous la forme décrite au dessus (ou faire une fonction transformant vers ce format (parse_equations))



class TrigoEquation:

    def __init__(self, equation, result):
            self.result = result
            self.equation = array(equation)
    
    def __init__(self, length):
        equation = array([[rand.randint(-10, 10), int(rand.random()), rand.randint(1, 10)]])
        nbrTerm = length

        while nbrTerm > 1:
            newTerm = array([rand.randint(-10, 10), rand.randint(0, 1), rand.randint(1, 10)])
            equation = append(equation, [newTerm], axis=0)
            nbrTerm -= 1

        self.equation = equation
        self.result = 0

    def get_equation(self):
        return self.equation

    def get_result(self):
        return self.result

    def set_equation(self, equation):
        self.equation = equation

    def set_result(self, result):
        self.result = result

    # derive une equation trigonometrique
    def derivate(self):
        derivate = TrigoEquation(self.equation.copy(), self.result)
        for eq in derivate.equation:
            if eq[1] == 0:
                eq[0] *= eq[2]
                eq[1] = 1
            else:
                eq[0] = -eq[0] * eq[2]
                eq[1] = 0
        
        return derivate

    def evaluate(self, x):
        value = 0
        for eq in self.equation:
            if eq[1] == 0:
                value += eq[0] * sin(eq[2] * x)
            else:
                value += eq[0] * cos(eq[2] * x)

        return value

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