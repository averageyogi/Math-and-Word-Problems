"""
In mathematics, the factorial of a non-negative integer n, denoted by n!,
is the product of all positive integers less than or equal to n:
n! = n ⋅ (n-1) ⋅ (n-2) ⋅ (n-3) ⋅ ⋯ ⋅ 3 ⋅ 2 ⋅ 1

For example,
5! = 5 ⋅ 4 ⋅ 3 ⋅ 2 ⋅ 1 = 120

The value of 0! is 1, according to the convention for an empty product.
"""

import functools


# Lambda one-liner implementation for the factorial of n
# Can't handle zero case, 0!=1, or negative numbers
# Raises TypeError in both cases
f = lambda n: functools.reduce(int.__mul__, range(1, n + 1))


def factorial_recursive(n: int) -> int:
    """
    Recursive implementation for the factorial of n.

    Raises:
        ValueError: if n < 0.
    """
    if n < 0:
        raise ValueError("Input must be a positive integer or zero: n >= 0.")
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_iterative(n: int) -> int:
    """
    Iterative implementation for the factorial of n.

    Raises:
        ValueError: if n < 0.
    """
    if n < 0:
        raise ValueError("Input must be a positive integer or zero: n >= 0.")
    if n <= 1:
        return 1
    for i in range(n - 1, 0, -1):  # iterate backwards from n-1 to 1
        n *= i
    return n


if __name__ == "__main__":
    test1 = f(input1 := int(input("Input number: ")))
    print(f"{input1}! = {test1}")
    test2 = factorial_recursive(input2 := int(input("Input number: ")))
    print(f"{input2}! = {test2}")
    test3 = factorial_iterative(input3 := int(input("Input number: ")))
    print(f"{input3}! = {test3}")
