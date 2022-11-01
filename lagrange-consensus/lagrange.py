import numpy as np

# Define a function :
# LagrangePolynomial(x) = F(x).D(x) = key(x)
# where F(x) is the Lagrange polynomial
# and D(x) is the test if the public address is a member of the polynomial
# key(x) is the randomly generated bit used as key for the user to claim the tokens

class LagrangePolynomial:

    def __init__(self, X):
        self.n = len(X)

        self.X = np.zeros(self.n)
        self.D_Y = np.zeros(self.n)

        self.modAddress = {}

        key = 1
        ctr = 0
        for address in X:
            key = self.randNum()
            while address % key == 0:
                key = self.randNum()

            # add exponentiation of address for the group
            modAddr = address % key
            self.X[ctr] = modAddr
            self.D_Y[ctr] = key
            self.modAddress[address] = modAddr
            ctr += 1

        assert(len(X) == len(self.D_Y))

    # lagrange basis polynomial
    def Dx(self, x, j) -> np.ndarray:
        b = [(x - self.X[m]) / (self.X[j] - self.X[m])
             for m in range(self.n) if m != j]

        return np.prod(b, axis=0) * self.D_Y[j]

    # returns 1 or 0 if the public address is a member of the polynomial
    def Fx(self, Dy) -> int:
        return 1 if Dy/int(Dy) == 1 else 0

    # returns the key for a public address
    def returnKey(self, x) -> int:
        # x = self.returnModAddress(x)
        Dy = np.sum([self.Dx(x, j) for j in range(self.n)], axis=0)
        Fy = self.Fx(Dy)

        return int(abs(Dy * Fy))

    # returns if the public address matched with the right key
    def finalize(self, x, y) -> int:
        x = self.returnModAddress(x)
        if y != 0 :
            return 1 if self.returnKey(x) == y else 0
        else:
            return 0

    # returns a random number
    def randNum(self) -> np.ndarray:
        return np.random.randint(low=0xFF, high=0xFFFF, size=1, dtype=int)

    def returnModAddress(self, x) -> float:
        return self.modAddress[x][0]