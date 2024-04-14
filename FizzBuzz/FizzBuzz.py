"""
If divisible by 3, print Fizz.
If divisible by 5, print Buzz.
If divisible by both, print FizzBuzz.
Else, print the number.
"""

from time import perf_counter
from typing import Optional, Sequence, Union


def fizzbuzz(N: int = 100) -> None:
    """Basic fizzbuzz"""
    for i in range(1, N+1):
        output = ""
        if i % 3 == 0:
            output += "fizz"
        if i % 5 == 0:
            output += "buzz"

        print(output or i)  # in Python, empty is false (ie None, "", (,), [] or {})


def regular_long(N: int = 100, keywords: Optional[dict[int, str]] = None) -> None:
    """
    Print numbers 1-N, replacing multiples of given values with specified words.

    Args:
        N (int, optional): end value of list, last number
        keywords (dict[int, str], optional): the divisor to replace multiples of and words to replace them with
    """
    if keywords is None:
        keywords = {
            3: "Fizz",
            5: "Buzz",
        }

    for i in range(1, N+1):
        # # Stored bool, extra checks, but no stored string
        # n = True  # Print number
        # for divisor, word in keywords.items():
        #     if (i % divisor) == 0:
        #         print(word, end="")
        #         n = False  # Don't print number if printing word
        # # If not printing word, print number and return line else just return line
        # print(i) if n else print()

        # Stored string
        output = ""
        for divisor, word in keywords.items():
            if (i % divisor) == 0:
                output += word
        print(output or i)  # In Python, empty is false (ie None, "", (), [] or {})


def golfed_limited(N:int=100,a:Optional[Sequence[Union[int,str]]]=None)->None:
    """
    N (int): number to go to
    a (List): list of value/word lists
        i.e. [ [3, "fizz"] , [5, "buzz"] ]
    """
    if a is None:  # not "golf minimized"
        a=[[3,"fizz"],[5,"buzz"]]
    for n in range(1,N+1):print("".join(j*(n%i<1)for i,j in a)or n)


golfed_infinite = lambda a,n=1: print("".join(j*(n%i<1)for i,j in a)or n)+golfed_infinite(a,n+1)


if __name__ == "__main__":
    start_time = perf_counter()

    # fizzbuzz()
    regular_long(keywords={4: "Fazz", 5: "Buzz"})
    # golfed_limited(1000, [[4, "Foo"], [7, "Bar"], [9, "Baz"]])
    # golfed_infinite([[4, "Foo"], [7, "Bar"], [9, "Baz"]])

    print(f"\nElapsed Time: {perf_counter()-start_time:0.8f} seconds")
