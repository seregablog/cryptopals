import hashlib
from Common.IntConverter import IntConverter
from Common.Random import Random


class SimplySreClient:
    def __init__(self, n: int, g: int) -> None:
        self.n = n
        self.g = g
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
    
    def generateKey(self, pubB: int, salt: int, u: int) -> None:
        x = self.converter.bytesToInt(self.hash.sha256(self.converter.intToBytes(salt) + self.password).digest())
        s = pow(pubB, self.a + u * x, self.n)
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
    converter = IntConverter()

    client = SimplySreClient(N, g)
    passwords = [
        b"client password",
        b"qwerty",
        b"123456"
    ]
    password = passwords[Random().getInt(0, len(passwords) - 1)]

    pubA = client.inizialize(password)
    salt = 2
    b = 3
    u = 4
    pubB = pow(g, b, N)
    client.generateKey(pubB, salt, u)

    for p in passwords:
        x = converter.bytesToInt(hashlib.sha256(converter.intToBytes(salt) + p).digest())
        v = pow(g, x, N)
        s = pow(pubA * pow(v, u, N), b, N)
        key = hashlib.sha256(IntConverter().intToBytes(s)).digest()
        if (key == client.key):
            print('Password finded:', p)
