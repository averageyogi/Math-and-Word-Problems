#!/usr/bin/env python
# coding: utf-8

"""
For N coins in a row, given number c, choose c coins (one at a time) going
from either end such that the total value is maximized
"""

from random import choices, randint

from numpy import argmax


N = 9  # number of coins
coin_values = [1, 5, 10, 25, 50, 100]  # American denomination in cents

coins = choices(coin_values, k=N)  # randomly assign row of coins
c = randint(2, N-1)  # number of coins to pick (1 and N are boring choices)
print(f"Coins: {coins}")
print(f"Choose {c} coins from the edges to maximize the value.")

################################################################################
# Solution
# The coins you should choose (not necessarily the order you
# need to choose them in when going from the edges).
################################################################################

# The possible coins to pick, going in at most 'c' from the edges
options = [coins[c-i] for i in range(1, (2 * c)+1)]

# The possible choices of picking 'c' coins
windows = [options[i:i+c] for i in range(c+1)]

selection = windows[argmax([sum(windows[i]) for i in range(len(windows))])]
print(f"Chosen coins (not necessarily the order chosen): {selection}")
