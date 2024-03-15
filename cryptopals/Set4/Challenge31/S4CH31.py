import time
from Set1.Challenge2.S1CH2 import xorBytes
from Set4.Challenge28.S4CH28 import Sha1


class HmacSha1:
    def __init__(self) -> None:
        self.sha1 = Sha1()
        self.b = 64
        self.L = 20
        self.ipad = bytearray.fromhex('36' * self.b)
        self.opad = bytearray.fromhex('5c' * self.b)
    
    def hmac(self, data: bytearray, key: bytearray) -> bytearray:
        k0 = self.__alignKey(key)

        return self.sha1.hash(xorBytes(k0, self.opad) + self.sha1.hash(xorBytes(k0, self.ipad) + data))

    def __alignKey(self, key: bytearray) -> bytearray:
        if len(key) > self.b:
            return self.sha1.hash(key) + bytearray.fromhex('00' * (self.b - self.L))
        elif len(key) < self.b:
            return key + bytearray.fromhex('00' * (self.b - len(key)))
        else:
            return key
    

class HmacTimeOracle:
    def __init__(self) -> None:
        self.hmac = HmacSha1()
        self.key = b"YELLOW SUBMARINE"

    def verify(self, data: bytearray, signature: bytearray) -> bool:
        return self.__insecureEquals(self.hmac.hmac(data, self.key), signature)
        
    def __insecureEquals(self, x: bytearray, y: bytearray) -> bool:
        for i in range(20):
            if x[i] != y[i]:
                return False
            time.sleep(0.00005)
        return True


if __name__ == "__main__":
    hmac = HmacSha1()
    print('Hmac correct:', hmac.hmac(b"Hello World", bytearray.fromhex('707172737475767778797a7b7c7d7e7f80818283')).hex() == '2e492768aa339e32a9280569c5d026262b912431')

    oracle = HmacTimeOracle()
    text = b"Hello world"
    signature = bytearray().fromhex('00' * 20)
    for i in range(20):
        times = [0] * 256
        nextByte = None
        min = 0
        for c in range(256):
            start = time.time()
            oracle.verify(text, signature[:i] + c.to_bytes(1, 'big') + signature[i + 1:])
            timeDiff = time.time() - start
            if timeDiff > min:
                min = timeDiff
                nextByte = c
        signature[i] = nextByte
        print('Signature:', i, signature.hex())
    
    print('Signature verify:', oracle.verify(text, signature))
