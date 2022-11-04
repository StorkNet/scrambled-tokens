import numpy as np
import secp256k1
from math import ceil
from hashlib import sha256

# Define a function :
# LagrangePolynomial(x) = F(x).D(x) = key(x)
# where F(x) is the Lagrange polynomial
# and D(x) is the test if the public address is a member of the polynomial
# key(x) is the randomly generated bit used as key for the user to claim the tokens

class LagrangePolynomial:

    def __init__(self, X):
        self.alpha = self.__randNum()
        self.p = self.__randNum()
        self.scale = 2**80
        self.n = len(X)

        self.X = []
        self.__D_Y = np.zeros(self.n, dtype=float)
        self.__F_Y = np.ones(self.n, dtype=float)

        self.__storkAddressMapping = {}

        ctr = 0
        for address in X:
            storkAddr = int(secp256k1.generateStorkAddress(address), 16)
            self.X.append(storkAddr)
            # self.X[ctr] = storkAddr
            self.__storkAddressMapping[address] = storkAddr
            self.__D_Y[ctr] = int(self.__randNum() * self.scale)
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
    # MAKE THE KEY LARGER SO THERE ARE NO COLLISIONS
    def returnKey(self, storkAddress):
        Dy = np.sum([self.__Dx(storkAddress, j) for j in range(self.n)], axis=0)
        Fy = int(storkAddress in self.X)
        # Fy = (np.sum([self.__Fx(storkAddress, j) for j in range(
        #     self.n)], axis=0))
        # Fy1 = sha256(str((Fy ^ self.scale)).encode()).hexdigest()
        # Fy = 1 - ceil((1/(1 + 2**(-ceil(Fy % self.scale))) - 0.5))
        # return (Fy, int(Fy * self.scale))
        return (self.generateKey(Dy, storkAddress) * Fy).zfill(64)

    # returns if the public address matched with the right key
    def finalize(self, storkAddress, y) -> int:
        if y != ''.zfill(64):
            return 1 if self.returnKey(storkAddress) == y else 0
        else:
            return 0

    # returns a random number
    def __randNum(self) -> np.ndarray:
        return np.random.randint(low=0xF001, high=0xFFFF, size=1, dtype=int)

    def generateKey(self, key, storkAddress) -> str:
        return sha256(str(int(key) ^ int(storkAddress)).encode()).hexdigest()

    def returnStorkAddress(self, x) -> int:
        return self.__storkAddressMapping[x]
