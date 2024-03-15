from Common.Random import Random
from Set3.Challenge18.S3CH18 import AesCtr


class CtrBitFlipOracle:
    def __init__(self) -> None:
        self. key = Random().getBytes(16)
        self.nonce = Random().getInt(0, 10)
        self.aes = AesCtr()
    
    def encrypt(self, text: str) -> bytearray:
        prefix = 'comment1=cooking%20MCs;userdata='
        postfix = ';comment2=%20like%20a%20pound%20of%20bacon'
        text = text.replace('=', "'='")
        text = text.replace(';', "';'")
        data = bytearray(prefix + text + postfix, 'ascii')
        return self.aes.encrypt(data, self.key, self.nonce)
    
    def isAdmin(self, data: bytearray):
        dec = self.aes.decrypt(data, self.key, self.nonce)
        return dec.find(b';admin=true;') != -1


if __name__ == "__main__":
    oracle = CtrBitFlipOracle()
    text = 'XadminYtrueX'
    print(ord('X') ^ ord(';'))  # 99
    print(ord('Y') ^ ord('='))  # 100
    enc = oracle.encrypt(text)
    
    enc[32] ^= 99
    enc[38] ^= 100
    enc[43] ^= 99
    print('Is admin:', oracle.isAdmin(enc))
