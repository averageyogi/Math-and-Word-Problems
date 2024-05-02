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
    for i in range(1, (n // 2) + 1):
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


def find_duplicates(items: Iterable[T]) -> list[T]:
    """Find duplicate items in an iterable."""
    return [item for item, count in collections.Counter(items).items() if count > 1]


def aliquot_sequence(n: int, al_seq: list[int] = None, pbar: tqdm = None, seq_iteration_cutoff: int = 100):
    if al_seq is None:
        al_seq = []

    if not (len(al_seq) > 1 and len(find_duplicates(al_seq)) > 0):
        if n > 0 and len(al_seq) < seq_iteration_cutoff:
            pbar.update(1)
            al_sum = aliquot_sum(find_proper_divisors(n))

            al_seq.append(al_sum)
            aliquot_sequence(al_sum, al_seq=al_seq, pbar=pbar)

    return al_seq


def aliquot_sequence_sequences(n: int):
    with open("./aliquot_sequences/sequence_files/proper_divisor_lists.txt", "w", encoding="utf-8") as f:
        f.write("")
    with open("./aliquot_sequences/sequence_files/proper_divisors_length.txt", "w", encoding="utf-8") as f:
        f.write("")
    with open("./aliquot_sequences/sequence_files/aliquot_sums.txt", "w", encoding="utf-8") as f:
        f.write("")
    with open("./aliquot_sequences/sequence_files/aliquot_sequence.txt", "w", encoding="utf-8") as f:
        f.write("")
    with open("./aliquot_sequences/sequence_files/aliquot_sequence_length.txt", "w", encoding="utf-8") as f:
        f.write("")

    for i in tqdm(
        range(1, n+1),
        total=n,
        ascii=" ░▒█",
        ncols=100,
        # desc=library[0],
        # unit=library[1].type
    ):
        divisor_list = find_proper_divisors(i)
        al_sum = aliquot_sum(divisor_list)

        pbar = tqdm(leave=False)
        al_seq = aliquot_sequence(i, pbar=pbar)

        with open("./aliquot_sequences/sequence_files/proper_divisor_lists.txt", "a", encoding="utf-8") as f:
            f.write(f"{i}-{divisor_list}\n")
        with open("./aliquot_sequences/sequence_files/proper_divisors_length.txt", "a", encoding="utf-8") as f:
            f.write(f"{i}-{len(divisor_list)}\n")
        with open("./aliquot_sequences/sequence_files/aliquot_sums.txt", "a", encoding="utf-8") as f:
            f.write(f"{i}-{al_sum}\n")
        with open("./aliquot_sequences/sequence_files/aliquot_sequence.txt", "a", encoding="utf-8") as f:
            f.write(f"{i}-{al_seq}\n")
        with open("./aliquot_sequences/sequence_files/aliquot_sequence_length.txt", "a", encoding="utf-8") as f:
            f.write(f"{i}-{len(set(al_seq))}\n")


def main():
    input_val = 80

    # divisor_list = find_proper_divisors(input_val)
    # print(divisor_list)
    # alqt_sum = aliquot_sum(divisor_list)
    # print(alqt_sum)

    # seq = aliquot_sequence(input_val)
    # print(seq)
    # print('length of sequence:', len(seq))

    aliquot_sequence_sequences(200)

if __name__ == "__main__":
    main()
