from Set6.Challenge43.S6CH43 import Dsa


if __name__ == "__main__":
    dsa = Dsa()
    p, g, q, y = dsa.getPublicKey()

    m1 = int('a4db3de27e2db3e5ef085ced2bced91b82e0df19', 16)
    s1 = 1267396447369736888040262262183731677867615804316
    m2 = int('d22804c4899b522b23eda34d2137cd8cc22b9ce8', 16)
    s2 = 1021643638653719618255840562522049391608552714967
    r = 1105520928110492191417703162650245113664610474875
    y = int('2d026f4bf30195ede3a088da85e398ef869611d0f68f0713d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b85519b1c23cc3ecdc6062650462e3063bd179c2a6581519f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d32971c3de5084cce04a2e147821', 16)

    k = (m1 - m2) * pow((s1 - s2) % q, -1, q) % q
    x = (pow(r, -1, q) * (k * s1 - m1)) % q
    print('Key: ', x)
    print('Public key check: ', pow(g, x, p) == y)
