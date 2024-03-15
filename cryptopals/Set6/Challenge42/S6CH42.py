

from Set5.Challenge39.S5CH39 import Rsa
from Common.IntConverter import IntConverter
from Set4.Challenge28.S4CH28 import Sha1


class BleichenbacherOracle:
    def __init__(self, rsa: Rsa)->None:
        self.converter = IntConverter()
        self.rsa = rsa
        self.hashLen = 20
        self.hash = Sha1()        
    
    def verify(self, signature:int, message: bytearray)->bool:
        packet = self.converter.intToBytes(self.rsa.encrypt(signature))

        index = packet.index(b'\x00\x01')
        index = packet.index(b'\x00', index + 1)
        hash = packet[index + 1: index + 1 + self.hashLen]
        if hash != self.hash.hash(message):
            raise Exception('hash check failed')
        
        return True

def cubeRoot(number):
    start = 0
    finish = number

    while (True):
        mid = (start + finish) // 2
        cube = pow(mid, 3)
        if (cube  > number):
            finish = mid
        elif (cube < number):
            start = mid
        else:
            return mid
        if (finish - start <= 1):
            break
        
    return finish


if __name__ == "__main__":
    sha = Sha1()
    bits = 1024
    rsa = Rsa(bits)
    converter = IntConverter()

    message = b'hi mom'
    
    hash = sha.hash(message)
    print('Hash=', hash)
    
    packetLen = bits // 8
    packet = b'\x00\x01' + b'\xff' * (packetLen - len(hash) - 3) + b'\x00' + hash
    
    signature = rsa.decrypt(converter.bytesToInt(packet))
    print('Signature', signature)

    oracle = BleichenbacherOracle(rsa)
    print('Verify: ', oracle.verify(signature, message))


    forgePacket =  b'\x00\x01' + b'\x00' + hash + b'\x00' * (packetLen - len(hash) - 3)
    num = converter.bytesToInt(forgePacket)
    forgeSignature = cubeRoot(num)
    print('Forged Signature', forgeSignature)
    print('Verify forge:', oracle.verify(forgeSignature, message))
    print('Signatuer == Forge:', signature == forgeSignature)



