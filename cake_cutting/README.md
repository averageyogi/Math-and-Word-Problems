# Cake Cutting Simulations

Simulate trials of cutting a cake with two candles. Record results of splitting the candle pair.

Original Numberphile videos that gave inspiration:

- [Two Candles, One Cake](https://www.youtube.com/watch?v=FkVe8qrT0LA),
- [Two Candles, One Cake (Part 2)](https://www.youtube.com/watch?v=l5gUrDg01cQ),
- [The Cake and Candles - Geogebra Build as used on Numberphile](https://www.youtube.com/watch?v=0eqBG6lz2mE)

## Long Cake

Candles split cake into 3 regions, slice chooses one of the regions.

P(slice between candles) = 1/3.

![long_cake](https://github.com/averageyogi/Math-and-Word-Problems/blob/main/cake_cutting/result_animations/long_cake.gif?raw=true)

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

![round_cake_cut_from_center_candleregion](https://github.com/averageyogi/Math-and-Word-Problems/blob/main/cake_cutting/result_animations/round_cake_cut_from_center_candleregion.gif?raw=true)

---
In the cut anywhere case, changing radius and center does seem to matter.

With fixed radius, all points are on a circle. Cut is 2 points on circle, those points can either be together between the candles (2 options (4 bi-directionally)), or have one candle in between each cut point (1 option (2 bi-directionally)).

P(cut points are each between candles) = 2/6 = 1/3.

![round_cake_cut_anywhere_fixedrad_candleregion](https://github.com/averageyogi/Math-and-Word-Problems/blob/main/cake_cutting/result_animations/round_cake_cut_anywhere_fixedrad_candleregion.gif?raw=true)

With random radius between 0-R, it appears to be around 0.38.

![round_cake_cut_anywhere_candleregion](https://github.com/averageyogi/Math-and-Word-Problems/blob/main/cake_cutting/result_animations/round_cake_cut_anywhere_candleregion.gif?raw=true)

---
From [Two Candles, One Cake (Part 2)](https://www.youtube.com/watch?v=l5gUrDg01cQ)

@steffahn 2 years ago (edited)\
5:08 So here are exact values for all 4 cases:\
random end points: 1/3 - 5/(4 π²) ≈ 0.206682\
random mid point: 1/8 + 2/(3 π²) ≈ 0.192547\
random radial point: 128/(45 π²) ≈ 0.288202\
random point random angle: 1/3 ≈ 0.333333

And as a bonus, here's a distribution of cuts that wasn't in the video:\
Take two random points inside of the cake and make a line through them.\
results in: 1/3 + 35/(72 π²) ≈ 0.382587

Exercise for the interested reader: Verify these results (or show where I might be wrong).
