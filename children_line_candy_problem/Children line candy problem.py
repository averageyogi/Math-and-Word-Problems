#!/usr/bin/env python
# coding: utf-8

"""
There are N children in line. Each child is assigned a score.
Each child is given candy based on two rules:
    1. Each child must have at least one candy.
    2. Children with higher rating get more candies than their neighbors.

What are the minimum candies you must give?
"""
# Note:
#   1. It doesn't specify what neighbors means.
#   2. It doesn't explicitly say what happens with equal scores.
#      Because equal is neither higher nor lower, equal scored
#      neighbors could have the same or different number of candies.

from random import choices

import numpy as np


N = 6   # Number of children in line
S = 10  # Score out of

scores = choices(range(1, S+1), k=N)  # Randomly assign each child score 1-S
# print(scores)


################################################################################
# Solution assuming local nearest neighbor (the two on either side):
# Related to score and placement.
# Equal neighbors may get different number of candies
################################################################################

candies_forward = [1] * N  # Every child gets at least one candy
candies_backward = [1] * N

for i in range(1, len(scores)):
    # Check if score is higher than child in front/left
    if scores[i] > scores[i-1]:
        candies_forward[i] = candies_forward[i-1] + 1

    # Check if score is higher than child behind/right
    if scores[N-i - 1] > scores[N-i]:
        candies_backward[N-i - 1] = candies_backward[N-i] + 1

# Element-wise maximum
candies_final = [max(c_f, c_b) for c_f, c_b in zip(candies_forward, candies_backward)]
# candies_final = list(np.maximum(candies_forward,candies_backward)) # if you want to import numpy,
#                                                                    # list() is just for printing to match

print("Assuming local nearest neighbor (the two on either side):")
print("Scores: ", scores)
print("Candies:", candies_final)
print("Total candies:", sum(candies_final))


################################################################################
# Solution assuming entire line consists of "neighbors":
# Related only to score.
# Equal scores (regardless of position) get equal candies.
################################################################################

candies = [1] * N  # Every child gets at least one candy
score_sort_idx = np.argsort(scores)
score_sort = np.array(scores)[score_sort_idx]
count = 0

for idx in range(len(scores)):
    # Sort scores
    # If the score matches previous, num candies should be same, so add one less than count
    if (idx > 0) and (score_sort[idx] == score_sort[idx-1]):
        candies[score_sort_idx[idx]] += count - 1

    # If score isn't same as previous, add current count and increment count
    else:
        candies[score_sort_idx[idx]] += count
        count += 1

print('\nAssuming entire line consists of "neighbors":')
print("Scores: ", scores)
print("Candies:", candies)
print("Total candies:", sum(candies))
