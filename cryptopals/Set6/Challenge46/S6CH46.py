import base64
from decimal import Decimal, getcontext
from Set5.Challenge39.S5CH39 import Rsa
from Common.IntConverter import IntConverter


class RsaParityOracle:
    def __init__(self) -> None:
        self.rsa = Rsa(512)
    
    def isEven(self, number: int) -> bool:
        decrypted = self.rsa.decrypt(number)
        return decrypted % 2 == 0


if __name__ == "__main__":
    text = base64.b64decode('VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ==')
    converter = IntConverter()
    number = converter.bytesToInt(text)
    oracle = RsaParityOracle()

    encrypted = oracle.rsa.encrypt(number)

    e, n = oracle.rsa.getPublicKey()
    start = Decimal(0)
    finish = Decimal(n)

    c = encrypted
    getcontext().prec = 1024

    while (finish - start > 1):
        c = c * pow(2, e, n)
        
        if oracle.isEven(c):
            finish = (start + finish) / 2
        else:
            start = (start + finish) / 2
    
    findedNumber = int(finish)
    findedText = converter.intToBytes(findedNumber).strip(b'\x00')
    print('Find number:', findedNumber)
    print('As text:', findedText)
    print('Text equals:: ', text == findedText)
