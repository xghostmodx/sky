import math
from functools import reduce

def kaos(*values):
    if len(values) == 0:
        return 0

    # Magnitude = product of absolute values
    magnitude = 1
    for v in values:
        magnitude *= abs(v)

    # Find largest absolute value(s)
    abs_vals = [abs(v) for v in values]
    max_val = max(abs_vals)

    # Check for tie among largest magnitudes
    max_count = abs_vals.count(max_val)

    if max_count > 1:
        # If tie exists (e.g., +5 and -5), annihilate
        return 0

    # Sign comes from the value with largest magnitude
    dominant_index = abs_vals.index(max_val)
    dominant_value = values[dominant_index]

    sign = 1 if dominant_value > 0 else -1

    return sign * magnitude