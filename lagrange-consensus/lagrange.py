import numpy as np

# Define a function :
# LagrangePolynomial(x) = F(x).D(x) = challengeBit(x)
# where F(x) is the Lagrange polynomial
# and D(x) is the test if the public address is a member of the polynomial
# challengeBit(x) is the randomly generated bit used as key for the user to claim the tokens

class LagrangePolynomial:

    def __init__(self, X):
        self.n = len(X)
        self.X = np.array(X)

        self.D_Y = []

        for i in range(self.n):
            key = 1
            while self.X[i] % key == 0:
                key = self.randNum()
            self.D_Y.append(key)

        assert(len(X) == len(self.D_Y))

    def Dx(self, x, j) -> np.ndarray:
        b = [(x - self.X[m]) / (self.X[j] - self.X[m])
             for m in range(self.n) if m != j]

        return np.prod(b, axis=0) * self.D_Y[j]

    def Fx(self, Dy) -> int:
        return 1 if Dy/int(Dy) == 1 else 0

    def returnChallenge(self, x) -> int:
        Dy = np.sum([self.Dx(x, j) for j in range(self.n)], axis=0)
        Fy = self.Fx(Dy)

        return int(abs(Dy * Fy)[0])

    def finalize(self, x, y) -> int:
        if y != 0 :
            return 1 if self.returnChallenge(x) == y else 0
        else:
            return 0

    def randNum(self) -> np.ndarray:
        return np.random.randint(low=0xFF, high=0xFFFF, size=1, dtype=int)



'''
X = [0x6be986730E72fCd23910D66A1722b4b3611e50D2, 0x07F20B1265059fEb39D605e8476aa51595483Ec6, 0x5F45498761247C2A4609d66E633959e0f9999999, 0x1ab07e29D2ec76117704944DfBDB9dE5b785E8f4, 0xD3358467C97906bA732d0ca4af20f14F0424CD4F]
'''