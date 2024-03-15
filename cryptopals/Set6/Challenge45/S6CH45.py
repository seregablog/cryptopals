from Set6.Challenge43.S6CH43 import Dsa
from Set4.Challenge28.S4CH28 import Sha1
from Common.IntConverter import IntConverter


if __name__ == "__main__":
    dsa = Dsa()
    sha1 = Sha1()
    converter = IntConverter()

    print('g = 0')
    p, g, q, y = dsa.getPublicKey()
    dsa.setParameters(p, 0, q)
    hash = sha1.hash(b'Hello, world')
    r, s = dsa.sign(hash)
    print('Signature:', r, s)
    print('Verify text: ', dsa.verify(hash, r, s))
    print('Verify another text: ', dsa.verify(sha1.hash(b'Goodbye, world'), r, s))
    print()

    print('g = p + 1')
    dsa = Dsa()
    p, g, q, y = dsa.getPublicKey()
    dsa.setParameters(p, p + 1, q)
    dsa.y = y
    z = 42
    r = pow(y, z, p) % q
    s = r * pow(z, -1, q) % q
    print('Verify text: ', dsa.verify(sha1.hash(b'Hello, world'), r, s))
    print('Verify another text: ', dsa.verify(sha1.hash(b'Goodbye, world'), r, s))
