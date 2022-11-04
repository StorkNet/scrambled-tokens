from hashlib import sha256

def generateKey(publicKeyEth) :
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    a = 0x0000000000000000000000000000000000000000000000000000000000000000
    b = 0x0000000000000000000000000000000000000000000000000000000000000007
    storkKey = ( (publicKeyEth**3 + publicKeyEth*a + b) % p ) ** 0.5
    return sha256((str(publicKeyEth) + "scrambled-egg").encode()).hexdigest()[:40]