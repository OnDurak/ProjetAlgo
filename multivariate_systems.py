# Idea : an equation is a Sum: (b * Product pow(x_j, kij))
# Representing an equation is representing an array of terms
# Representing a term is representing an array with the coefficient b as the first element and an array containing
# all the exponent value of each unknowns for the term as the second element
# Example : [ [5, [3, 0, 1] ] ,... ] => 5*(x^3 * 1 * z) + ...

# We suppose that the equation given to this class are represented using this encoding
import random as rand


class MultivariateEquations:
    B_INDEX = 0
    POW_INDEX = 1

    def __init__(self, eq, result, nbUnknowns):
        self.result = result
        self.nbUnknowns = nbUnknowns
        self.eq = eq
        self.J = self.__partial_derivative()

        if not all(len(T[self.POW_INDEX]) is self.nbUnknowns for T in self.eq):
            raise Exception("Error: terms have different number of unknowns")

    # Create the jacobian vector of the equation symbolically (private func because we build this in the constructor)
    def __partial_derivative(self):
        partialDerivatives = []

        for i in range(self.nbUnknowns):
            currTerm = []
            for term in self.eq:
                currTerm.append(self.__derivate(term, i))
            partialDerivatives.append(currTerm)

        return partialDerivatives

    # Function returning the derivative with respect to unknownIndex of the calling equation (private func because only
    # used internally)
    def __derivate(self, term, unknownIndex):
        newTerm = term.copy()
        newTerm[self.POW_INDEX] = newTerm[self.POW_INDEX].copy()

        newTerm[self.B_INDEX] *= newTerm[self.POW_INDEX][unknownIndex]

        if newTerm[self.POW_INDEX][unknownIndex] > 0:
            newTerm[self.POW_INDEX][unknownIndex] -= 1

        return newTerm

    # Compute the jacobian vector of the equation given a vector (numerical value)
    def partial_derivative_at(self, vector):
        evaluatedJacVector = []

        for eq in self.J:
            evaluatedJacVector.append(self.evaluate(eq, vector))

        return evaluatedJacVector

    def read_equation_poly(nbrEq, file):
        for i in range(int(nbrEq)):
            file_equation = 
        res = file_equation.split('; ')
        result = res.pop()
        result = int(result)
        for i in range(len(res)):
            res[i] = res[i].strip('][').split(',')
            res[i][0] = int(res[i][0])
            res[i][1] = int(res[i][1])

        polyEq = res
        return PolynomialEquations(polyEq, result)

    # Evaluate the equation given a vector Sum: (b * Product pow(x_i, k_i)), where x_i belongs to vector
    def evaluate(self, eq, vector):
        sum = 0
        for term in eq:
            sum += self.evaluate_term(term, vector)

        return sum

    # Evaluate the equation given a vector (Sum: (b * Product pow(x_i, k_i))) - c, where x_i belongs to vector
    def evaluate_eq(self, vector):
        sum = self.evaluate(self.eq, vector)

        return sum - self.result

    # Evaluate a term of the equation given a vector (b * Product pow(x_i, k_i), where x_i belongs to vector
    def evaluate_term(self, term, vector):
        if self.nbUnknowns != len(vector):
            raise Exception("cannot evaluate a term : input vector length doesn't match unknowns number")

        product = 1
        for i in range(self.nbUnknowns):
            product *= pow(vector[i], term[self.POW_INDEX][i])

        return term[self.B_INDEX] * product

    # Class method that returns a random equation given the number of terms and unknowns
    @classmethod
    def random_equation(cls, n, N):
        eq = []
        for i in range(n):
            exp = rand.sample(range(0, 10), N)
            eq.append([rand.randint(-10, 10), exp])

        return MultivariateEquations(eq, rand.randint(-10, 10), N)

    # Function printing the equation in a pretty way
    def __str__(self):
        s = ""
        n = len(self.eq)
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

        for i in range(n):
            exp = ""
            k = 0
            for j in self.eq[i][1]:
                term = f'x{k}'.translate(SUB)
                term = f'{term}{j} '.translate(SUP)
                exp += term
                k += 1
            if i == n - 1:
                s += f'{self.eq[i][0]}({exp}) = {self.result}\n'
            else:
                s += f'{self.eq[i][0]}({exp}) + '

        return s


# Class storing instances of MultivariateEquations in an array as well as implementing functions related to systems
class MultivariateSystem:

    def __init__(self, *eq):
        self.sys = list(eq)

        self.N = len(self.sys)

        if not all(X.nbUnknowns is self.N for X in self.sys):
            raise Exception("Error: Number of equations/unknowns mismatch")

    def jacobian_matrix(self):
        J = []
        for eq in self.sys:
            J.append(eq.J)

        return J

    def jacobian_matrix_at(self, vector):
        J = []
        for eq in self.sys:
            J.append(eq.partial_derivative_at(vector))

        return J

    def evaluate(self, vector):
        F = []
        for eq in self.sys:
            F.append(eq.evaluate_eq(vector))

        return F

    # Class method that returns a random system given the number n of unknowns/equations
    @classmethod
    def random_system(cls, n):
        sys = []
        for i in range(n):
            sys.append(MultivariateEquations.random_equation(rand.randint(int(n/2), n), n))

        m = MultivariateSystem()
        m.N = n
        m.sys = sys

        return m

    # Function printing the system in a pretty way
    def __str__(self):
        s = ""
        i = 0
        for eq in self.sys:
            s += str(i) + " : " + str(eq) + "\n"
            i += 1

        return s
