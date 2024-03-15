from Set5.Challenge33.S5CH33 import DiffieHellman
from Set2.Challenge10.S2CH10 import AesCbc
from Set4.Challenge28.S4CH28 import Sha1


class DiffieHellmanAes:
    def __init__(self, p: int, g: int) -> None:
        self.dh = DiffieHellman(p, g)
        self.aes = AesCbc()
        self.sha1 = Sha1()
        self.iv = b"YELLOW SUBMARINE"
    
    def encrypt(self, data: bytearray, publicKey: int):
        sessionKey = self.dh.generateSessionKey(publicKey)
        key = self.sha1.hash(sessionKey.to_bytes(16, 'big'))[:16]
        encrypted = self.aes.encrypt(data, key, self.iv)
        return encrypted, self.iv


if __name__ == "__main__":
    p = 37
    g = 5
    a = DiffieHellmanAes(p, g)
    data = b"Hello alice, bob"
    encrypted, iv = a.encrypt(data, p)
    
    aes = AesCbc()
    sha1 = Sha1()
    key = sha1.hash((0).to_bytes(16, 'big'))[:16]
    print('Correct decrypt:', aes.decrypt(encrypted, key, iv) == data)
