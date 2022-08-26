import numpy as np
import random

class Wrapper:
    def __init__(self, x, y) -> None:
        self.position = np.array([x, y])
        self.rand = random.random()
        self.__array_interface__ = self.position.__array_interface__

if __name__ == "__main__":
    a = np.array([np.array(Wrapper(x, x+10)) for x in range(10)])
    print(a)
    print(a[0].rand)
