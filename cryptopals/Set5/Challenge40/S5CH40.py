from Set5.Challenge39.S5CH39 import Rsa


if __name__ == "__main__":
    rsa1  = Rsa()
    rsa2  = Rsa()
    rsa3  = Rsa()
    message = 42424242424242
    c1 = rsa1.encrypt(message)
    c2 = rsa2.encrypt(message)
    c3 = rsa3.encrypt(message)

    e, n1 = rsa1.getPublicKey()
    e, n2 = rsa2.getPublicKey()
    e, n3 = rsa3.getPublicKey()


    m1 = n2 * n3
    m2 = n1 * n3
    m3 = n1 * n2

    x = c1 * m1 * pow(m1, -1, n1) + c2 * m2 * pow(m2, -1, n2) + c3 * m3 * pow(m3, -1, n3)
    x %= n1 * n2 * n3
    m = round(pow(x, 1/3))

    
    
    print('Find message correct:', m == message)


