import lagrange
import numpy as np

print("Testing lagrange.py")
X = [0x6be986730E72fCd23910D66A1722b4b3611e50D2, 0x07F20B1265059fEb39D605e8476aa51595483Ec6,
     0x5F45498761247C2A4609d66E633959e0f9999999, 0x1ab07e29D2ec76117704944DfBDB9dE5b785E8f4, 0xD3358467C97906bA732d0ca4af20f14F0424CD4F]

print("Initializing lagrange object")
alpha = np.random.randint(low=0x03, high=0xF, size=1, dtype=int)[0]
lp = lagrange.LagrangePolynomial(X)

# def ModAddressTest():
# lagrange_test.alpha ** (lagrange_test.X[0] % lagrange_test.lp.returnKey(lagrange_test.X[0])) % lagrange_test.lp.returnKey(lagrange_test.X[0])
# lagrange_test.X[0] % lagrange_test.lp.returnKey(lagrange_test.X[0])
# lagrange_test.alpha
# lagrange_test.lp.returnKey(lagrange_test.X[0])


def FinalizeTest():
    for x in X:
        print("Testing address: 0x%x" % x)
        print("Group address: 0x%x" % lp.returnGroupAddress(x))
        print("Key: 0x%x" % lp.returnKey(x))
        print("Finalize: %d" % lp.finalize(x, lp.returnKey(lp.returnGroupAddress(0x6be986730E72fCd23910D66A1722b4b3611e50D2))))
        print("")
        assert(lp.finalize(x, lp.returnKey(x)) == 1)
    print("All addresses finalized with 1")