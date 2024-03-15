
class Base64:
    BASE_64_SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    PAD = '='
    THREE_BYTES_LENTH = 6

    def encodeHex(self, hex: str) -> str:
        base64 = ''
        for i in range(0, len(hex), self.THREE_BYTES_LENTH):
            next24Bits = hex[i: i + self.THREE_BYTES_LENTH]
            base64 += self.__convert24BitsToSymbols(next24Bits)
        return base64
    
    def __convert24BitsToSymbols(self, bits: str) -> str:
        symbols = []
        if (len(bits) % self.THREE_BYTES_LENTH == 0):
            symbols = self.__divide24Bits(bits)
        elif (len(bits) % self.THREE_BYTES_LENTH == 2):
            bits += '0000'
            symbols = self.__divide24Bits(bits)
            symbols[2] = symbols[3] = self.PAD
        elif (len(bits) % self.THREE_BYTES_LENTH == 4):
            bits += '00'
            symbols = self.__divide24Bits(bits)
            symbols[3] = self.PAD
        else:
            raise Exception('incorrect hex string')

        return ''.join(symbols)
    
    def __divide24Bits(self, bits: str) -> str:
        symbols = []
        mask = 0x3f
        value = int(bits, 16)

        for i in range(4):
            symbols.append(self.BASE_64_SYMBOLS[value & mask])
            value = value >> self.THREE_BYTES_LENTH
        symbols.reverse()
        return symbols


if __name__ == "__main__":
    b = Base64()
    hex = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    print('Base64:', b.encodeHex(hex))
