
from Set2.Challenge10.S2CH10 import AesCbc
from Set2.Challenge9.S2CH9 import Pkcs7
from Common.Random import Random

class CbcBitFlipOracle:
    def __init__(self, key, iv) -> None:
        self.key = key
        self.iv = iv
        self.aes = AesCbc()
        self.padding = Pkcs7()
    
    def encrypt(self, text: str)->bytes:
        prefix = 'comment1=cooking%20MCs;userdata='
        postfix = ';comment2=%20like%20a%20pound%20of%20bacon'
        text = text.replace('=', "'='")
        text = text.replace(';', "';'")
        data = bytearray(prefix + text + postfix, 'ascii')
        return self.aes.encrypt(self.padding.pad(data, 16), self.key, self.iv)
    

    def isAdmin(self, data: bytearray)->bool:
        dec = self.padding.unpad(self.aes.decrypt(data, self.key, self.iv))
        return dec.find(b';admin=true;') != -1
    
if __name__ == "__main__":
    oracle = CbcBitFlipOracle(Random().getBytes(16), Random().getBytes(16))
    text = 'XadminYtrueX' + 'A' * 4
    print(ord('X') ^ ord(';')) # 99
    print(ord('Y') ^ ord('=')) # 100
    enc = oracle.encrypt(text)
    
    enc[16] ^= 99
    enc[22] ^= 100
    enc[27] ^= 99
    print('Is admin:', oracle.isAdmin(enc))




