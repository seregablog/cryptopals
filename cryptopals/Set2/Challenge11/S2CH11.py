

from Set1.Challenge7.S1CH7 import AesEcb
from Set2.Challenge10.S2CH10 import AesCbc
from Set2.Challenge9.S2CH9 import Pkcs7
from Set1.Challenge8.S1CH8 import detectEcb
from Common.Random import Random



class EcbOrCbcOracle():
    def __init__(self) -> None:
        self.random = Random()
        self.ecb = AesEcb()
        self.cbc = AesCbc()
        self.padding = Pkcs7()

    def ecrypt(self, data: bytearray):
        data = self.__addToData(data)
        data = self.padding.pad(data, 16)
        key = self.random.getBytes(16)
        if (self.random.getInt(0, 1)) == 0:
            mode = 'ecb'
            encrypted = self.ecb.encrypt(data, key)
        else:
            mode = 'cbc'
            iv = self.random.getBytes(16)
            encrypted = self.cbc.encrypt(data, key, iv)
        return encrypted, mode


    
    def __addToData(self, data: bytearray):
        startBytes = self.random.getBytes(self.random.getInt(5, 10))
        finishBytes = self.random.getBytes(self.random.getInt(5, 10))
        return startBytes + data + finishBytes
    
def detectMode(data: bytearray):
    if (detectEcb(data)):
        return 'ecb'
    else:
        return 'cbc'


if __name__ == "__main__":
    count = 100
    data = b"a" * 48 # 4 full block
    oracle = EcbOrCbcOracle()
    wrong = 0
    for i in range(count):
        encrypt, mode = oracle.ecrypt(data)
        answer = detectMode(encrypt)
        if answer != mode:
            wrong += 1
    if wrong > 0:
        print('wrong answers: ', wrong)
    else:
        print('correct')
        