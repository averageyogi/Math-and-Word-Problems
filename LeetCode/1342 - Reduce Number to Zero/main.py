class Solution:
    def numberOfSteps(self, num: int, steps: int = 0) -> int:
        """
        If odd, subtract 1. If even, divide by 2. Track the number of steps to get to zero.

        Args:
            num (int): starting number
            steps (int, optional): Recursive record of the number of steps taken. Defaults to 0.

        Returns:
            int: number of steps
        """
        # Iterative
        steps = 0
        while num > 0:
            if num % 2 == 0:
                num /= 2
                steps += 1
            else:
                num -= 1
                steps += 1
        return steps

        # # Recursive
        # if num == 0:
        #     return steps
        # if num % 2 == 0:
        #     return Solution.numberOfSteps(self, num/2, steps+1)
        # return Solution.numberOfSteps(self, num-1, steps+1)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matplotlib.axes import Axes
    import numpy as np

    sol = Solution()
    # n = int(input('Enter number: '))
    # num_steps = sol.numberOfSteps(n)
    # print(num_steps)

    n_range = 100
    plot_arr = np.vectorize(sol.numberOfSteps)(np.arange(n_range))
    values, counts = np.unique(plot_arr, return_counts=True)
    # print(plot_arr)

    fig = plt.figure(figsize=(15, 7))
    fig.suptitle("If odd, subtract 1. If even, divide by 2.\nTrack the number of steps to get to zero.", fontsize=20)
    ax1, ax2 = fig.subplots(ncols=2)

    ax1: Axes
    ax1.plot(plot_arr)
    ax1.set_xlabel("n")
    ax1.set_ylabel("number of steps")
    ax1.legend(["number of steps"])

    ax2: Axes
    ax2.bar(values, counts)
    ax2.set_xlabel("number of steps")
    ax2.set_ylabel(f"count of first {n_range:,} n")
    ax2.set_xticks(np.arange(0, max(values), 5))
    ax2.legend(["counts"])

    plt.show()
