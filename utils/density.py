from math import sin, pi


def hour_density(h, offset=0):
    return sin((float(h) + offset) / 24 * pi)



