import sys
from Common.FileReader import FileReader


class MersenneTwister:
    def __init__(self) -> None:
        self.w = 32
        self.n = 624
        self.m = 397
        self.r = 31
        self.a = 0x9908b0df
        self.u = 11
        self.d = 0xffffffff
        self.s = 7
        self.b = 0x9d2c5680
        self.t = 15
        self.c = 0xefc60000
        self.l = 18
        self.f = 1812433253

        self.mt = [None for i in range(self.n)]
        
    def seed(self, seed: int) -> None:
        self.mt[0] = seed
        self.index = self.n
        for i in range(1, self.n):
            self.mt[i] = self.__lowestWBits(self.f * (self.mt[i - 1] ^ (self.mt[i - 1] >> (self.w - 2))) + i)

    def seedByState(self, mt: list) -> None:
        self.index = 0
        self.mt = mt.copy()

    def getRandomNumber(self) -> int:
        if self.index > self.n:
            raise Exception('index more than mt')
        
        if self.index == self.n:
            self.__twist()

        y = self.mt[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
 
        self.index = self.index + 1
        return self.__lowestWBits(y)

    def __twist(self) -> None:
        lowerMask = (1 << self.r) - 1
        upperMask = self.__lowestWBits(~lowerMask)
        for i in range(self.n):
            x = (self.mt[i] & upperMask) + (self.mt[(i + 1) % self.n] & lowerMask)
            xA = x >> 1
            if x % 2 != 0:
                xA = xA ^ self.a
            self.mt[i] = self.mt[(i + self.m) % self.n] ^ xA
        self.index = 0

    def __lowestWBits(self, x) -> int:
        mask = (1 << self.w) - 1
        return x & mask


if __name__ == "__main__":
    m = MersenneTwister()
    m.seed(123456)
    f = FileReader()
    numbers = f.readLines(sys.argv[0], 'test.txt')
    for number in numbers:
        randomNumber = m.getRandomNumber()
        if int(number) != randomNumber:
            print('RNG is not correct:' + str(number) + ' ' + str(randomNumber))
            exit()
    print('RNG is correct')
