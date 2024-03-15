
from Set2.Challenge9.S2CH9 import Pkcs7


if __name__ == "__main__":
    p  = Pkcs7()
    print(p.unpad(b"ICE ICE BABY\x04\x04\x04\x04"))
    