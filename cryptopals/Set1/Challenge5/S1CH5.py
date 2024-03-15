def xorEncrypt(text: bytearray, key: bytearray) -> bytearray:
    encrypt = bytearray()
    keyLength = len(key)
    keyIndex = 0
    for t in text:
        encrypt.append(t ^ key[keyIndex])
        keyIndex = (keyIndex + 1) % keyLength
    return encrypt


if __name__ == "__main__":
    text = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    key = 'ICE'

    print('Text:', text)
    print('Key:', key)

    e = xorEncrypt(bytearray(text, 'ascii'), bytearray(key, 'ascii'))
    print('Encrypted:', e.hex())
