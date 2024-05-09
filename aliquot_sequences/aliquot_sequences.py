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
from matplotlib.animation import FuncAnimation, PillowWriter
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


def flatten(l: list[list[T]]) -> list[T]:
    """Flatten a list one dimension lower"""
    flat = []
    for item in l:
        if isinstance(item, list):
            # flat += item
            flat.extend(item)
        else:
            flat.append(item)
    return flat


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

    for i in tqdm(range(1, n+1), total=n, ascii=" ░▒█", ncols=100):
        divisor_list = find_proper_divisors(i)
        al_sum = aliquot_sum(divisor_list)

        pbar = tqdm(leave=False)
        al_seq = aliquot_sequence_recursive(i, pbar=pbar)
        al_seq = aliquot_sequence(i, allow_repetition=False, pbar=pbar)

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


def animate_sequences():
    fig, ax = plt.subplots()

    x = np.arange(0, 2*np.pi, 0.01)
    line, = ax.plot(x, np.sin(x))


    def animate(i):
        line.set_ydata(np.sin(x + i / 50))  # update the data.
        return line,


    ani = FuncAnimation(
        fig, animate, interval=20, blit=True, save_count=50)

    # To save the animation, use e.g.
    #
    # ani.save("movie.mp4")
    #
    # or
    #
    # writer = animation.FFMpegWriter(
    #     fps=15, metadata=dict(artist='Me'), bitrate=1800)
    # ani.save("movie.mp4", writer=writer)

    plt.show()


def open_sequence_files() -> tuple[list[list[int]], list[int], list[int], list[list[int]], list[int]]:
    with open("./aliquot_sequences/sequence_files/proper_divisor_lists.txt", "r", encoding="utf-8") as f:
        proper_divisor_lists_import = []
        for line in f:
            proper_divisor_lists_import.append(
                line.strip().replace("[","").replace("]","").split("-")[1:][0].split(",")
            )
        proper_divisor_lists = []
        for l in proper_divisor_lists_import:
            new_line = []
            for val in l:
                if val == "":
                    continue
                new_line.append(int(val))
            proper_divisor_lists.append(new_line)
    with open("./aliquot_sequences/sequence_files/proper_divisors_length.txt", "r", encoding="utf-8") as f:
        proper_divisors_length = []
        for line in f:
            proper_divisors_length.append(line.strip().replace("[","").replace("]","").split("-")[1:][0].split(","))
        proper_divisors_length = [int(val) for l in proper_divisors_length for val in l]
    with open("./aliquot_sequences/sequence_files/aliquot_sums.txt", "r", encoding="utf-8") as f:
        aliquot_sums = []
        for line in f:
            aliquot_sums.append(line.strip().replace("[","").replace("]","").split("-")[1:][0].split(","))
        aliquot_sums = [int(val) for l in aliquot_sums for val in l]
    with open("./aliquot_sequences/sequence_files/aliquot_sequence.txt", "r", encoding="utf-8") as f:
        aliquot_sequence_list_import = []
        for line in f:
            aliquot_sequence_list_import.append(
                line.strip().replace("[","").replace("]","").split("-")[1:][0].split(",")
            )
        aliquot_sequence_list = []
        for l in aliquot_sequence_list_import:
            new_line = []
            for val in l:
                if val == "":
                    continue
                new_line.append(int(val))
            aliquot_sequence_list.append(new_line)
    with open("./aliquot_sequences/sequence_files/aliquot_sequence_length.txt", "r", encoding="utf-8") as f:
        aliquot_sequence_length = []
        for line in f:
            aliquot_sequence_length.append(line.strip().replace("[","").replace("]","").split("-")[1:][0].split(","))
        aliquot_sequence_length = [int(val) for l in aliquot_sequence_length for val in l]

    return (
        proper_divisor_lists,
        proper_divisors_length,
        aliquot_sums,
        aliquot_sequence_list,
        aliquot_sequence_length,
    )


def plot_sequences(save: bool = False, show: bool = True) -> None:
    (
        proper_divisor_lists,
        proper_divisors_length,
        aliquot_sums,
        aliquot_sequence_list,
        aliquot_sequence_length,
    ) = open_sequence_files()

    # print(aliquot_sequence_length[:5])
    # print(aliquot_sequence_list[:5])
    # print(aliquot_sums[:5])
    # print(proper_divisor_lists[:5])
    # # print(proper_divisors_length[:5])

    plt.figure(figsize=(15,6))
    plt.plot(aliquot_sequence_length)
    plt.title("Length of Aliquot Sequence (early cutoff at Length=100)")
    plt.xlabel("n")
    plt.ylabel("Length")

    plt.figure(figsize=(15,6))
    plt.plot(aliquot_sums)
    plt.title("Aliquot Sum")
    plt.xlabel("n")
    plt.ylabel("Sum")

    plt.figure(figsize=(15,6))
    plt.plot(proper_divisors_length)
    plt.title("Number of Proper Divisors of n")
    plt.xlabel("n")
    plt.ylabel("Number of Proper Divisors")
    plt.ylabel("Sum")

    plt.figure(figsize=(15,6))
    plt.bar(x=range(len(proper_divisors_length)), height=proper_divisors_length)
    plt.title("Number of Proper Divisors of n")
    plt.xlabel("n")
    plt.ylabel("Number of Proper Divisors")

    aliquot_sequence_length_counter = collections.Counter(aliquot_sequence_length)
    plt.figure(figsize=(15,6))
    plt.bar(x=aliquot_sequence_length_counter.keys(), height=aliquot_sequence_length_counter.values())
    plt.title("Count of Aliquot Sequence Lengths, for sequences of n <= 500 (early cutoff at Length=100)")
    plt.xlabel("Length of Aliquot Sequence")
    plt.ylabel("Length")

    proper_divisors_length_counter = collections.Counter(proper_divisors_length)
    plt.figure(figsize=(15,6))
    plt.bar(x=proper_divisors_length_counter.keys(), height=proper_divisors_length_counter.values())
    plt.title("Count of Number of Proper Divisors of n, n <= 500")
    plt.xlabel("Number of Proper Divisors")
    plt.ylabel("Count")

    # number of occurrences of m in combined proper divisors of all n's approaches n/m as n approaches infinity
    proper_divisor_lists_counter = collections.Counter(flatten(proper_divisor_lists))
    plt.figure(figsize=(15,6))
    plt.bar(x=proper_divisor_lists_counter.keys(), height=proper_divisor_lists_counter.values())
    plt.title("Frequency of Proper Divisors of n, n <= 500")
    plt.xlabel("Proper Divisor")
    plt.ylabel("Count")

    if show:
        plt.show()


def main() -> None:
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

    # counter_start = perf_counter()
    # aliquot_sequence_sequences(500)
    # print(f"Elapsed time: {perf_counter() - counter_start}")

    #TODO plots of sequences, animate?
    # animate_sequences()

    plot_sequences()


if __name__ == "__main__":
    main()
