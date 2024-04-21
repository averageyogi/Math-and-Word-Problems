import os
from functools import partial
from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
from matplotlib import patches, lines, text
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import numpy.typing as npt

import shapely
import shapely.affinity
from shapely.geometry import LineString as sLineString
from shapely.geometry import Point as sPoint

from axline import axline


R: float = 1
CENTER: "tuple[float, float]" = (-0.1, -0.35)
CUT_DISPLAY_R: float = 0.42
SUCCESS_COLOR: str = "darkorange"
FAILURE_COLOR: str = "k"


def find_quadrant_rect(x: float, y: float) -> Literal[1, 2, 3, 4]:
    """Return Cartesian quadrant number for given x, y coordinates. 0 is positive."""
    x = x - CENTER[0]
    y = y - CENTER[1]

    if x >= 0 and y >= 0:
        return 1
    if x < 0 and y >= 0:
        return 2
    if x < 0 and y < 0:
        return 3
    return 4  # x >= 0 and y < 0


def simple_simulation(rng: np.random.Generator, sim_length: int) -> None:
    """
    Simulate trials of cutting a circular cake with two candles. Record results of splitting the candle pair.

    There are three cases:
    - cutting through the center of the cake
    - cutting anywhere, with a fixed radius for all points
    - cutting anywhere, with a random position for all points

    In the simple case going through the center, changing radius doesn't matter.
    One point is fixed, and the other point is on the same line no matter the distance away.
    It only matters when displaying the results.

    Slice splits cake in half, P(one candle is on each half) = 2/4 = 1/2.

    In the cut anywhere case, changing radius and center does seem to matter.
    With fixed radius, all points are on a circle. Cut is 2 points on circle,
    those points can either be together between the candles (2 options (4 bi-directionally)),
    or have one candle in between each cut point (1 option (2 bi-directionally)).
    P(cut points are each between candles) = 2/6 = 1/3.

    With random radius between 0-R, it appears to be around 0.38.

    Args:
        rng (np.random.Generator): random number generator
        sim_length (int): length of simulation, number of trials
    """
    #####################################################################
    ## Simple simulation, cut through the center
    #####################################################################
    ## Angle/position around the cake candles will be placed at
    theta = rng.uniform(0, 2 * np.pi, (sim_length, 5))
    ## Random radius from center that candles will be placed at
    radius = R
    # radius = rng.uniform(0, R, (sim_length, 4)) ** 0.5

    x = radius * np.cos(theta[:, 0:4])  # + CENTER[0]
    y = radius * np.sin(theta[:, 0:4])  # + CENTER[1]

    c1 = np.array([x[:, 0], y[:, 0]]).transpose()
    c2 = np.array([x[:, 1], y[:, 1]]).transpose()
    cut = np.array([x[:, 2], y[:, 2]]).transpose()  # cut always goes through center and point (x2, y2)

    # side_of_cut_c1 = np.sign(np.cross(np.subtract(cut[:,:2], CENTER), np.subtract(c1, CENTER)))
    # side_of_cut_c2 = np.sign(np.cross(np.subtract(cut[:,:2], CENTER), np.subtract(c2, CENTER)))
    side_of_cut_c1 = np.sign(np.cross(cut[:, :2], c1))
    side_of_cut_c2 = np.sign(np.cross(cut[:, :2], c2))

    count = 0
    for candle1_side, candle2_side in zip(side_of_cut_c1, side_of_cut_c2):
        if candle1_side != candle2_side:
            count += 1
    print(f"Successful slice rate (cut through center): {count / sim_length}")

    #####################################################################
    ## Simple simulation, cut anywhere
    #####################################################################
    ## Angle/position around the cake candles will be placed at
    theta = rng.uniform(0, 2 * np.pi, (sim_length, 5))
    ## Fixed or random radius from center that candles will be placed at
    for idx, radius in enumerate([R, rng.uniform(0, R, (sim_length, 4)) ** 0.5]):
        x = radius * np.cos(theta[:, 0:4])
        y = radius * np.sin(theta[:, 0:4])

        c1 = np.array([x[:, 0], y[:, 0]]).transpose()
        c2 = np.array([x[:, 1], y[:, 1]]).transpose()
        # Cut anywhere, through point (x2, y2) and (x3, y3)
        cut = np.array([x[:, 2], y[:, 2], x[:, 3], y[:, 3]]).transpose()

        side_of_cut_c1 = np.sign(np.cross(np.subtract(cut[:, :2], cut[:, 2:]), np.subtract(c1, cut[:, 2:])))
        side_of_cut_c2 = np.sign(np.cross(np.subtract(cut[:, :2], cut[:, 2:]), np.subtract(c2, cut[:, 2:])))

        count = 0
        for candle1_side, candle2_side in zip(side_of_cut_c1, side_of_cut_c2):
            if candle1_side != candle2_side:
                count += 1
        if idx == 0:
            print(f"Successful slice rate (cut anywhere, fixed radius): {count / sim_length}")
        else:
            print(f"Successful slice rate (cut anywhere, random position for all points): {count / sim_length}")


