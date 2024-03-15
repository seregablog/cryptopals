import sys

from Common.FileReader import FileReader
from Crypto.Cipher import AES


class AesEcb():
    def encrypt(self, data: bytearray, key: bytearray) -> bytes:
        aes = AES.new(key, AES.MODE_ECB)
        return aes.encrypt(data)
    
    def decrypt(self, encrypted: bytearray, key: bytearray) -> bytes:
        aes = AES.new(key, AES.MODE_ECB)
        return aes.decrypt(encrypted)
        

if __name__ == "__main__":
    f = FileReader()
    data = f.readBase64Line(sys.argv[0], 'input.txt')
    key = b'YELLOW SUBMARINE'
    aes = AesEcb()
    print('Decrypted:', aes.decrypt(data, key).decode('ascii'))
