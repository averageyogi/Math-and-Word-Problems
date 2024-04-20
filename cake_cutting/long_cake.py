import os
from functools import partial
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import patches, lines, text
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import numpy.typing as npt


RECT_SIZE: "tuple[float, float]" = (0.8, 0.35)
RECT_POSITION: "tuple[float, float]" = (0.1, 0.25)
SUCCESS_COLOR: str = "darkorange"
FAILURE_COLOR: str = "k"


def simple_simulation(rng: np.random.Generator, sim_length: int) -> None:
    """
    Simulate trials of cutting a rectangular cake with two candles. Record results of splitting the candle pair.

    Candles split cake into 3 regions, slice chooses one of the regions. P(slice between candles) = 1/3.

    Args:
        rng (np.random.Generator): random number generator
        sim_length (int): length of simulation, number of trials
    """
    c1 = rng.random(sim_length)  # Equivalent to rng.uniform(0, 1, sim_length)
    c2 = rng.random(sim_length)
    cut = rng.random(sim_length)

    count = 0
    for i in range(sim_length):
        # Is cut between candles?
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
    sim_length: int,
) -> list:
    """Update animation frame with new data from simulation."""
    plot_candle1.set_data([simulation["candle1"][frame_number]], [RECT_POSITION[1] + (RECT_SIZE[1] / 2)])
    plot_candle2.set_data([simulation["candle2"][frame_number]], [RECT_POSITION[1] + (RECT_SIZE[1] / 2)])
    plot_cut.set_data(
        [simulation["cut"][frame_number], simulation["cut"][frame_number]],
        [RECT_POSITION[1] - 0.05, RECT_POSITION[1] + RECT_SIZE[1] + 0.05]
    )
    if simulation["success"][frame_number]:
        plot_cut.set_color(SUCCESS_COLOR)
    else:
        plot_cut.set_color(FAILURE_COLOR)

    trial_num_text.set_text(f"Trial: {frame_number+1}/{sim_length}")
    if frame_number != 0:
        success_rate_text.set_text(f"Success rate: {simulation['success'][:frame_number].mean() * 100:0.2f}%")

    return [plot_candle1, plot_candle2, plot_cut, trial_num_text, success_rate_text]


def simulation_animation(
    rng: np.random.Generator,
    sim_length: int,
    show_candle_region: bool = False,
    save_animation: bool = False,
    save_filename: Path = Path(os.getcwd()).joinpath("long_cake.gif"),
) -> None:
    """
    Animate plots of simulation results, giving updated results as trials complete.

    Args:
        rng (np.random.Generator): random number generator
        sim_length (int): length of simulation, number of trials
        show_candle_region (bool, optional): Display region where candles are placed. Defaults to False.
        save_animation (bool, optional): Save animation to file as GIF. Defaults to False.
        save_filename (Path, optional): Path to save animation.
            Defaults to Path(os.getcwd()).joinpath("long cake.gif").
    """
    sim = np.zeros(
        sim_length,
        dtype=[
            ("candle1", float),
            ("candle2", float),
            ("cut", float),
            ("success", bool),
        ]
    )

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

    ## Text
    ax.text(0.05, 0.9, "Probability slice will separate the two candles", fontsize=20)
    trial_num = ax.text(0.1, 0.8, "Trial:", fontsize=18)
    success_rate = ax.text(0.5, 0.8, "Success rate:", fontsize=20)

    ## Background "boundaries"
    # Cake outline
    ax.add_patch(
        patches.Rectangle(RECT_POSITION, RECT_SIZE[0], RECT_SIZE[1], linewidth=1, edgecolor="k", facecolor="none")
    )
    # Candle placement path
    candle_region_legend = patches.Patch(fill=False, edgecolor="w", label=None)
    if show_candle_region:
        ax.add_patch(
            patches.Rectangle(
                (RECT_POSITION[0], RECT_POSITION[1] + (RECT_SIZE[1] / 2)),  # (x, y)
                RECT_SIZE[0], 0,  # w, h
                linewidth=20,
                edgecolor="b",
                facecolor="none",
                alpha=0.25,
            )
        )
        candle_region_legend = patches.Patch(edgecolor="b", linewidth=9, alpha=0.25, fill=False, label="Candle region")


    ## Sim values
    candle1_plot = ax.plot(sim["candle1"][0], RECT_POSITION[1] + (RECT_SIZE[1] / 2), "b.", markersize=20)[0]
    candle2_plot = ax.plot(sim["candle2"][0], RECT_POSITION[1] + (RECT_SIZE[1] / 2), "g.", markersize=20)[0]
    cut_plot = ax.plot(
        [sim["cut"][0], sim["cut"][0]],
        [RECT_POSITION[1] - 0.05, RECT_POSITION[1] + RECT_SIZE[1] + 0.05],
        linewidth=3,
        color=SUCCESS_COLOR if sim["success"][0] else FAILURE_COLOR,
    )[0]

    success_legend = lines.Line2D([], [], color=SUCCESS_COLOR, linewidth=3, label="Success")
    failure_legend = lines.Line2D([], [], color=FAILURE_COLOR, linewidth=3, label="Failure")
    ax.legend(
        handles=[success_legend, failure_legend, candle_region_legend],
        loc="lower right",
        fontsize=12,
        frameon=False,
        borderpad=0.8,
    )

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
            sim_length=sim_length,
        ),
        frames=sim_length,
        interval=100,
        repeat=False,
        blit=True,
    )
    if save_animation:
        animation.save(save_filename, writer=PillowWriter(fps=10))

    plt.show()
    plt.close("all")


if __name__ == "__main__":
    rng_main = np.random.default_rng(seed=None)
    sim_length_main = 500
    save_animation_main = False

    print("The probability a slice will separate the two candles:")
    print(f"Simulation: {sim_length_main} trials.")

    simple_simulation(rng_main, sim_length_main)
    simulation_animation(
        rng_main,
        sim_length_main,
        show_candle_region=True,
        save_animation=save_animation_main,
        save_filename=Path("./cake_cutting/result_animations/long_cake.gif"),
    )