def animation_update(
    frame_number,
    simulation: npt.ArrayLike,
    plot_candle1: lines.Line2D,
    plot_candle2: lines.Line2D,
    plot_cut: lines.Line2D,
    trial_num_text: text.Text,
    success_rate_text: text.Text,
    sim_length: int,
    anywhere: bool = False,
    cut_plot = None,
) -> list:
    """Update animation frame with new data from simulation."""
    plot_candle1.set_data([simulation["candle1"][frame_number, 0]], [simulation["candle1"][frame_number, 1]])
    plot_candle2.set_data([simulation["candle2"][frame_number, 0]], [simulation["candle2"][frame_number, 1]])
    if anywhere:
        plot_cut.set_data(
            [cut_plot[frame_number, 0], cut_plot[frame_number, 2]],
            [cut_plot[frame_number, 1], cut_plot[frame_number, 3]],
        )
    else:
        plot_cut.set_data(
            [simulation["cut"][frame_number, 0],
             CENTER[0] * 2 - simulation["cut"][frame_number, 0]],  # [x, x reflected]
            [simulation["cut"][frame_number, 1],
             CENTER[1] * 2 - simulation["cut"][frame_number, 1]],  # [y, y reflected]
        )
    if simulation["success"][frame_number, 0]:
        plot_cut.set_color(SUCCESS_COLOR)
    else:
        plot_cut.set_color(FAILURE_COLOR)

    trial_num_text.set_text(f"Trial: {frame_number+1}/{sim_length}")
    if frame_number != 0:
        success_rate_text.set_text(f"Success rate: {simulation['success'][:frame_number, 0].mean() * 100:0.2f}%")

    return [plot_candle1, plot_candle2, plot_cut, trial_num_text, success_rate_text]


