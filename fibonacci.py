"""
In mathematics, the Fibonacci numbers, commonly denoted F_n, form a sequence,
called the Fibonacci sequence, such that each number is the sum of the two
preceding ones, starting from 0 and 1. That is,

F_0 = 0 , F_1 = 1 , and
F_n = F_n-1 + F_n-2 for n > 1.

The sequence starts:
0 , 1 , 1 , 2 , 3 , 5 , 8 , 13 , 21 , 34 , 55 , 89 , 144 , … 

fib(3) = fib(2)+fib(1) = (fib(1)+fib(0))+1 = (1+0)+1 = 2
fib(4) = fib(3)+fib(2) = (fib(2)+fib(1))+(fib(1)+fib(0))
       = ((fib(1)+fib(0))+1)+(1+0) = ((1+0)+1)+(1+0) = (1+1)+1 = 2+1 = 3
etc...

https://stackoverflow.com/questions/494594/how-to-write-the-fibonacci-sequence
https://stackoverflow.com/questions/37802129/fibonacci-in-python-recursively-into-a-list
"""

from statistics import mean
from time import perf_counter


# MARK: Recursive
def fibonacci_recursive(n: int) -> int:
    """
    Recursive implementation to generate F_n, the n-th Fibonacci number,
    beginning from from F_0

    Raises:
        ValueError: if n < 0.

    Return:
        int: the n-th Fibonacci number
    """
    if n < 0:
        raise ValueError("Input must be a positive integer or zero: n >= 0.")
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

    # # Exponentially faster than above by using list function, making list and one recursion instead of branching
    # if n < 2:
    #     return [0, 1][:n+1]

    # fib_list = fibonacci_recursive_list(n-1)
    # fib_list.append(sum(fib_list[-2:]))

    # return fib_list[-1]


# MARK: RecursiveList (w)
def fibonacci_recursive_list_wasteful(n: int) -> list[int]:
    """
    Recursive implementation to generate the Fibonacci sequence up to F_n,
    starting from F_0

    Wasteful as it just calls the regular function and does the full recursion
    for every value added to the list.

    Return:
        list[int]: list of the first n+1 Fibonacci numbers (sequence up to F_n)
    """
    return [fibonacci_recursive(i) for i in range(n + 1)]


# MARK: Recursive List
def fibonacci_recursive_list(n: int) -> list[int]:
    """
    Recursive implementation to generate the Fibonacci sequence upto F_n,
    starting from F_0

    Raises:
        ValueError: if n < 0.

    Return:
        list[int]: list of the first n+1 Fibonacci numbers (sequence up to F_n)
    """

    if n < 0:
        raise ValueError("Input must be a positive integer or zero: n >= 0.")
    if n < 2:
        return [0, 1][: n + 1]

    fib_list = fibonacci_recursive_list(n - 1)
    fib_list.append(sum(fib_list[-2:]))

    return fib_list


# MARK: Iterative
def fibonacci_iterative(n: int) -> int:
    """
    Iterative implementation to generate F_n, the n-th Fibonacci number,
    beginning from from F_0

    Raises:
        ValueError: if n < 0.

    Return:
        int: the n-th Fibonacci number
    """
    if n < 0:
        raise ValueError("Input must be a positive integer or zero: n >= 0.")
    if n == 0:
        return 0
    if n == 1:
        return 1

    n1, n2 = 0, 1
    for _ in range(n):
        next_val = n1 + n2

        n1 = n2
        n2 = next_val
    return n1


# MARK: Iterative List
def fibonacci_iterative_list(n: int) -> list[int]:
    """
    Iterative implementation to generate the Fibonacci sequence upto F_n,
    starting from F_0

    Raises:
        ValueError: if n < 0.

    Return:
        list[int]: list of the first n+1 Fibonacci numbers (sequence up to F_n)
    """
    if n < 0:
        raise ValueError("Input must be a positive integer or zero: n >= 0.")
    fib_list = [0]
    n1, n2 = 0, 1
    for _ in range(n):
        next_val = n1 + n2

        n1 = n2
        n2 = next_val
        fib_list.append(n1)
    return fib_list


