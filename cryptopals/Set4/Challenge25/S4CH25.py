import sys


from Set3.Challenge18.S3CH18 import AesCtr
from Set1.Challenge2.S1CH2 import xorBytes
from Common.FileReader import FileReader
from Common.Random import Random


class EditCtrOracle():
    def __init__(self) -> None:
        self.ctr = AesCtr()
        self. key = Random().getBytes(16)
        self.nonce = Random().getInt(0, 10)
    
    def encrypt(self, data: bytearray) -> bytearray:
        return self.ctr.encrypt(data, self.key, self.nonce)
    
    def edit(self, ciphertext: bytearray, offset: int, newText: bytearray) -> bytearray:
        text = self.ctr.decrypt(ciphertext, self.key, self.nonce)
        editText = text[:offset] + newText + text[offset + len(newText):]
        return self.ctr.encrypt(editText, self.key, self.nonce)


if __name__ == "__main__":
    data = FileReader().readBase64Line(sys.argv[0], 'input.txt')
    oracle = EditCtrOracle()
    encrypted = oracle.encrypt(data)
    key = oracle.edit(encrypted, 0, bytearray(b'\x00') * len(encrypted))
    print('Decrypt correct:', xorBytes(encrypted, key) == data)
