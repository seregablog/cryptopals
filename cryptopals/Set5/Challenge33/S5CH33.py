from Common.Random import Random


class DiffieHellman:
    def __init__(self, p, g) -> None:
        self.p = p
        self.g = g
        self.random = Random()
        self.secretKey = None
        self.publicKey = None
        self.generateSecretkey()
        self.generatePublicKey()

    def generateSecretkey(self) -> None:
        self.secretKey = self.random.getInt(1, self.p - 1)
    
    def generatePublicKey(self) -> None:
        self.publicKey = pow(self.g, self.secretKey, self.p)
    
    def generateSessionKey(self, publicKey: int) -> int:
        return pow(publicKey, self.secretKey, self.p)


if __name__ == "__main__":
    p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
    g = 2
    a = DiffieHellman(p, g)
    b = DiffieHellman(p, g)
    print('Session keys equals:', a.generateSessionKey(b.publicKey) == b.generateSessionKey(a.publicKey))
