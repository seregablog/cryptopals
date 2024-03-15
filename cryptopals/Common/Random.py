from random import randint


class Random:
    def getInt(self, start: int, finish: int)->int: 
        return randint(start, finish)

    def getBytes(self, length: int)->int:
        bytes = bytearray()
        for i in range(length):
            bytes.append(self.getInt(0, 255))
        return bytes
