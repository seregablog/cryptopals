import hashlib
from Common.Random import Random
from Common.IntConverter import IntConverter


class SreServer:
    def __init__(self, n: int, g: int, k: int) -> None:
        self.n = n
        self.g = g
        self.k = k
        self.random = Random()
        self.hash = hashlib
        self.converter = IntConverter()
        self.salt = None
        self.v = None
        self.key = None

    def inizialize(self, password: bytearray) -> None:
        self.salt = self.random.getInt(1, self.n - 1)
        x = self.converter.bytesToInt(self.hash.sha256(self.converter.intToBytes(self.salt) + password).digest())
        self.v = pow(self.g, x, self.n)
    
    def generateKey(self, pubA: int):
        b = self.random.getInt(1, self.n - 1)
        pubB = (self.k * self.v + pow(self.g, b, self.n)) % self.n
        u = self.converter.bytesToInt(self.hash.sha256(self.converter.intToBytes(pubA) + self.converter.intToBytes(pubB)).digest())
        s = pow(pubA * pow(self.v, u, self.n), b, self.n)
        self.key = self.hash.sha256(self.converter.intToBytes(s)).digest()
        return self.salt, pubB


class SreClient:
    def __init__(self, n: int, g: int, k: int) -> None:
        self.n = n
        self.g = g
        self.k = k
        self.random = Random()
        self.hash = hashlib
        self.converter = IntConverter()
        self.a = None
        self.pubA = None
        self.password = None
    
    def inizialize(self, password: bytearray) -> int:
        self.password = password
        self.a = self.random.getInt(1, self.n - 1)
        self.pubA = pow(self.g, self.a, self.n)
        return self.pubA
    
    def generateKey(self, pubB: int, salt: int) -> None:
        u = self.converter.bytesToInt(self.hash.sha256(self.converter.intToBytes(self.pubA) + self.converter.intToBytes(pubB)).digest())
        x = self.converter.bytesToInt(self.hash.sha256(self.converter.intToBytes(salt) + self.password).digest())
        s = pow(pubB - self.k * pow(self.g, x, self.n), self.a + u * x, self.n)
        self.key = self.hash.sha256(self.converter.intToBytes(s)).digest()

    
if __name__ == "__main__":
    N = """00:c0:37:c3:75:88:b4:32:98:87:e6:1c:2d:a3:32:
       4b:1b:a4:b8:1a:63:f9:74:8f:ed:2d:8a:41:0c:2f:
       c2:1b:12:32:f0:d3:bf:a0:24:27:6c:fd:88:44:81:
       97:aa:e4:86:a6:3b:fc:a7:b8:bf:77:54:df:b3:27:
       c7:20:1f:6f:d1:7f:d7:fd:74:15:8b:d3:1c:e7:72:
       c9:f5:f8:ab:58:45:48:a9:9a:75:9b:5a:2c:05:32:
       16:2b:7b:62:18:e8:f1:42:bc:e2:c3:0d:77:84:68:
       9a:48:3e:09:5e:70:16:18:43:79:13:a8:c3:9c:3d:"""
     
    N = int("".join(N.split()).replace(":", ""), 16)
    g = 2
    k = 3

    server = SreServer(N, g, k)
    client = SreClient(N, g, k)
    password = b"client password"

    pubA = client.inizialize(password)
    server.inizialize(password)

    salt, pubB = server.generateKey(pubA)
    client.generateKey(pubB, salt)

    print("Server key:", server.key.hex())
    print("Client key:", client.key.hex())
    print('Keys equals:', server.key == client.key)
