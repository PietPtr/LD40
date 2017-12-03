import random

def randint_seeded(seed, low, high):
    random.seed(seed + 10)
    return random.randint(int(low), int(high))
