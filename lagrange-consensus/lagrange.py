from hashlib import sha256
import numpy as np
from math import ceil
from hashlib import sha256

# Define a function :
# LagrangePolynomial(x) = F(x).D(x) = key(x)
# where F(x) is the Lagrange polynomial
# and D(x) is the test if the public address is a member of the polynomial
# key(x) is the randomly generated bit used as key for the user to claim the tokens

class LagrangePolynomial:

    def __init__(self, X):
        self.n = len(X)
        self.alpha = 131
        self.X = np.zeros(self.n)
        self.__D_Y = np.zeros(self.n)
        self.__F_Y = np.ones(self.n)

        self.__groupAddressMapping = {}

        key = 1
        ctr = 0
        for address in X:
            key = self.__randNum()
            while address % key == 0:
                key = self.__randNum()

            modAddr = address % key

            # finding the group element of the address
            groupAddr = self.alpha ** modAddr % key

            self.X[ctr] = groupAddr
            self.__D_Y[ctr] = key
            self.__groupAddressMapping[address] = groupAddr
            ctr += 1

        assert(len(X) == len(self.__D_Y))

    # lagrange basis polynomial
    def __Dx(self, x, j) -> np.ndarray:
        b = [(x - self.X[m]) / (self.X[j] - self.X[m])
             for m in range(self.n) if m != j]

        return np.prod(b, axis=0) * self.__D_Y[j]

    # returns 1 or 0 if the public address is a member of the polynomial
    def __Fx(self, x, j) -> int:
        b = [(x - self.X[m]) / (self.X[j] - self.X[m])
             for m in range(self.n) if m != j]

        return np.prod(b, axis=0) * self.__F_Y[j]

    # returns the key for a public address
    def returnKey(self, x):
        Dy = np.sum([self.__Dx(x, j) for j in range(self.n)], axis=0)
        Fy = np.sum([self.__Fx(x, j) for j in range(self.n)], axis=0)
        # Fy = 1 - ceil((1/(1 + 2**(-Fy)) - 0.5))
        # return Fy
        n = int(abs(Dy * Fy) * 2 ** 40)
        return sha256(str(n ^ x).encode()).hexdigest()

    # returns if the public address matched with the right key
    def finalize(self, x, y) -> int:
        if y != 0 :
            return 1 if self.returnKey(x) == y else 0
        else:
            return 0

    # returns a random number
    def __randNum(self) -> np.ndarray:
        return np.random.randint(low=0xF001, high=0xFFFF, size=1, dtype=int)

    def returnGroupAddress(self, x) -> int:
        return self.__groupAddressMapping[x][0]
