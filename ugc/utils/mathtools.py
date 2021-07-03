"""
Math helper functions.
"""
import math


def round_half_up(num: float, decimals: int = 0):
    """Round a float up and return it.

    Assumes 10 decimals is enough precision. Also assumes we won't be rounding
    anything beyond 1,000,000 as that's far outside the range of expected
    values and would lead to overflow errors in this implementation."""
    if decimals > 10 or decimals < 0:
        raise ValueError("Supporting up to 10 decimals of precision, no more!")
    if num > 1_000_000:
        raise ValueError("We don't round that high around here (max value: 1,000,000)")
    multiplier = 10 ** decimals
    return math.floor(num * multiplier + 0.5) / multiplier
