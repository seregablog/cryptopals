from Set4.Challenge28.S4CH28 import Sha1
from Common.Random import Random
from Common.IntConverter import IntConverter


class Dsa:
    def __init__(self) -> None:
        self.p = int('0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1', 16)
        self.q = int('0xf4f47f05794b256174bba6e9b396a7707e563c5b', 16)
        self.g = int('0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291', 16)
        self.x = None
        self.y = None
        self.random = Random()
        self.converter = IntConverter()
        self.generateKeys()
    
    def generateKeys(self) -> None:
        self.x = self.random.getInt(1, self.q - 1)
        self.y = pow(self.g, self.x, self.p)
    
    def setParameters(self, p: int, g: int, q: int) -> None:
        self.p = p
        self.g = g
        self.q = q
        self.generateKeys()
    
    def setY(self) -> None:
        self.y = y

    def getPublicKey(self):
        return self.p, self.g, self.q, self.y

    def sign(self, hash: bytearray):
        h = self.converter.bytesToInt(hash)
        k = self.random.getInt(1, self.q - 1)
        r = pow(self.g, k, self.p) % self.q
        s = (pow(k, -1, self.q) * (h + self.x * r)) % self.q
        return r, s
        
    def verify(self, hash: bytearray, r: int, s: int) -> bool:
        h = self.converter.bytesToInt(hash)
        w = pow(s, -1, self.q)
        u1 = h * w % self.q
        u2 = r * w % self.q
        v = pow(self.g, u1, self.p) * pow(self.y, u2, self.p) % self.p % self.q
        return v == r


if __name__ == "__main__":
    dsa = Dsa()

    sha1 = Sha1()
    converter = IntConverter()
    hash = sha1.hash(b'Hi world')
    r, s = dsa.sign(hash)
    print('Sign-Verify test: ', dsa.verify(hash, r, s))

    p, g, q, y = dsa.getPublicKey()

    y = int('0x84ad4719d044495496a3201c8ff484feb45b962e7302e56a392aee4abab3e4bdebf2955b4736012f21a08084056b19bcd7fee56048e004e44984e2f411788efdc837a0d2e5abb7b555039fd243ac01f0fb2ed1dec568280ce678e931868d23eb095fde9d3779191b8c0299d6e07bbb283e6633451e535c45513b2d33c99ea17', 16)
    h = int('0xd2d0714f014a9784047eaeccf956520045c45265', 16)
    r = 548099063082341131477253921760299949438196259240
    s = 857042759984254168557880549501802188789837994940

    finish = 2 ** 16
    for k in range(finish):
        x = (pow(r, -1, q) * (k * s - h)) % q
        if pow(g, x, p) == y:
            print('Find key', x)
            print('Key hash: ', sha1.hash(hex(x)[2:].encode()).hex())
            print('Public key correct: ', pow(g, x, p) == y)
            break
