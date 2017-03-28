
from random import uniform

def random_floats(low, high, size):
    return [uniform(low, high) for _ in range(size)]