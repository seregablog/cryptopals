import base64
import string

from Set1.Challenge7.S1CH7 import AesEcb
from Set2.Challenge9.S2CH9 import Pkcs7
from Common.Random import Random


class EcbPrefixOracle():
    def __init__(self, key, prefix) -> None:
        self.key = key
        self.prefix = prefix
        self.ecb = AesEcb()
        self.padding = Pkcs7()
        self.secret = base64.b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')
    def encrypt(self, data: bytearray):
        toEncrypt = self.padding.pad(self.prefix + data + self.secret, 16)
        return self.ecb.encrypt(toEncrypt, self.key)


# find two consecutive duplicate blocks and detect prefix length by it
def detectPrefixLength(oracle: EcbPrefixOracle)->int:
    blockSize = 16
    for i in range(1, 256):
        text = bytearray('A' * i, 'ascii')
        enc = oracle.encrypt(text)

        for j in range(blockSize, len(enc), blockSize):
            if enc[j: j + blockSize] == enc[j - blockSize: j]:
                return j - blockSize - (i - 32)

if __name__ == "__main__":
    blockSize = 16
    key = Random().getBytes(16)
    oraclePrefix = Random().getBytes(Random().getInt(1, 100)) 
    oracle = EcbPrefixOracle(key, oraclePrefix)
    oraclePrefixLength = detectPrefixLength(oracle)


    prefixLengthToFullBlock = blockSize - (oraclePrefixLength % blockSize)
    prefixBlockSize = oraclePrefixLength + prefixLengthToFullBlock


    size = 144
    alphabet = string.printable
    answer = bytearray()
    for i in range(size):
        prefix = bytearray('A' * (prefixLengthToFullBlock + size - i - 1), 'ascii')
        correct = oracle.encrypt(prefix)
        for c in alphabet:
            tryPrefix = prefix.copy() + answer
            tryPrefix.append(ord(c))
            enc = oracle.encrypt(tryPrefix)          
            if correct[prefixBlockSize: prefixBlockSize + size] == enc[prefixBlockSize: prefixBlockSize + size]:
                answer.append(ord(c))
                break
    
    print('Decrypted:', answer.decode('ascii'))

