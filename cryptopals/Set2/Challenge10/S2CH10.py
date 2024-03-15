import sys
from Set1.Challenge7.S1CH7 import AesEcb
from Set1.Challenge2.S1CH2 import xorBytes
from Common.FileReader import FileReader


class AesCbc():
    def encrypt(self, data: bytearray, key: bytearray, iv: bytearray) -> bytearray:
        aes = AesEcb()
        encrypted = bytearray()
        blockSize = 16
        previous = iv
        for i in range(0, len(data), blockSize):
            block = data[i: i + blockSize]
            encryptedBlock = aes.encrypt(xorBytes(block, previous), key)
            encrypted.extend(encryptedBlock)
            previous = encryptedBlock
        return encrypted
    
    def decrypt(self, encrypted: bytearray, key: bytearray, iv: bytearray) -> bytearray:
        aes = AesEcb()
        decrypted = bytearray()
        blockSize = 16
        previous = iv
        for i in range(0, len(encrypted), blockSize):
            block = encrypted[i: i + blockSize]
            decrypted.extend(xorBytes(aes.decrypt(block, key), previous))
            previous = block
        return decrypted
    

if __name__ == "__main__":
    f = FileReader()
    a = AesCbc()
    data = f.readBase64Line(sys.argv[0], 'input.txt')
    key = b'YELLOW SUBMARINE'
    iv = bytearray(b'\x00') * 16
    print('Decryped:')
    print(a.decrypt(data, key, iv).decode('ascii'))
