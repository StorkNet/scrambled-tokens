import numpy as np

class LagrangePoly:

    def __init__(self, X, Y):
        self.n = len(X)
        self.X = np.array(X)
        self.D_Y = np.array(Y)
        self.F_Y = np.ones(len(X), dtype=int)
        assert(len(X) == len(self.D_Y) == len(self.F_Y))

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

        return np.sum(Dy, axis=0)

'''
X = [0x6be986730E72fCd23910D66A1722b4b3611e50D2, 0x6be986730E72fCd23910D66A1722b4b3611e50D2, 0x5F45498761247C2A4609d66E633959e0f9999999, 0x1ab07e29D2ec76117704944DfBDB9dE5b785E8f4, 0xD3358467C97906bA732d0ca4af20f14F0424CD4F]
Dx_Range = [0.3, 11, 0.57, 120, 17]

max_addr = 0xffffffffffffffffffffffffffffffffffffffff
'''