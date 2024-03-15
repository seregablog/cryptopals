import sys

from Set1.Challenge6.S1CH6 import RepeatedXorDecryptor
from Set1.Challenge2.S1CH2 import xorBytes
from Common.FileReader import FileReader
from Set3.Challenge19.S3CH19 import CtrOracle


if __name__ == "__main__":
    f = FileReader()
    texts = f.readBase64Lines(sys.argv[0], 'input.txt')
    key = b"YELLOW SUBMARINE"
    nonce = 0
    ctr = CtrOracle(key)
    enc = []
    for t in texts:
        enc.append(ctr.encrypt(t, nonce))
    
    print("Auto decrypt:")
    data = bytearray()
    keyLength = 53
    for t in enc:
        data += t[:keyLength]

    d = RepeatedXorDecryptor()
    
    key1 = d.findKey(data, keyLength)
    
    print('Key', key1.hex())
    for t in enc:
        print(xorBytes(t[:keyLength], key1))

    print("Manual decrypt:")
    key = bytearray.fromhex('76d1cb4bafa246e2e3af035d6c13c372d2ec6cdc986d12decfda1f93afee73182da08ecb117b374bc3dab726b2fc84cdc180ab3549fa6e55d14c6667c96fa5b08086db36a71159f82f9897e3e7d193e58ca19bc8df3957ba9288400a830c213af7618f28cf43fabb353c6d58b3d6537e909389392adf4dc86efc19c71e666b77')

    for t in enc:
        print(xorBytes(t, key[:len(t)]).decode('ascii'))
