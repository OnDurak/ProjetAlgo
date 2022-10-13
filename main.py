#Idée : Une équation est Somme: (b * Produit pow(x_i, k))
# Représenter une équation, c'est représenter un tableau de terme
# Représenter un terme est un tableau avec la constante b, est un tableau avec les différentes variables et leur puissance
# Exemple : [ [5, [3, 0, 1] ] ,... ] => 5*(x^3 * 1 * z) + ...

# Supposer que les équations sont passées sous la forme décrite au dessus (ou faire une fonction transformant vers ce format (parse_equations))
class MultivariateEquations:
    COEFF = 0
    UNKNOWNS = 1
    def __init__(self, eq, result, nbUnknowns):
        self.result = result
        self.nbUnknowns = nbUnknowns
        self.eq = eq

    # A implémenter si l'on veut transformer l'input sous la forme décrite au-dessus
    def parse_equations(self, eq):
        pass

    # Itérer pour le nombre de variables, itérer pour le nombre de terme, pour chaque terme dériver par rapport à la ième variable
    def partial_derivative(self):
        partialDerivatives = []

        for i in range(self.nbUnknowns):
            for term in self.eq:
                partialDerivatives.append(self.derivate(term, i))

        return partialDerivatives

    def derivate(self, term, unknownIndex):
        unknownCurrPower = term[self.UNKNOWNS][unknownIndex]
        term[self.UNKNOWNS][unknownIndex] -= 1
        term[self.COEFF] *= unknownCurrPower

        return term



if __name__ == '__main__':
    print('PyCharm')


