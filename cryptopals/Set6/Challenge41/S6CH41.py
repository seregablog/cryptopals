


from Set5.Challenge39.S5CH39 import Rsa
from Common.Random import Random


if __name__ == "__main__":
    rsa  = Rsa()
    e, n = rsa.getPublicKey()
    message = 42
    c = rsa.encrypt(message)


    s = Random().getInt(2, 100)
    newC = (pow(s, e, n) * c) % n
    print('Ciphertexts differ:', c != newC)
    p = (rsa.decrypt(newC) * pow(s, -1, n)) % n
    print('Decrypt success:',  p == message)

