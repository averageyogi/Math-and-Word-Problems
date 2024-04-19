def maximumWealth(accounts: list[list[int]]) -> int:
    """
    From list of accounts with multiple subvalues, find account with greatest wealth.

    Args:
        accounts (list[list[int]]): list of accounts

    Returns:
        int: max wealth value
    """
    max_wealth = 0
    for i in accounts:
        s = sum(i)
        max_wealth = max(max_wealth, s)

    return max_wealth


if __name__ == '__main__':
    mat = [[1,5],[7,3],[3,5,3,5]]

    print(maximumWealth(mat))
