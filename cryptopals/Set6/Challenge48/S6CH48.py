from Set5.Challenge39.S5CH39 import Rsa
from Common.IntConverter import IntConverter


class PkcsRsaOracle:
    def __init__(self, k: int) -> None:
        self.k = k
        bits = (k // 2) * 8
        self.rsa = Rsa(bits)
        self.converter = IntConverter()
    
    def isCorrect(self, number: int) -> bool:
        decrypt = self.rsa.decrypt(number)
        bytes = self.converter.intToBytes(decrypt, self.k)
        return bytes[0] == 0x00 and bytes[1] == 0x02


def pkcsPad(data: bytearray, k: int) -> bytearray:
    d = len(data)
    pad = b'\xff' * (k - d - 3)
    return b'\x00\x02' + pad + b'\x00' + data


class Segment:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b
    
    def length(self) -> int:
        return self.b - self.a
    
    def isPoint(self) -> bool:
        return self.length() == 0
    
    def __str__(self) -> str:
        return '[' + str(self.a) + ',' + str(self.b) + ']'
    
    def __eq__(self, __o: object) -> bool:
        return self.a == __o.a and self.b == __o.b
    
    def __hash__(self) -> int:
        return hash(str(self.a) + str(self.b))


def ceil(x, y) -> int:
    return x // y + int(x % y != 0)


def findS(start: int, oracle: PkcsRsaOracle, c: int, e: int, n: int) -> int:
    s = start
    while True:
        cn = c * pow(s, e, n)
        if oracle.isCorrect(cn):
            break

        s += 1
    
    print('s=', s)
    return s


def unionOneSegment(segment: Segment, s: int, n: int, B: int) -> set:
    a = segment.a
    b = segment.b

    r1 = (a * s - 3 * B + 1) // n
    r2 = (b * s - 2 * B) // n

    newSegments = set()

    for r in range(r1, r2 + 1):
        start = max(a, ceil((2 * B + r * n), s))
        finish = min(b, (3 * B - 1 + r * n) // s)
        if (start <= finish):
            sgm = Segment(start, finish)
            if sgm not in newSegments:
                newSegments.add(sgm)
    
    return newSegments


def union(M: set, s: int, n: int, B: int) -> set:
    newM = set()
    for segment in M:
        newM = newM.union(unionOneSegment(segment, s, n, B))
    
    return newM


def printSegments(M: set) -> None:
    for segment in M:
        print(segment, segment.length(),)
    print()


def findSForOneSegment(a: int, b: int, sPrev: int, B: int, c: int, e: int, n: int) -> int:
    r = 2 * (b * sPrev - B) // n

    print('r=', r)

    while True:
        for s in range((2 * B + r * n) // b, (3 * B + r * n) // a + 1):
            cn = c * pow(s, e, n)
            if oracle.isCorrect(cn):
                print('s=', s)
                return s
        r += 1


if __name__ == "__main__":
    k = 96
    B = 2 ** (8 * (k - 2))
    oracle = PkcsRsaOracle(k)
    converter = IntConverter()
    e, n = oracle.rsa.getPublicKey()
    
    data = b"H"
    padData = pkcsPad(data, k)
    number = converter.bytesToInt(padData)
    
    c = oracle.rsa.encrypt(number)

    print('Start')

    M = set([Segment(2 * B, 3 * B)])

    s = findS(n // (3 * B), oracle, c, e, n)
    M = union(M, s, n, B)
    print('S1 finded')

    while True:
        printSegments(M)
        if (len(M) >= 2):
            print('two or more segments')
            s = findS(s + 1, oracle, c, e, n)
            M = union(M, s, n, B)
            continue
        elif (len(M) == 1):
            print('one segment')
            segment = M.pop()
            M.add(segment)
            if segment.isPoint():
                print('finish search')
                break
            s = findSForOneSegment(segment.a, segment.b, s, B, c, e, n)
            M = union(M, s, n, B)
            continue
    
    print('Find number correct:', M.pop().a == number)
