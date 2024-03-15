from Set3.Challenge21.S3CH21 import MersenneTwister
from Common.Random import Random

BITS_LENGTH = 32


def intToBits(x) -> list:
    bits = [0] * BITS_LENGTH
    i = 0
    while x > 0:
        bits[i] = x % 2
        x = x >> 1
        i += 1
    return bits


def bitsToInt(bits) -> int:
    x = 0
    bits.reverse()
    for b in bits:
        x = (x << 1) ^ b
    return x


# revert x = y ^ ((y << k) & m)
def revertLeft(x, k, m) -> int:
    xBits = intToBits(x)
    mBits = intToBits(m)
    yBits = [0] * BITS_LENGTH

    for i in range(k):
        yBits[i] = xBits[i]
    
    for i in range(k, BITS_LENGTH):
        yBits[i] = xBits[i] ^ yBits[i - k] & mBits[i]

    return bitsToInt(yBits)


# revert x = y ^ ((y >> k) & m)
def revertRight(x, k, m) -> int:
    xBits = intToBits(x)
    mBits = intToBits(m)
    yBits = [0] * BITS_LENGTH

    for i in range(BITS_LENGTH - 1, BITS_LENGTH - 1 - k, -1):
        yBits[i] = xBits[i]

    for i in range(BITS_LENGTH - 1 - k, -1, -1):
        yBits[i] = xBits[i] ^ yBits[i + k] & mBits[i]

    return bitsToInt(yBits)


'''
Revert
y = y ^ ((y >> u) & d)
y = y ^ ((y << s) & b)
y = y ^ ((y << t) & c)
y = y ^ (y >> l)
'''


def revertState(y):
    l = 18
    t = 15
    c = 0xefc60000
    s = 7
    b = 0x9d2c5680
    u = 11
    d = 0xffffffff
    y = revertRight(y, l, 0xffffffff)
    y = revertLeft(y, t, c)
    y = revertLeft(y, s, b)
    y = revertRight(y, u, d)
    return y


if __name__ == "__main__":
    n = 624
    state = []
    for i in range(n):
        state.append(Random().getInt(0, 1000))
    rng = MersenneTwister()
    rng.seedByState(state)
    initialOutput = rng.getRandomNumber()
    
    print('Initial output', initialOutput)
    reversedState = [0] * n
    
    output = initialOutput
    for i in range(n):
        reversedState[i] = revertState(output)
        output = rng.getRandomNumber()
    print('State equals', state == reversedState)
    reversedRng = MersenneTwister()
    reversedRng.seedByState(reversedState)
    reversedOutput = reversedRng.getRandomNumber()
    print('Reversed output', reversedOutput)
    print('Output equals', initialOutput == reversedOutput)
