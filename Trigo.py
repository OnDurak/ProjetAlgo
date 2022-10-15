#Idée : Une équation est Somme: (b * fonctionTrigo(k * x))
# Représenter une équation, c'est représenter un tableau de terme
# la fonction sinus est representé par la valeur 0 et la fonction sinus par la valeur 1
# Représenter un terme est un tableau avec la constante b en premier élément et la fonction trigonometrique  en second élément et la constante k en troisieme du terme
# Exemple : [[3, 0, 1], [2, 1, 5], 5 ] => 3 sin(X) + 2 cos (5x) = 5

# Supposer que les équations sont passées sous la forme décrite au dessus (ou faire une fonction transformant vers ce format (parse_equations))



class TrigoEquation:

    def __init__(self, eq, result):
            self.result = result
            self.eq = eq

    def get_equation(self):
        return self.eq
    
    def get_result(self):
        return self.result

    def set_equation(self, equation):
        self.eq = equation

    def set_result(self, result):
        self.result = result

    # derive une equation trigonometrique
    def trigo_derivative(self):

        for i in range(len(self.eq)):
                    
                        
            self.eq[i][0] *= self.eq[i][2]
            if self.eq[i][1] == 0:
                self.eq[i][1] = 1
            else:
                if self.eq[i][1] == 1:
                    self.eq[i][1] = 0
                    self.eq[i][0] = - self.eq[i][0]
                else:
                    print("the value takes the sinus or the cosine is not in accordance with the data representation model\n" ) 
                            
        return self.eq

    # apelle les fonction pour dériver et evaluer une equation (à completer)
    def Trigo(self, unknow):
        derivateTrigo = self.trigo_derivative()
        evaluatedTrigo = 0

        
        evaluatedTrigo = self.evaluate_Trigo(unknow)

        return derivateTrigo

    # Evalue une équation trigo (à completer)
    def evaluate_Trigo(self, unknow):
        sum = 0
        for i in range(2):
            sum += self.taylor(unknow)

        return sum

    # developement de taylor pour evaluer la valeur d'un cos ou d'un sin (à completer)
    def taylor(self, unknow):

        return 0


if __name__ == '__main__':
    m = TrigoEquation([[3, 0, 7], [2, 1, 5], [2, 0, 5]], 9)
    print(m.eq)
    print("\n")
    print(m.trigo_derivative())
    
    
    

    