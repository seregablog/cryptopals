
class Pkcs7():
    def pad(self, data: bytearray, bytesLength: int)->bytearray:
        bytesToAdd = bytesLength - (len(data) % bytesLength)
        for i in range(bytesToAdd):
            data.append(bytesToAdd)
        
        return data
    
    def unpad(self, data: bytearray)->bytearray:
        lastByte = data[-1]
        length = int(lastByte)
        if (length < 1 or length > 16):
            raise Exception('incorrect pkcs7 padding')
        for i in range(length):
            if data[len(data) - i - 1] != lastByte:
                raise Exception('incorrect pkcs7 padding')
        
        unpadded = data[:-length]
        return unpadded




if __name__ == "__main__":
    pad = Pkcs7()
    bytes = bytearray('YELLOW SUBMARINE', 'ascii')
    padded = pad.pad(bytes, 20)
    print('Padded:', padded)
    print('Unpadded:', pad.unpad(padded))
