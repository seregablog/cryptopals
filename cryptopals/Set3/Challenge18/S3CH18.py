
import base64


from Set1.Challenge7.S1CH7 import AesEcb


class AesCtr:
    def __init__(self) -> None:
        self.blockSize = 16
        self.aes = AesEcb()

    def encrypt(self, data: bytearray, key: bytearray, nonce: int) -> bytearray:
        counter = 0
        nonceData = nonce.to_bytes(8, 'little')
        encrypted = bytearray()
        for i in range(0, len(data), self.blockSize):
            counterData = counter.to_bytes(8, 'little')
            gamma = self.aes.encrypt(nonceData + counterData, key)
            encrypted += self.__xor(data[i: i + self.blockSize], gamma)
            counter += 1
        return encrypted

    def decrypt(self, data: bytearray, key: bytearray, nonce: int) -> bytearray:
        return self.encrypt(data, key, nonce)

    def __xor(self, x: bytearray, y: bytearray) -> bytearray:
        c = bytearray()
        length = min(len(x), len(y))
        for i in range(length):
            c.append(x[i] ^ y[i])
        
        return c


if __name__ == "__main__":
    aes = AesCtr()
    key = b"YELLOW SUBMARINE"
    nonce = 0
    data = base64.b64decode('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
    print('Decrypted:', aes.decrypt(data, key, nonce).decode('ascii'))
