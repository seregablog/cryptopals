from Set3.Challenge21.S3CH21 import MersenneTwister
from Common.Random import Random


class MersenneCtr:
    def __init__(self) -> None:
        self.blockSize = 32
        self.rng = MersenneTwister()

    def encrypt(self, data: bytearray, key: int) -> bytearray:
        self.rng.seed(key)
        encrypted = bytearray()
        for i in range(0, len(data), self.blockSize):
            gamma = bytearray()
            for j in range(self.blockSize // 8):
                gamma += self.rng.getRandomNumber().to_bytes(8, 'little')
            encrypted += self.__xor(data[i: i + self.blockSize], gamma)
        return encrypted

    def decrypt(self, data: bytearray, key: int) -> bytearray:
        return self.encrypt(data, key)

    def __xor(self, x: bytearray, y: bytearray) -> bytearray:
        c = bytearray()
        length = min(len(x), len(y))
        for i in range(length):
            c.append(x[i] ^ y[i])
        return c


if __name__ == "__main__":
    key = Random().getInt(0, 0xffff)
    ctr = MersenneCtr()
    part = bytearray('A' * 14, 'ascii')
    data = Random().getBytes(Random().getInt(1, 40)) + part

    encrypted = ctr.encrypt(data, key)

    for k in range(0xffff):
        decrypted = ctr.decrypt(encrypted, k)
        if decrypted.find(part) != -1:
            print('Key:', key)
            print('Decrypted:', decrypted)
            break
