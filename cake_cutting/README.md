# Cake Cutting Simulations

Simulate trials of cutting a cake with two candles. Record results of splitting the candle pair.

## Long Cake

Candles split cake into 3 regions, slice chooses one of the regions.

P(slice between candles) = 1/3.

![alt text](.\result_animations\long_cake.gif "Title")

## Round Cake

Simulate trials of cutting a circular cake with two candles. Record results of splitting the candle pair.

There are three cases:

- cutting through the center of the cake
- cutting anywhere, with a fixed radius for all points
- cutting anywhere, with a random position for all points

---
In the simple case going through the center, changing radius doesn't matter.
One point is fixed, and the other point is on the same line no matter the distance away.
It only matters when displaying the results.

Slice splits cake in half:

P(one candle is on each half) = 2/4 = 1/2.

![alt text](.\result_animations\round_cake_cut_from_center_candleregion.gif "Title")

---
In the cut anywhere case, changing radius and center does seem to matter.

With fixed radius, all points are on a circle. Cut is 2 points on circle, those points can either be together between the candles (2 options (4 bi-directionally)), or have one candle in between each cut point (1 option (2 bi-directionally)).

P(cut points are each between candles) = 2/6 = 1/3.

![alt text](.\result_animations\round_cake_cut_anywhere_fixedrad_candleregion.gif "Title")

With random radius between 0-R, it appears to be around 0.38.

![alt text](.\result_animations\round_cake_cut_anywhere_candleregion.gif "Title")
