import base64
from Set2.Challenge10.S2CH10 import AesCbc
from Set2.Challenge9.S2CH9 import Pkcs7
from Common.Random import Random

BLOCK_SIZE = 16


class CbcPaddingOracle:

    def __init__(self, key, iv) -> None:
        self.key = key
        self.iv = iv
        self.aes = AesCbc()
        self.padding = Pkcs7()
        self.texts = [
            'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
            'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
            'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
            'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
            'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
            'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
            'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
            'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
            'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
            'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG9',
        ]
    
    def encrypt(self) -> bytes:
        text = bytearray(self.texts[Random().getInt(0, len(self.texts) - 1)], 'ascii')
        return self.aes.encrypt(self.padding.pad(text, BLOCK_SIZE), self.key, self.iv)
    
    def decrypt(self, data) -> bytes:
        dec = self.aes.decrypt(data, self.key, self.iv)
        return self.padding.unpad(dec)


def decryptByte(intermediate, index, oracle, block) -> bytearray:
    padByte = BLOCK_SIZE - index
    for c in range(256):
        tryBlock = bytearray('A' * BLOCK_SIZE, 'ascii')
        for j in range(index, BLOCK_SIZE):
            tryBlock[j] = intermediate[j] ^ padByte
        tryBlock[index] = c
        tryBlock += block
        try:
            oracle.decrypt(tryBlock)
            intermediate[index] = c ^ padByte
            return intermediate
        except:
            continue


def decryptBlock(oracle, block, prevBlock):
    intermediate = bytearray(b'\x00') * BLOCK_SIZE
    for index in range(BLOCK_SIZE - 1, -1, -1):
        intermediate = decryptByte(intermediate, index, oracle, block)
    
    decrypted = bytearray()
    for i in range(BLOCK_SIZE):
        decrypted.append(intermediate[i] ^ prevBlock[i])
    
    return decrypted


if __name__ == "__main__":
    key = Random().getBytes(16)
    iv = Random().getBytes(16)
    oracle = CbcPaddingOracle(key, iv)
    enc = oracle.encrypt()
    prevBlock = iv
    message = bytearray()
    for i in range(0, len(enc), BLOCK_SIZE):
        message += decryptBlock(oracle, enc[i:i + BLOCK_SIZE], prevBlock)
        prevBlock = enc[i: i + BLOCK_SIZE]
    print('Message:', message)
    print('Decoded:', base64.b64decode(Pkcs7().unpad(message)))
