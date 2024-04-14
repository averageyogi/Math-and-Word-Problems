import os
from functools import partial
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np


rng = np.random.default_rng(seed=None)
sim_length = 10000
save_animation = False

print("The probability a slice will separate the two candles:")

#####################################################################
## Simple simulation
#####################################################################
c1 = rng.random(sim_length)  # Equivalent to rng.uniform(0, 1, sim_length)
c2 = rng.random(sim_length)
cut = rng.random(sim_length)

count = 0
for i in range(sim_length):
    if ((c1[i] < cut[i]) and (cut[i] < c2[i])) or ((c2[i] < cut[i]) and (cut[i] < c1[i])):
        count += 1
print("Successful slice rate: ", count / sim_length)


#####################################################################
## For animation plot
#####################################################################
sim = np.zeros(
    sim_length,
    dtype=[
        ("candle1", float),
        ("candle2", float),
        ("cut", float),
        ("success", bool)
    ]
)

# High/low range is to fit within the animation display
sim["candle1"] = rng.uniform(0.1, 0.9, sim_length)
sim["candle2"] = rng.uniform(0.1, 0.9, sim_length)
sim["cut"] = rng.uniform(0.1, 0.9, sim_length)
sim["success"] = (
    (sim["candle1"] < sim["cut"]) & (sim["cut"] < sim["candle2"])
    | (sim["candle2"] < sim["cut"]) & (sim["cut"] < sim["candle1"])
)
# print('Successful slice rate: ', np.average(sim['success']))


## Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])

## Background "boundaries"
rect = patches.Rectangle((0.1, 0.25), 0.8, 0.35, linewidth=1, edgecolor="k", facecolor="none")
ax.add_patch(rect)

## Sim values
candle1_plot = ax.plot(sim["candle1"][0], 0.45, "b.", markersize=20)[0]
candle2_plot = ax.plot(sim["candle2"][0], 0.45, "g.", markersize=20)[0]
cut_plot = ax.plot([], [], linewidth=3, color="k")[0]

## Text
ax.text(0.05, 0.9, "Probability slice will separate the two candles", fontsize=20)
trial_num = ax.text(0.05, 0.8, "", fontsize=18)
success_rate = ax.text(0.5, 0.8, "", fontsize=20)


def update(frame_number, simulation, plot_candle1, plot_candle2, plot_cut, trial_num_text, success_rate_text):
    """Update animation frame with new data from simulation."""
    plot_candle1.set_data([simulation["candle1"][frame_number]], [0.45])
    plot_candle2.set_data([simulation["candle2"][frame_number]], [0.45])
    plot_cut.set_data([simulation["cut"][frame_number], simulation["cut"][frame_number]], [0.2, 0.65])
    if simulation["success"][frame_number]:
        plot_cut.set_color("r")
    else:
        plot_cut.set_color("k")

    trial_num_text.set_text(f"Trial: {frame_number}/{sim_length}")
    if frame_number != 0:
        success_rate_text.set_text(f"Success rate: {simulation['success'][:frame_number].mean() * 100:0.2f}%")


## Construct the animation, using the update function as the animation director.
animation = FuncAnimation(
    fig,
    func=partial(
        update,
        simulation=sim,
        plot_candle1=candle1_plot,
        plot_candle2=candle2_plot,
        plot_cut=cut_plot,
        trial_num_text=trial_num,
        success_rate_text=success_rate,
    ),
    frames=sim_length,
    interval=100,
    repeat=False,
)
if save_animation:
    animation.save(Path(os.getcwd()).joinpath("long cake.gif"), writer=PillowWriter(fps=10))

plt.show()
plt.close("all")
