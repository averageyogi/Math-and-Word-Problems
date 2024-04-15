import os
from functools import partial
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import patches, lines, text
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import numpy.typing as npt


RECT_SIZE = (0.8, 0.35)
RECT_POSITION = (0.1, 0.25)

def simple_simulation(rng: np.random.Generator, sim_length: int):
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
    print(f"Successful slice rate: {count / sim_length}")


def animation_update(
    frame_number,
    simulation: npt.ArrayLike,
    plot_candle1: lines.Line2D,
    plot_candle2: lines.Line2D,
    plot_cut: lines.Line2D,
    trial_num_text: text.Text,
    success_rate_text: text.Text,
    sim_length: int
):
    """Update animation frame with new data from simulation."""
    plot_candle1.set_data([simulation["candle1"][frame_number]], [RECT_POSITION[1] + (RECT_SIZE[1] / 2)])
    plot_candle2.set_data([simulation["candle2"][frame_number]], [RECT_POSITION[1] + (RECT_SIZE[1] / 2)])
    plot_cut.set_data(
        [simulation["cut"][frame_number], simulation["cut"][frame_number]],
        [RECT_POSITION[1] - 0.05, RECT_POSITION[1] + RECT_SIZE[1] + 0.05]
    )
    if simulation["success"][frame_number]:
        plot_cut.set_color("r")
    else:
        plot_cut.set_color("k")

    trial_num_text.set_text(f"Trial: {frame_number}/{sim_length}")
    if frame_number != 0:
        success_rate_text.set_text(f"Success rate: {simulation['success'][:frame_number].mean() * 100:0.2f}%")


def simulation_animation(rng: np.random.Generator, sim_length: int, save_animation: bool = False):
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
    sim["candle1"] = rng.uniform(RECT_POSITION[0], RECT_POSITION[0] + RECT_SIZE[0], sim_length)
    sim["candle2"] = rng.uniform(RECT_POSITION[0], RECT_POSITION[0] + RECT_SIZE[0], sim_length)
    sim["cut"] = rng.uniform(RECT_POSITION[0], RECT_POSITION[0] + RECT_SIZE[0], sim_length)
    sim["success"] = (
        (sim["candle1"] < sim["cut"]) & (sim["cut"] < sim["candle2"])
        | (sim["candle2"] < sim["cut"]) & (sim["cut"] < sim["candle1"])
    )
    print(f'Successful slice rate: {np.average(sim["success"])}')


    ## Create new Figure and an Axes which fills it.
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_axes([0, 0, 1, 1], frameon=False)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    ## Background "boundaries"
    rect = patches.Rectangle(RECT_POSITION, RECT_SIZE[0], RECT_SIZE[1], linewidth=1, edgecolor="k", facecolor="none")
    ax.add_patch(rect)
    ax.add_patch(patches.Rectangle(
        (RECT_POSITION[0], RECT_POSITION[1] + (RECT_SIZE[1] / 2)),
        RECT_SIZE[0], 0,
        linewidth=20, edgecolor="b", facecolor="none", alpha=0.25
    ))

    ## Sim values
    candle1_plot = ax.plot(sim["candle1"][0], RECT_POSITION[1] + (RECT_SIZE[1] / 2), "b.", markersize=20)[0]
    candle2_plot = ax.plot(sim["candle2"][0], RECT_POSITION[1] + (RECT_SIZE[1] / 2), "g.", markersize=20)[0]
    cut_plot = ax.plot([], [], linewidth=3, color="k")[0]

    ## Text
    ax.text(0.05, 0.9, "Probability slice will separate the two candles", fontsize=20)
    trial_num = ax.text(0.05, 0.8, "", fontsize=18)
    success_rate = ax.text(0.5, 0.8, "", fontsize=20)

    ## Construct the animation, using the update function as the animation director.
    animation = FuncAnimation(
        fig,
        func=partial(
            animation_update,
            simulation=sim,
            plot_candle1=candle1_plot,
            plot_candle2=candle2_plot,
            plot_cut=cut_plot,
            trial_num_text=trial_num,
            success_rate_text=success_rate,
            sim_length=sim_length
        ),
        frames=sim_length,
        interval=100,
        repeat=False,
    )
    if save_animation:
        animation.save(Path(os.getcwd()).joinpath("long cake.gif"), writer=PillowWriter(fps=10))

    plt.show()
    plt.close("all")

if __name__ == "__main__":
    rng = np.random.default_rng(seed=None)
    sim_length = 10000
    save_animation = False

    print("The probability a slice will separate the two candles:")

    simple_simulation(rng, sim_length)
    simulation_animation(rng, sim_length, save_animation)
