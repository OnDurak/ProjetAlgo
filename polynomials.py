#Idée : Une équation est Somme: (b * Produit pow(x_i, k))
# Représenter une équation, c'est représenter un tableau de terme
# Représenter un terme est un tableau avec la constante b en premier élément et la puissance k en second élément du terme
# Exemple: [[2, 3], [-3, 5], [1, 2]] => 2(x^3) - 3(x^5) + x^2

# Supposer que les équations sont passées sous la forme décrite au dessus (ou faire une fonction transformant vers ce format (parse_equations))
class PolynomialEquations:


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

    #Compute the derivatie of the polynomial equation 
    def derivate(self):
        for eq in self.equation:
            if eq[1] == 0:
                self.equation.remove(eq)
            else:
                eq[0]*=eq[1]
                eq[1]-=1

    #toString function
    def __str__(self):
        s = ""
        for i in range(len(self.equation)):
            if i == len(self.equation) - 1:
                s += f'{self.equation[i][0]}x^{self.equation[i][1]}\n'
            else:
                s += f'{self.equation[i][0]}x^{self.equation[i][1]} + '
        return s
        
            
            
            


equation = PolynomialEquations([[6, 3], [-3, 2], [1, 2], [5, 0], [7, 20]], 0)
print(equation.__str__())
equation.derivate()
print(equation.equation)
#print(equation.__str__())

