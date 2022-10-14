# coding=utf-8
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

        if not all(len(T[self.UNKNOWNS]) is self.nbUnknowns for T in self.eq):
            raise Exception("Error: terms have different number of unknowns")

    # Itérer pour le nombre de variables, itérer pour le nombre de terme, pour chaque terme dériver par rapport à la ième variable
    # Calcule la matrice jaocbienne sans évaluer (symbolique)
    def partial_derivative(self):
        partialDerivatives = []

        for i in range(self.nbUnknowns):
            currTerm = []
            for term in self.eq:
                currTerm.append(self.derivate(term, i))
            partialDerivatives.append(currTerm)

        return partialDerivatives

    # Calcule la matrice jacobienne pour un vecteur donnée
    def partial_derivative_at(self, vector):
        jacobianVector = self.partial_derivative()
        evaluatedJacVector = []

        for eq in jacobianVector:
            evaluatedJacVector.append(self.evaluate(eq, vector))

        return evaluatedJacVector

    # Dérive un terme de l'équation par rapport à l'inconnu numéro unknownIndex
    def derivate(self, term, unknownIndex):
        newTerm = term.copy()
        newTerm[self.UNKNOWNS] = newTerm[self.UNKNOWNS].copy()

        unknownCurrPower = newTerm[self.UNKNOWNS][unknownIndex]

        if newTerm[self.UNKNOWNS][unknownIndex] > 0:
            newTerm[self.UNKNOWNS][unknownIndex] -= 1

        newTerm[self.COEFF] *= unknownCurrPower

        return newTerm

    # Evalue une équation en un vecteur (Somme: (b * Produit pow(x_i, k)))
    def evaluate(self, eq, vector):
        sum = 0
        for term in eq:
            sum += self.evaluate_term(term, vector)

        return sum

    # Evalue un terme de l'équation avec un vecteur donnée (b * Produit pow(x_i, k_i), où k est un élément de vector)
    def evaluate_term(self, term, vector):
        if self.nbUnknowns != len(vector):
            raise Exception("cannot evaluate a term : input vector length doesn't match unknowns number")

        unknownProduct = 1
        for i in range(self.nbUnknowns):
            unknownProduct *= pow(vector[i], term[self.UNKNOWNS][i])

        return term[self.COEFF] * unknownProduct



class MultivariateSystem:

    def __init__(self, *eq):
        self.sys = list(eq)

        self.N = len(self.sys)

        if not all(X.nbUnknowns is self.N for X in self.sys):
            raise Exception("Error: Number of equations/unknowns mismatch")

    def jacobian_matrix(self):
        J = []
        for eq in self.sys:
            J.append(eq.partial_derivative())

        return J

    def jacobian_matrix_at(self, vector):
        J = []
        for eq in self.sys:
            J.append(eq.partial_derivative_at(vector))

        return J



if __name__ == '__main__':
    m = MultivariateEquations([[4, [0, 2, 3]], [4, [1, 3, 2]]], 9, 3)

    print(m.partial_derivative_at([3, 3, 3]))

    print(MultivariateSystem(m, m, m).jacobian_matrix_at([3, 3, 3]))