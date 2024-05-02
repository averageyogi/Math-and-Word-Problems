"""
https://www.youtube.com/watch?v=OtYKDzXwDEE
https://www.youtube.com/watch?v=Yh1QUYn2f3I&t=0s
https://en.wikipedia.org/wiki/Aliquot_sequence

Unsolved problem in mathematics:

Catalan-Dickson conjecture:
    Do all aliquot sequences eventually end with a prime number, a perfect number,
    or a set of amicable or sociable numbers?
"""

import collections
from math import sqrt
from time import perf_counter
from typing import Iterable, TypeVar

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

T = TypeVar("T")

def find_proper_divisors(n: int) -> "list[int]":
    """A positive divisor of n that is different from n"""
    if n < 1:
        raise ValueError("Must be a positive integer.")

    proper_divisors = []
    if n == 1:
        return proper_divisors  # 1 doesn't have any proper divisors, because it is it's only divisor
    for i in range(1, int(sqrt(n)) + 1):
        if n % i == 0:
            proper_divisors.append(i)
            if i > 1:
                proper_divisors.append(n // i)

    return sorted(set(proper_divisors))


def aliquot_sum(proper_divisors: "list[int]") -> int:
    """
    The sum of all proper divisors of n, that is, all divisors of n other than n itself.

    Args:
        divisors (list[int]): the list of proper divisors

    Returns:
        int: the sum of the proper divisors
    """
    return sum(proper_divisors)


def find_duplicates(items: Iterable[T]) -> "list[T]":
    """Find duplicate items in an iterable."""
    return [item for item, count in collections.Counter(items).items() if count > 1]


def aliquot_sequence_recursive(n: int, al_seq: "list[int]" = None, pbar: tqdm = None, seq_iteration_cutoff: int = 100):
    """Recursive implementation to create aliquot sequence"""
    if al_seq is None:
        al_seq = []

    if not (len(al_seq) > 1 and len(find_duplicates(al_seq)) > 0):
        if n > 0 and len(al_seq) < seq_iteration_cutoff:
            pbar.update(1)
            al_sum = aliquot_sum(find_proper_divisors(n))

            al_seq.append(al_sum)
            aliquot_sequence_recursive(al_sum, al_seq=al_seq, pbar=pbar)

    return al_seq


def aliquot_sequence(
    n: int, seq_iteration_cutoff: int = 100, allow_repetition: bool = False, pbar: tqdm = None
) -> "list[int]":
    """
    A sequence of positive integers in which each term is the sum of the proper divisors of the previous term.

    Resulting sequence does not include initializing value n, and for terminating values, will stop at 0.

    Args:
        n (int): initializing value of the sequence
        seq_iteration_cutoff (int, optional): An iteration bound for sequences. For some n, the length of the
            aliquot sequence is currently unknown. Defaults to 100.
        allow_repetition (bool, optional): Allow sequence to run (until seq_iteration_cutoff) to show repeated values.
            Defaults to False.
        pbar (tqdm, optional): tqdm progress bar. Defaults to None.

    Returns:
        list[int]: aliquot sequence for n

    Examples:
    >>> aliquot_sequence(12)
    [16, 15, 9, 4, 3, 1, 0]

    Repeating sequences will terminate before the first repetition, ie before the first repeated value would be re-added
    >>> aliquot_sequence(6)
    [6]
    >>> aliquot_sequence(220)
    [284, 220]
    """
    al_seq = []
    # Sequence is unknown length for some n, set an iteration bound
    while (n > 0) and (len(al_seq) < seq_iteration_cutoff):
        if pbar is not None:
            pbar.update(1)

        #TODO check text file for existing divisors list, else generate them, and save to list?
        n = aliquot_sum(find_proper_divisors(n))
        # If new aliquot sum is already in the sequence, then sequence will loop, if not allowing repetition
        if not allow_repetition and n in set(al_seq):
            break

        al_seq.append(n)

    return al_seq


def aliquot_sequence_sequences(n: int):
    # with open("./aliquot_sequences/sequence_files/proper_divisor_lists.txt", "w", encoding="utf-8") as f:
    #     f.write("")
    # with open("./aliquot_sequences/sequence_files/proper_divisors_length.txt", "w", encoding="utf-8") as f:
    #     f.write("")
    # with open("./aliquot_sequences/sequence_files/aliquot_sums.txt", "w", encoding="utf-8") as f:
    #     f.write("")
    with open("./aliquot_sequences/sequence_files/aliquot_sequence.txt", "w", encoding="utf-8") as f:
        f.write("")
    with open("./aliquot_sequences/sequence_files/aliquot_sequence_length.txt", "w", encoding="utf-8") as f:
        f.write("")

    for i in tqdm(range(1, n+1), total=n, ascii=" ░▒█", ncols=100):
        # divisor_list = find_proper_divisors(i)
        # al_sum = aliquot_sum(divisor_list)

        pbar = tqdm(leave=False)
        # al_seq = aliquot_sequence_recursive(i, pbar=pbar)
        al_seq = aliquot_sequence(i, allow_repetition=False, pbar=pbar)

        # with open("./aliquot_sequences/sequence_files/proper_divisor_lists.txt", "a", encoding="utf-8") as f:
        #     f.write(f"{i}-{divisor_list}\n")
        # with open("./aliquot_sequences/sequence_files/proper_divisors_length.txt", "a", encoding="utf-8") as f:
        #     f.write(f"{i}-{len(divisor_list)}\n")
        # with open("./aliquot_sequences/sequence_files/aliquot_sums.txt", "a", encoding="utf-8") as f:
        #     f.write(f"{i}-{al_sum}\n")
        with open("./aliquot_sequences/sequence_files/aliquot_sequence.txt", "a", encoding="utf-8") as f:
            f.write(f"{i}-{al_seq}\n")
        with open("./aliquot_sequences/sequence_files/aliquot_sequence_length.txt", "a", encoding="utf-8") as f:
            f.write(f"{i}-{len(set(al_seq))}\n")


def main():
    """Run main script logic."""
    # input_val = 138

    # divisor_list = find_proper_divisors(input_val)
    # print(divisor_list)
    # al_sum = aliquot_sum(divisor_list)
    # print(al_sum)

    # pbar = tqdm(unit=" step", leave=True)
    # seq = aliquot_sequence(input_val, allow_repetition=False, pbar=pbar)
    # print("\nn =", input_val)
    # print(seq)
    # print('length of sequence:', len(seq))

    counter_start = perf_counter()
    aliquot_sequence_sequences(10000000)
    print(f"Elapsed time: {perf_counter() - counter_start}")

    #TODO plots of sequences, animate?


if __name__ == "__main__":
    main()
