import numpy as np


def gen_otp(size):
    rng = np.random.default_rng()
    return "".join([str(rng.integers(0, 10)) for _ in range(size)])
