from Set4.Challenge28.S4CH28 import Sha1, Sha1PrefixMac


class Sha1PrefixOracle():
    def __init__(self) -> None:
        self.key = b"YELLOW SUBMARINE"
    
    def mac(self, data):
        return Sha1PrefixMac().mac(data, self.key)


if __name__ == "__main__":
    mac = Sha1PrefixMac()
    sha1 = Sha1()
    oracle = Sha1PrefixOracle()
    text = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    textMac = oracle.mac(text)
    
    paddedText = sha1.pad(b'A' * 16 + text)
    newSha1StateText = sha1.pad(paddedText + b';admin=true')

    state = []
    for i in range(0, len(textMac), 4):
        state.append(int.from_bytes(textMac[i: i + 4], 'big'))

    forgedMac = sha1.processData(state, newSha1StateText[newSha1StateText.find(b';admin=true'):])

    print('Mac forged:', oracle.mac(paddedText[paddedText.find(text):] + b';admin=true') == forgedMac)
