from Set5.Challenge33.S5CH33 import DiffieHellman


if __name__ == "__main__":
    p = 17
    g = 1
    a = DiffieHellman(p, g)
    b = DiffieHellman(p, g)
    print('g = 1', 'key:', a.generateSessionKey(b.publicKey))

    g = p

    a = DiffieHellman(p, g)
    b = DiffieHellman(p, g)
    print('g = p', 'key:', a.generateSessionKey(b.publicKey))
    
    g = p - 1
    a = DiffieHellman(p, g)
    b = DiffieHellman(p, g)
    print('g = p-1', 'key:', a.generateSessionKey(b.publicKey))
