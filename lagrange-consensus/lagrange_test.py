import lagrange
import numpy as np
from hashlib import sha256

def randNum():
    return np.random.randint(low=0xF001, high=0xFFFF, size=1, dtype=int)[0]

def printSummary(summary):
    print("\n--------------------------------------\nSummary:\n" + summary)

print("Testing lagrange.py")
X_honest = [0x6be986730E72fCd23910D66A1722b4b3611e50D2,
            0x07F20B1265059fEb39D605e8476aa51595483Ec6]

X_attack = [0x1ab07e29D2ec76117704944DfBDB9dE5b785E8f4,
            0xD3358467C97906bA732d0ca4af20f14F0424CD4F]

print("Initializing lagrange object")
alpha = 131
lp = lagrange.LagrangePolynomial(X_honest)

# def ModAddressTest():
# lagrange_test.alpha ** (lagrange_test.X[0] % lagrange_test.lp.returnKey(lagrange_test.X[0])) % lagrange_test.lp.returnKey(lagrange_test.X[0])
# lagrange_test.X[0] % lagrange_test.lp.returnKey(lagrange_test.X[0])
# lagrange_test.alpha
# lagrange_test.lp.returnKey(lagrange_test.X[0])


def FinalizeTest():
    for x_honest in X_honest:
        print("Testing address: 0x%x" % x_honest)
        print("Group address: 0x%x" % lp.returnGroupAddress(x_honest))
        print("Key: 0x%s" % lp.returnKey(lp.returnGroupAddress(x_honest)))
        print("")
        assert(lp.finalize(lp.returnGroupAddress(x_honest),
               lp.returnKey(lp.returnGroupAddress(x_honest))) == 1)

    for x_attack in X_attack:
        print("Testing address: 0x%x" % x_attack)
        print("Key: 0x%s" % lp.returnKey(x_attack))
        print("Finalize: %d" % lp.finalize(
            x_attack, lp.returnKey(x_attack)))
        print("")
        assert(lp.returnKey(x_attack) == ''.zfill(64))

    printSummary("All honest group addresses finalized with 1 \nAll attack group addresses finalized with 0")
