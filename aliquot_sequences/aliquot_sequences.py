"""
https://www.youtube.com/watch?v=OtYKDzXwDEE
https://www.youtube.com/watch?v=Yh1QUYn2f3I&t=0s
https://en.wikipedia.org/wiki/Aliquot_sequence

Unsolved problem in mathematics:

Catalan-Dickson conjecture:
    Do all aliquot sequences eventually end with a prime number, a perfect number,
    or a set of amicable or sociable numbers?
"""

import numpy as np
import matplotlib.pyplot as plt


def find_proper_divisors(n: int) -> "list[int]":
    """A positive divisor of n that is different from n"""
    if n < 1:
        raise ValueError("Must be a positive integer.")

    return [1,2,4]
    raise NotImplementedError


def aliquot_sum(proper_divisors: "list[int]") -> int:
    """
    The sum of all proper divisors of n, that is, all divisors of n other than n itself.

    Args:
        divisors (list[int]): the list of proper divisors

    Returns:
        int: the sum of the proper divisors
    """
    return sum(proper_divisors)


def main():
    input_val = 8

    divisor_list = find_proper_divisors(input_val)
    alqt_sum = aliquot_sum(divisor_list)

    with open("./aliquot_sequences/proper_divisor_lists.txt", "a", encoding="utf-8") as f:
        f.write(f"{input_val}-{divisor_list}")
    with open("./aliquot_sequences/aliquot_sums.txt", "a", encoding="utf-8") as f:
        f.write(f"{input_val}-{alqt_sum}")


if __name__ == "__main__":
    main()
