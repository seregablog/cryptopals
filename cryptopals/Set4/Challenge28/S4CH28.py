
class Sha1:
    def hash(self, data: bytearray)->bytearray:
        paddedData = self.pad(data)
        h0 = 0x67452301
        h1 = 0xEFCDAB89
        h2 = 0x98BADCFE
        h3 = 0x10325476
        h4 = 0xC3D2E1F0

        state = [h0, h1, h2, h3, h4]

        return self.processData(state, paddedData)
    
    def processData(self, state: list, paddedData: bytearray)->bytearray:
        for i in range(0, len(paddedData), 64):
            state = self.__processBlock(state, paddedData[i: i + 64])
        
        hash = bytearray()
        for i in range(0, 5):
            hash.extend(state[i].to_bytes(4, 'big'))
        
        return hash


    def __processBlock(self, state: list, block: bytearray)->list:
        w = [0] * 80
        for i in range(0, 16):
            w[i] = int.from_bytes(block[4 * i: 4 * i + 4], 'big')
        
        for i in range(16, 80):
            w[i] = self.__leftrotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)
        

        a = state[0]
        b = state[1]
        c = state[2]
        d = state[3]
        e = state[4]
        
        for i in range(0, 80):
            
            if 0 <= i <= 19:
                f = (b & c) | ((b ^ 0xffffffff) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = self.__leftrotate(a, 5)
            temp = self.__add32(temp, f)
            temp = self.__add32(temp, e)
            temp = self.__add32(temp, k)
            temp = self.__add32(temp, w[i])
            e = d
            d = c
            c = self.__leftrotate(b, 30)
            b = a
            a = temp

        state[0] = self.__add32(state[0], a)
        state[1] = self.__add32(state[1], b)
        state[2] = self.__add32(state[2], c)
        state[3] = self.__add32(state[3], d)
        state[4] = self.__add32(state[4], e)

        return state
        
    def __leftrotate(self, x:int, n:int)->int:
        mask = 0xffffffff
        return ((x << n) | (x >> 32 - n)) & mask
    
    def __add32(self, x:int, y:int)->int:
        mask = 0xffffffff
        return (x + y) & mask

    def pad(self, data: bytearray):
        length = len(data) * 8
        paddedData = bytearray(data)
        paddedData.append(0x80)
        addedLength = 56 - (len(paddedData) % 64)
        if addedLength < 0:
            addedLength += 64
        
        paddedData.extend(bytearray(b'\x00' * addedLength))
        paddedData.extend(length.to_bytes(8, 'big'))
        return paddedData


        


class Sha1PrefixMac():
    def mac(self, message: bytearray, key: bytearray)->bytearray:
        return Sha1().hash(key + message)


if __name__ == "__main__":
    sha1 = Sha1()

    print('The quick brown fox...:', sha1.hash(bytearray('The quick brown fox jumps over the lazy dog', 'ascii')).hex())

    mac  = Sha1PrefixMac()
    key = b"YELLOW SUBMARINE"

    print('SOME MESSAGE:', mac.mac(key, b"SOME MESSAGE").hex())
    print('ANOTHER MESSAGE:',mac.mac(key, b"ANOTHER MESSAGE").hex())