import random

def generator_uid():
    hashed = random.randint(100000, 999999)
    return hashed