def simulation_animation_cut_through_center(
    rng: np.random.Generator,
    sim_length: int,
    show_candle_region: bool = False,
    save_animation: bool = False,
    save_filename: Path = Path(os.getcwd()).joinpath("round_cake.gif"),
):
    """
    Animate plots of simulation results, giving updated results as trials complete.

    Currently only case 1: cutting through the center of the cake, is implemented.

    Args:
        rng (np.random.Generator): random number generator
        sim_length (int): length of simulation, number of trials
        show_candle_region (bool, optional): Display region where candles are placed. Defaults to False.
        save_animation (bool, optional): Save animation to file as GIF. Defaults to False.
        save_filename (Path, optional): Path to save animation.
            Defaults to Path(os.getcwd()).joinpath("round_cake.gif").
    """
    #####################################################################
    ## Simple simulation, cut through the center
    #####################################################################
    sim = np.zeros(
        (sim_length, 2),
        dtype=[
            ("candle1", tuple),
            ("candle2", tuple),
            ("cut", tuple),
            ("success", bool),
        ],
    )

    ## Angle/position around the cake candles will be placed at
    theta = rng.uniform(0, 2 * np.pi, (sim_length, 5))
    ## Random radius from center that candles will be placed at
    radius = R * 0.65
    # radius = rng.uniform(0, R, (sim_length, 4)) ** 0.5

    x = radius * np.cos(theta[:, 0:4]) + CENTER[0]
    y = radius * np.sin(theta[:, 0:4]) + CENTER[1]

    sim["candle1"] = np.array([x[:, 0], y[:, 0]]).transpose()
    sim["candle2"] = np.array([x[:, 1], y[:, 1]]).transpose()
    sim["cut"] = np.array([x[:, 2], y[:, 2]]).transpose()  # cut always goes through center and point (x2, y2)
    # sim['cut'] = np.array([x[:, 2], y[:, 2], theta[:, 3]]).transpose()  # cut anywhere, theta angle at point (x,y)

    # Extending the cut segment for display to R*1.07
    sim["cut"] = np.array(
        [
            sim["cut"][:, 0] + ((sim["cut"][:, 0] - CENTER[0]) / radius) * CUT_DISPLAY_R,
            sim["cut"][:, 1] + ((sim["cut"][:, 1] - CENTER[1]) / radius) * CUT_DISPLAY_R,
        ]
    ).transpose()

    # Because cuts go through CENTER, they pass through adjacent quadrants (i.e. 1&3, 4&2, 2&4, etc.)
    # cut_with_quadrants: [x, y, quadrant, other quadrant]
    # cut_quadrants = [find_quadrant_rect(x,y) for x,y in sim['cut']]
    # cut_with_quadrants = np.column_stack((sim['cut'], cut_quadrants, [(((x-1) + 2) % 4) + 1 for x in cut_quadrants]))

    side_of_cut_c1 = np.sign(np.cross(np.subtract(sim["cut"][:, :2], CENTER), np.subtract(sim["candle1"], CENTER)))
    side_of_cut_c2 = np.sign(np.cross(np.subtract(sim["cut"][:, :2], CENTER), np.subtract(sim["candle2"], CENTER)))

    sim["success"] = np.array([side_of_cut_c1 != side_of_cut_c2, np.zeros(sim_length)]).transpose()
    print("Successful slice rate (cut through center): ", np.average(sim["success"][:, 0]))

    ## Create new Figure and an Axes which fills it.
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_axes([0, 0, 1, 1], polar=False, frameon=False)
    ax.set_xlim(-R * 1.5, R * 1.5)
    ax.set_ylim(-R * 1.5, R * 1.5)
    ax.set_xticks([])
    ax.set_yticks([])

    # Testing plot
    testing = False
    if testing:
        if sim_length < 10:
            for i in [sim["candle1"], sim["candle2"], sim["cut"]]:
                for idx, (x, y, *q) in enumerate(i):
                    ax.text(x, y, f"{idx} ({x:.2f},{y:.2f})", fontsize=12)
        ax.text(CENTER[0], CENTER[1], f"center ({CENTER[0]:.2f},{CENTER[1]:.2f})", fontsize=12)
        ax.text(0, 0, "(0,0)", fontsize=12)
        ax.vlines(CENTER[0], CENTER[1] - R, CENTER[1] + R, "lime", lw=6)
        ax.hlines(CENTER[1], CENTER[0] - R, CENTER[0] + R, "lime", lw=6)

    ## Text
    ax.text(
        0, 1.1,
        (
            "Probability slice will separate the two candles\n"
            "Cutting through the center of the cake"
        ),
        horizontalalignment="center",
        fontsize=20,
    )
    trial_num = ax.text(-1.2, 0.9, "Trial:", fontsize=18)
    success_rate = ax.text(0, 0.9, "Success rate:", fontsize=20)

    ## Background "boundaries"
    # Cake outline
    ax.add_patch(patches.Circle(CENTER, R, linewidth=1, edgecolor="k", facecolor="none"))
    # ax.add_patch(patches.Circle(CENTER, R*1.07, linewidth=1, edgecolor="r", facecolor="none"))
    # Candle placement path
    candle_region_legend = patches.Patch(fill=False, edgecolor="w", label=None)
    if show_candle_region:
        ax.add_patch(patches.Circle(CENTER, radius, linewidth=20, edgecolor="b", facecolor="none", alpha=0.25))
        candle_region_legend = patches.Patch(edgecolor="b", linewidth=9, alpha=0.25, fill=False, label="Candle region")

    ## Sim values
    candle1_plot = ax.plot(sim["candle1"][0, 0], sim["candle1"][0, 1], "b.", markersize=20)[0]
    candle2_plot = ax.plot(sim["candle2"][0, 0], sim["candle1"][0, 1], "g.", markersize=20)[0]
    cut_plot = ax.plot(
        [sim["cut"][0, 0], CENTER[0] * 2 - sim["cut"][0, 0]],  # [x, x reflected]
        [sim["cut"][0, 1], CENTER[1] * 2 - sim["cut"][0, 1]],  # [y, y reflected]
        linewidth=3,
        color=SUCCESS_COLOR if sim["success"][0, 0] else FAILURE_COLOR,
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

    # ax.scatter(sim["candle1"][:, 0], sim["candle1"][:, 1], s=500, marker=".", color="b")
    # ax.scatter(sim["candle2"][:, 0], sim["candle2"][:, 1], s=500, marker=".", color="g")
    # for i in range(sim_length):
    #     cut_plot1 = ax.plot(
    #         [sim['cut'][i, 0], CENTER[0] * 2 - sim['cut'][i, 0]],
    #         [sim['cut'][i, 1], CENTER[1] * 2 - sim['cut'][i, 1]],
    #         linewidth=3, color="k"
    #     )[0]
    #     ## ax.axline((cut[i, 0], cut[i, 1]), slope=cut[i, 2], color="red")  # cut anywhere?
    #     axline(  #TODO do I really actually need this
    #         ax,
    #         xy1=(sim['cut'][i, 0], sim['cut'][i, 1]),
    #         xy2=(CENTER[0] * 2 - sim['cut'][i, 0], CENTER[1] * 2 - sim['cut'][i, 1]),  # point reflection
    #         # xy2=CENTER,
    #         segment=True,
    #         color="r"
    #     )  # cut through center
    # # plt.show()

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

def simulation_animation_cut_anywhere(
    rng: np.random.Generator,
    sim_length: int,
    show_candle_region: bool = False,
    save_animation: bool = False,
    save_filename: Path = Path(os.getcwd()).joinpath("round_cake.gif"),
):
    """
    Animate plots of simulation results, giving updated results as trials complete.

    Currently only case 1: cutting through the center of the cake, is implemented.

    Args:
        rng (np.random.Generator): random number generator
        sim_length (int): length of simulation, number of trials
        show_candle_region (bool, optional): Display region where candles are placed. Defaults to False.
        save_animation (bool, optional): Save animation to file as GIF. Defaults to False.
        save_filename (Path, optional): Path to save animation.
            Defaults to Path(os.getcwd()).joinpath("round_cake.gif").
    """
    #####################################################################
    ## Simple simulation, cut anywhere
    #####################################################################
    sim = np.zeros(
        (sim_length, 2),
        dtype=[
            ("candle1", tuple),
            ("candle2", tuple),
            ("cut", tuple),
            ("success", bool),
        ],
    )

    ## Create new Figure and an Axes which fills it.
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_axes([0, 0, 1, 1], polar=False, frameon=False)
    ax.set_xlim(-R * 1.5, R * 1.5)
    ax.set_ylim(-R * 1.5, R * 1.5)
    ax.set_xticks([])
    ax.set_yticks([])

    ## Angle/position around the cake candles will be placed at
    theta = rng.uniform(0, 2 * np.pi, (sim_length, 5))
    ## Random radius from center that candles will be placed at
    radius = R * 0.65  # fixed radius
    # radius = rng.uniform(0, R, (sim_length, 4)) ** 0.5  # random position for all points

    x = radius * np.cos(theta[:, 0:4]) + CENTER[0]
    y = radius * np.sin(theta[:, 0:4]) + CENTER[1]

    sim["candle1"] = np.array([x[:, 0], y[:, 0]]).transpose()
    sim["candle2"] = np.array([x[:, 1], y[:, 1]]).transpose()
    # sim["cut"] = np.array([x[:, 2], y[:, 2]]).transpose()  # cut always goes through center and point (x2, y2)
    # Cut anywhere, through point (x2, y2) and (x3, y3)
    cut = np.array([x[:, 2], y[:, 2], x[:, 3], y[:, 3]]).transpose()
    # sim["cut"] = np.hstack((cut))

    def extend_lines(cut):
        def getExtrapolatedLine(p1, p2, extrapolate_ratio = sim_length):
            """Creates a line extrapolated in p1->p2 direction"""
            a = p1
            b = (
                p1[0] + extrapolate_ratio * (p2[0] - p1[0]),
                p1[1] + extrapolate_ratio * (p2[1] - p1[1]),
            )
            a = (
                p1[0] - extrapolate_ratio * (p2[0] - p1[0]),
                p1[1] - extrapolate_ratio * (p2[1] - p1[1]),
            )
            return sLineString([a,b])

        # print(cut)
        p = sPoint(CENTER)
        c = p.buffer(R * 1.07).boundary
        l = sLineString([[cut[0], cut[1]], [cut[2], cut[3]]])
        l_coords = np.array(l.coords)
        long_line = getExtrapolatedLine(*l_coords[-2:]) #we use the last two points
        # long_line_arr = np.array(long_line.coords)
        # print(long_line_arr)
        # ax.add_patch(patches.Circle(CENTER, R, linewidth=1, edgecolor="k", facecolor="none"))
        # ax.add_patch(patches.Circle(CENTER, R*1.07, linewidth=1, edgecolor="r", facecolor="none"))
        # for idx, (x, y, *q) in enumerate(long_line_arr):
        #     ax.text(x, y, f"{idx} ({x:.2f},{y:.2f})", fontsize=12)
        # ax.plot(long_line_arr[:,0], long_line_arr[:,1], color="lime", linewidth=5)
        intersect = c.intersection(long_line)
        # print(i)
        # if i:
        #FIXME i.geoms errors out sometimes, i has no points or only one point instead of two
        # increasing extrapolate_ratio seems to help, but not sure why it should, or why it has to be so large
        intersection_arr = np.hstack((np.array(intersect.geoms[0].coords[0]), np.array(intersect.geoms[1].coords[0])))
        # else:
        #     intersection_arr = np.zeros(4)
        # ax.plot(intersection_arr[0], intersection_arr[2], "y.", markersize=30)
        # ax.plot(intersection_arr[1], intersection_arr[3], "y.", markersize=30)
        # plt.show()

        return intersection_arr

    # print('cut[0]', cut[0])
    # print('inters', intersection_arr)
    # vfunc = np.vectorize(extend_lines)(cut)
    cut = np.array([extend_lines(x) for x in cut])
    # print(cut22)

    # a circle exterior to R, extend cut to intersect with exterior circle?
    # ax.add_patch(patches.Circle(CENTER, R*1.07, linewidth=1, edgecolor="r", facecolor="none"))
    # Extending the cut segment for display
    # cut2 = np.array(
    #     [
    #         cut[:, 0] + ((cut[:, 0] - cut[:, 2]) * ((1.7 - radius) / radius)), #CUT_DISPLAY_R / radius)),
    #         cut[:, 1] + ((cut[:, 1] - cut[:, 3]) * ((1.7 - radius) / radius)), #CUT_DISPLAY_R / radius)),
    #         cut[:, 2] + ((cut[:, 2] - cut[:, 0]) * ((1.7 - radius) / radius)), #CUT_DISPLAY_R / radius)),
    #         cut[:, 3] + ((cut[:, 3] - cut[:, 1]) * ((1.7 - radius) / radius)), #CUT_DISPLAY_R / radius)),
    #         # cut[:, 0],
    #         # cut[:, 1],
    #         # cut[:, 2],
    #         # cut[:, 3],
    #     ]
    # ).transpose()
    # print(cut2)

    # Because cuts go through CENTER, they pass through adjacent quadrants (i.e. 1&3, 4&2, 2&4, etc.)
    # cut_with_quadrants: [x, y, quadrant, other quadrant]
    # cut_quadrants = [find_quadrant_rect(x,y) for x,y in sim['cut']]
    # cut_with_quadrants = np.column_stack((sim['cut'], cut_quadrants, [(((x-1) + 2) % 4) + 1 for x in cut_quadrants]))

    side_of_cut_c1 = np.sign(np.cross(
        np.subtract(cut[:, :2], cut[:, 2:]),
        np.subtract(sim["candle1"], cut[:, 2:])
    ))
    side_of_cut_c2 = np.sign(np.cross(
        np.subtract(cut[:, :2], cut[:, 2:]),
        np.subtract(sim["candle2"], cut[:, 2:])
    ))

    sim["success"] = np.array([side_of_cut_c1 != side_of_cut_c2, np.zeros(sim_length)]).transpose()
    print("Successful slice rate (cut anywhere, fixed radius): ", np.average(sim["success"][:, 0]))

    # # Testing plot
    # testing = True
    # if testing:
    #     if sim_length < 10:
    #         for i in [sim["candle1"], sim["candle2"], cut]:
    #             for idx, (x, y, *q) in enumerate(i):
    #                 ax.text(x, y, f"{idx} ({x:.2f},{y:.2f})", fontsize=12)
    #     ax.text(CENTER[0], CENTER[1], f"center ({CENTER[0]:.2f},{CENTER[1]:.2f})", fontsize=12)
    #     ax.text(0, 0, "(0,0)", fontsize=12)
    #     ax.vlines(CENTER[0], CENTER[1] - R, CENTER[1] + R, "lime", lw=6)
    #     ax.hlines(CENTER[1], CENTER[0] - R, CENTER[0] + R, "lime", lw=6)

    ## Text
    ax.text(
        0, 1.1,
        (
            "Probability slice will separate the two candles\n"
            "Cutting anywhere, fixed radius"
        ),
        horizontalalignment="center",
        fontsize=20,
    )
    trial_num = ax.text(-1.2, 0.9, "Trial:", fontsize=18)
    success_rate = ax.text(0, 0.9, "Success rate:", fontsize=20)

    ## Background "boundaries"
    # Cake outline
    ax.add_patch(patches.Circle(CENTER, R, linewidth=1, edgecolor="k", facecolor="none"))
    # ax.add_patch(patches.Circle(CENTER, R*1.07, linewidth=1, edgecolor="r", facecolor="none"))
    # Candle placement path
    candle_region_legend = patches.Patch(fill=False, edgecolor="w", label=None)
    if show_candle_region:
        ax.add_patch(patches.Circle(CENTER, radius, linewidth=20, edgecolor="b", facecolor="none", alpha=0.25))
        candle_region_legend = patches.Patch(edgecolor="b", linewidth=9, alpha=0.25, fill=False, label="Candle region")

    ## Sim values
    candle1_plot = ax.plot(sim["candle1"][0, 0], sim["candle1"][0, 1], "b.", markersize=20)[0]
    candle2_plot = ax.plot(sim["candle2"][0, 0], sim["candle2"][0, 1], "g.", markersize=20)[0]
    cut_plot = ax.plot(
        [cut[0, 0], cut[0, 2]],  # [x, x reflected]
        [cut[0, 1], cut[0, 3]],  # [y, y reflected]
        linewidth=3,
        color=SUCCESS_COLOR if sim["success"][0, 0] else FAILURE_COLOR,
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

    # ax.scatter(sim["candle1"][:, 0], sim["candle1"][:, 1], s=500, marker=".", color="b")
    # ax.scatter(sim["candle2"][:, 0], sim["candle2"][:, 1], s=500, marker=".", color="g")
    # for i in range(sim_length):
    #     cut_plot1 = ax.plot(
    #         # [cut[i, 0], CENTER[0] * 2 - cut[i, 0]],
    #         # [cut[i, 1], CENTER[1] * 2 - cut[i, 1]],
    #         [cut[i, 0], cut[i, 2]],
    #         [cut[i, 1], cut[i, 3]],
    #         linewidth=3, color="k"
    #     )[0]
    #     cut2_plot1 = ax.plot(
    #         # [cut[i, 0], CENTER[0] * 2 - cut[i, 0]],
    #         # [cut[i, 1], CENTER[1] * 2 - cut[i, 1]],
    #         [cut2[i, 0], cut2[i, 2]],
    #         [cut2[i, 1], cut2[i, 3]],
    #         linewidth=3, color="darkorange", alpha=0.3
    #     )[0]
    #     ## ax.axline((cut[i, 0], cut[i, 1]), slope=cut[i, 2], color="red")  # cut anywhere?
    #     # axline(  #TODO do I really actually need this
    #     #     ax,
    #     #     xy1=(sim['cut'][i, 0], sim['cut'][i, 1]),
    #     #     xy2=(CENTER[0] * 2 - sim['cut'][i, 0], CENTER[1] * 2 - sim['cut'][i, 1]),  # point reflection
    #     #     # xy2=CENTER,
    #     #     segment=True,
    #     #     color="r"
    #     # )  # cut through center
    # plt.show()

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
            anywhere=True,
            cut_plot=cut,
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
    simulation_animation_cut_through_center(
        rng_main,
        sim_length_main,
        show_candle_region=True,
        save_animation=save_animation_main,
        save_filename=Path("./cake_cutting/result_animations/round_cake_cut_from_center.gif"),
    )
    simulation_animation_cut_anywhere(
        rng_main,
        sim_length_main,
        show_candle_region=True,
        save_animation=save_animation_main,
        save_filename=Path("./cake_cutting/result_animations/round_cake_cut_anywhere_fixedrad_candleregion.gif"),
    )
