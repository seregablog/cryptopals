
import sys

from Set1.Challenge3.S1CH3 import OneByteXorDecryptor
from Set1.Challenge5.S1CH5 import xorEncrypt
from Common.FileReader import FileReader


class RepeatedXorDecryptor:

    def detectKeyLength(self, text: bytearray)->int:
        min = 1000
        length = None
        for keyLength in range (2, 41):
            part1 = text[:keyLength]
            part2 = text[keyLength:2 * keyLength]
            part3 = text[2 * keyLength:3 * keyLength]
            part4 = text[3 * keyLength:4 * keyLength]
            h = (self.__hammingDistance(part1, part2) + self.__hammingDistance(part1, part3) + self.__hammingDistance(part1, part4) + self.__hammingDistance(part2, part3) + self.__hammingDistance(part2, part4) + + self.__hammingDistance(part3, part4)) / 6 / keyLength 
            if (h < min):
                min = h
                length = keyLength
        return length


    def findKey(self, text: bytearray, keyLength: int)->bytearray:
        transposed = self.__transpose(text, keyLength)
        d = OneByteXorDecryptor()
        key = bytearray()
        for i in range(keyLength):
            k, metric, text = d.decrypt(transposed[i].hex())
            key.append(k)
        return key
    
    def __transpose(self, text: bytearray, length: int)->list:
        lines = [bytearray() for i in range(length)]
        counter = 0
        for t in text:
            lines[counter].append(t)
            counter  = (counter + 1) % length
        return lines

    def __bytebyteBitsDiff(self, x: int, y: int)->int:
        c = x ^ y
        bits = 0
        while c > 0:
            bits += c % 2
            c = c // 2
        return bits

    def __hammingDistance(self, x: bytearray, y: bytearray)->int:
        if len(x) != len(y):
            raise Exception('Hamming distance strings not equals length')
        dist = 0
        for i in range(len(x)):
            dist += self. __bytebyteBitsDiff(x[i], y[i])
        return dist




if __name__ == "__main__":
    f = FileReader()
    data = f.readBase64Line(sys.argv[0], 'input.txt')
    decryptor = RepeatedXorDecryptor()
    keyLength = decryptor.detectKeyLength(data)
    print ('Key length:', keyLength)
    key = decryptor.findKey(data, keyLength)

    print('Key:', key.hex())
    print ("Decrypted:")
    decrypted = xorEncrypt(data, key)
    print (decrypted.decode("ascii"))


    # next manual part






