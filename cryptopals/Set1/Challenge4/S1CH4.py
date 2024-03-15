import sys

from Set1.Challenge3.S1CH3 import OneByteXorDecryptor
from Common.FileReader import FileReader

if __name__ == "__main__":
    d = OneByteXorDecryptor()
    f = FileReader()
    lines = f.readLines(sys.argv[0], 'input.txt')
    min = 1000
    decrypted = None
    key = None
    for hexLine in lines:
        k, m, text = d.decrypt(hexLine)
        if (m < min):
            min = m
            decrypted = text
            key = k
    print('Encrypted:', hexLine)
    print('Key:', hex(key))
    print('Decrypted:', decrypted.decode('ascii'))
    