# MARK: List Indexing
def fibonacci_list_indexing(n: int) -> list[int]:
    """
    Iterative list indexing implementation to generate the Fibonacci sequence up to F_n,
    starting from F_0

    Raises:
        ValueError: if n < 0.

    Return:
        list[int]: list of the first n+1 Fibonacci numbers (sequence up to F_n)
    """
    if n < 0:
        raise ValueError("Input must be a positive integer or zero: n >= 0.")
    if n == 0:
        return [0]

    fib_list = [0, 1]
    if n == 1:
        return fib_list

    # for i in range(2, n+1):
    #     fib_list.append(fib_list[i-1] + fib_list[i-2])
    while len(fib_list) < n + 1:
        fib_list.append(fib_list[-1] + fib_list[-2])

    return fib_list


# MARK: Generator Yield
def fibonacci_yield(n: int) -> list[int]:
    """
    Generator implementation to generate the Fibonacci sequence up to F_n,
    starting from F_0

    Raises:
        ValueError: if n < 0.

    Return:
        list[int]: list of the first n+1 Fibonacci numbers (sequence up to F_n)
    """
    if n < 0:
        raise ValueError("Input must be a positive integer or zero: n >= 0.")

    def fib():
        """
        Generator for the Fibonacci sequence.

        Yields:
            int: next value in Fibonacci sequence, starting at F_0
        """
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    fib_list = []
    for idx, x in enumerate(fib()):
        fib_list.append(x)
        if idx == n:
            break
    return fib_list


def benchmark(n: int = 40):
    """
    Time benchmarking for Fibonacci sequence functions.

    Args:
        n: index to generate Fibonacci sequence up to, F_n
    """
    fibonacci_recursive_times = []
    fibonacci_recursive_list_wasteful_times = []
    fibonacci_recursive_list_times = []
    fibonacci_iterative_times = []
    fibonacci_iterative_list_times = []
    fibonacci_list_indexing_times = []
    fibonacci_yield_times = []

    for _ in range(5):
        counter_start = perf_counter()
        fibonacci_recursive(n)
        fibonacci_recursive_times.append(perf_counter() - counter_start)

        counter_start = perf_counter()
        fibonacci_recursive_list_wasteful(n)
        fibonacci_recursive_list_wasteful_times.append(perf_counter() - counter_start)

        counter_start = perf_counter()
        fibonacci_recursive_list(n)
        fibonacci_recursive_list_times.append(perf_counter() - counter_start)

        counter_start = perf_counter()
        fibonacci_iterative(n)
        fibonacci_iterative_times.append(perf_counter() - counter_start)

        counter_start = perf_counter()
        fibonacci_iterative_list(n)
        fibonacci_iterative_list_times.append(perf_counter() - counter_start)

        counter_start = perf_counter()
        fibonacci_list_indexing(n)
        fibonacci_list_indexing_times.append(perf_counter() - counter_start)

        counter_start = perf_counter()
        fibonacci_yield(n)
        fibonacci_yield_times.append(perf_counter() - counter_start)

    print(f"fibonacci_recursive Average elapsed time: {mean(fibonacci_recursive_times)}")
    print(f"fibonacci_recursive_list_wasteful Average elapsed time: {mean(fibonacci_recursive_list_wasteful_times)}")
    print(f"fibonacci_recursive_list Average elapsed time: {mean(fibonacci_recursive_list_times)}")
    print(f"fibonacci_iterative Average elapsed time: {mean(fibonacci_iterative_times)}")
    print(f"fibonacci_iterative_list Average elapsed time: {mean(fibonacci_iterative_list_times)}")
    print(f"fibonacci_list_indexing Average elapsed time: {mean(fibonacci_list_indexing_times)}")
    print(f"fibonacci_yield Average elapsed time: {mean(fibonacci_yield_times)}")


if __name__ == "__main__":
    test1 = fibonacci_recursive(input1 := int(input("Input number: ")))
    print(f"Fibonacci number F_{input1} = {test1}")
    print(f'Fibonacci sequence: {fibonacci_recursive_list_wasteful(int(input("Input number: ")))}')
    print(f'Fibonacci sequence: {fibonacci_recursive_list(int(input("Input number: ")))}')
    test2 = fibonacci_iterative(input2 := int(input("Input number: ")))
    print(f"Fibonacci number F_{input2} = {test2}")
    print(f'Fibonacci sequence: {fibonacci_iterative_list(int(input("Input number: ")))}')
    print(f'Fibonacci sequence: {fibonacci_list_indexing(int(input("Input number: ")))}')
    print(f'Fibonacci sequence: {fibonacci_yield(int(input("Input number: ")))}')

    # benchmark(40)
