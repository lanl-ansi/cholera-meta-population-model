
import numpy as np


def fill_cumsum(x, y, l):
    """
    For a given pair of times and values, creates a new pair where all
    the times from 0 to l, are given and values at new times are set to zero.
    :param x: set times (numpy.array)
    :param y: set of values (numpy.array)
    :param l: length of new set of times (int)
    :return: pair of times (now consecutive) and values (numpy.array, numpy.array)
    """
    z = np.zeros(l)
    z[x] = y
    x = np.arange(l)
    return x, z
