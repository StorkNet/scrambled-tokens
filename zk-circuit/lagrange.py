import numpy as np

class LagrangePoly:

    def __init__(self, X):
        self.n = len(X)
        self.X = np.array(X)

        self.D_Y = []

        for i in range(self.n):
            randChallenge = 1
            while self.X[i] % randChallenge == 0:
                randChallenge = self.randNum()
            self.D_Y.append(randChallenge)

        self.F_Y = np.ones(len(X), dtype=int)

        assert(len(X) == len(self.D_Y) == len(self.F_Y))

    def randNum(self):
        return np.random.randint(low=0xFF, high=0xFFFF, size=1, dtype=int)

    def Dx(self, x, j):
        b = [(x - self.X[m]) / (self.X[j] - self.X[m])
             for m in range(self.n) if m != j]

        return np.prod(b, axis=0) * self.D_Y[j]

    def Fx(self, x, j):
        b = [(x - self.X[m]) / (self.X[j] - self.X[m])
             for m in range(self.n) if m != j]
        return np.prod(b, axis=0) * self.F_Y[j]

    def interpolate(self, x):
        Dy = [self.Dx(x, j) for j in range(self.n)]
        Fy = [self.Fx(x, j) for j in range(self.n)]

        Fy = np.sum(Fy, axis=0)

        if Fy != 1:
            Fy = 0

        return (np.sum(Dy, axis=0) * Fy)[0]

    def challenge(self, x, y):
        return 1 if y == self.interpolate(x) else 0

'''
X = [0x6be986730E72fCd23910D66A1722b4b3611e50D2, 0x07F20B1265059fEb39D605e8476aa51595483Ec6, 0x5F45498761247C2A4609d66E633959e0f9999999, 0x1ab07e29D2ec76117704944DfBDB9dE5b785E8f4, 0xD3358467C97906bA732d0ca4af20f14F0424CD4F]
Y = [0.3, 11, 0.57, 120, 17]

max_addr = 0xffffffffffffffffffffffffffffffffffffffff

def test(x):
    x = abs(x)
    x = x + 1
    x = x//1 
'''