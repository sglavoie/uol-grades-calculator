"""
Math helper functions.
"""
import math


def round_half_up(num: float, decimals=0):
    """Round a float up and return it."""
    multiplier = 10 ** decimals
    return math.floor(num * multiplier + 0.5) / multiplier
