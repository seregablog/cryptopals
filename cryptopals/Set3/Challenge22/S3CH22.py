import time
import random


from Set3.Challenge21.S3CH21 import MersenneTwister


class MtTimeOracle:
    def __init__(self) -> None:
        self.rng = MersenneTwister()
        seed = int(time.time()) + random.randint(40, 1000)
        self.rng.seed(seed)

    def getRandom(self)->int:
        return self.rng.getRandomNumber()

if __name__ == "__main__":
    oracle = MtTimeOracle()
    output = oracle.getRandom()
    timestamp = int(time.time()) + 1001
    while timestamp > 0:
        rng = MersenneTwister()
        rng.seed(timestamp)
        number = rng.getRandomNumber()
        if  number == output:
            print('Seed=', timestamp)
            print('Numbers predict correct:',number == output)
            break
        timestamp -= 1


        


