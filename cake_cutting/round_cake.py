import os
from functools import partial
from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
from matplotlib import patches, lines, text, transforms
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.axes import Axes
import numpy as np
import numpy.typing as npt

from axline import axline


R: float = 1
CENTER: "tuple[float, float]" = (0, -0.35)
CUT_DISPLAY_R: float = 0.42


# FIXME problem is now 2D if cut can be anywhere? long cake would be the same?
# still 1D, fix cut to origin/center and rotate, candles can be anywhere in circle
# check half-plane created by cut that each candle is in


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

    x = radius * np.cos(theta[:, 0:4]) #+ CENTER[0]
    y = radius * np.sin(theta[:, 0:4]) #+ CENTER[1]

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
) -> list:
    """Update animation frame with new data from simulation."""
    plot_candle1.set_data([simulation["candle1"][frame_number, 0]], [simulation["candle1"][frame_number, 1]])
    plot_candle2.set_data([simulation["candle2"][frame_number, 0]], [simulation["candle2"][frame_number, 1]])
    plot_cut.set_data(
        [simulation["cut"][frame_number], simulation["cut"][frame_number]],
        [RECT_POSITION[1] - 0.05, RECT_POSITION[1] + RECT_SIZE[1] + 0.05]
    )
    if simulation["success"][frame_number]:
        plot_cut.set_color("r")
    else:
        plot_cut.set_color("k")

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
):
    #####################################################################
    ## For animation plot
    #####################################################################
    sim = np.zeros(
        (sim_length, 2),
        dtype=[
            ('candle1', tuple),
            ('candle2', tuple),
            ('cut',     tuple),
            ('success', bool)
        ]
    )

    # sim['candle1'] = rng.uniform(0.1, 0.9, sim_length)
    # sim['candle2'] = rng.uniform(0.1, 0.9, sim_length)
    # sim['cut'] = rng.uniform(0.1, 0.9, sim_length)
    # sim['success'] = ((sim['candle1'] < sim['cut']) & (sim['cut'] < sim['candle2'])
    #                     | (sim['candle2'] < sim['cut']) & (sim['cut'] < sim['candle1']))

    theta = rng.uniform(0, 2 * np.pi, (sim_length, 5))
    ## Random radius from center that candles will be placed at
    radius = R*0.65
    # radius = rng.uniform(0, R, (sim_length, 4)) ** 0.5

    x = radius * np.cos(theta[:, 0:4]) #+ CENTER[0]
    y = radius * np.sin(theta[:, 0:4]) #+ CENTER[1]

    sim['candle1'] = np.array([x[:, 0], y[:, 0]]).transpose()
    sim['candle2'] = np.array([x[:, 1], y[:, 1]]).transpose()
    sim['cut'] = np.array([x[:, 2], y[:, 2]]).transpose()  # cut always goes through center and point (x2, y2)
    print(sim["candle1"])

    # side_of_cut_c1 = np.sign(np.cross(np.subtract(cut[:,:2], CENTER), np.subtract(c1, CENTER)))
    # side_of_cut_c2 = np.sign(np.cross(np.subtract(cut[:,:2], CENTER), np.subtract(c2, CENTER)))
    side_of_cut_c1 = np.sign(np.cross(sim['cut'][:, :2], sim['candle1']))
    side_of_cut_c2 = np.sign(np.cross(sim['cut'][:, :2], sim['candle2']))

    sim['success'] = np.array([side_of_cut_c1 != side_of_cut_c2, np.zeros(sim_length)]).transpose()
    print('Successful slice rate: ', np.average(sim['success'][:, 0]))
    count = 0
    for candle1_side, candle2_side in zip(side_of_cut_c1, side_of_cut_c2):
        if candle1_side != candle2_side:
            count += 1
    print(f"Successful slice rate (cut through center): {count / sim_length}")



    ##################################################################################
    # theta = rng.uniform(0, 2 * np.pi, (sim_length, 4))
    # Radius that candles will be placed at
    # radius = rng.uniform(0, R, (sim_length, 3)) ** 0.5
    # radius = R*0.65

    # x = radius * np.cos(theta[:, 0:3]) + CENTER[0]
    # y = radius * np.sin(theta[:, 0:3]) + CENTER[1]

    c1 = np.array([x[:, 0], y[:, 0]]).transpose()
    c2 = np.array([x[:, 1], y[:, 1]]).transpose()
    # cut = np.array([x[:, 2], y[:, 2], theta[:, 3]]).transpose()  # cut anywhere, theta angle at point (x,y)
    cut = np.array([x[:, 2], y[:, 2]]).transpose()
    print(c1)

    # Because cuts go through CENTER, they pass through adjacent quadrants (i.e. 1&3, 4&2, 2&4, etc.)
    # cut: [x, y, quadrant, other quadrant]
    cut_quadrants = [find_quadrant_rect(x,y) for x,y in cut]
    cut = np.column_stack((cut, cut_quadrants, [(((x-1) + 2) % 4) + 1 for x in cut_quadrants]))
    # print(cut)


    new_cut = np.array(
        [cut[:, 0] + ((cut[:, 0] - CENTER[0]) / radius) * CUT_DISPLAY_R,
         cut[:, 1] + ((cut[:, 1] - CENTER[1]) / radius) * CUT_DISPLAY_R]
    ).transpose()

    # Extending the cut segment shouldn't change the quadrants it's in
    new_cut_quadrants = [find_quadrant_rect(x,y) for x,y in new_cut]
    new_cut = np.column_stack((new_cut, new_cut_quadrants, [(((x-1) + 2) % 4) + 1 for x in new_cut_quadrants]))
    # print('newc', new_cut[:,:2])
    # print('new-', np.subtract(new_cut[:,:2], CENTER))
    # print()

    side_of_cut_c1 = np.sign(np.cross(np.subtract(new_cut[:,:2], CENTER), np.subtract(c1, CENTER)))
    side_of_cut_c2 = np.sign(np.cross(np.subtract(new_cut[:,:2], CENTER), np.subtract(c2, CENTER)))
    # print(side_of_cut_c1)
    # print(side_of_cut_c2)

    count = 0
    for can1, can2 in zip(side_of_cut_c1, side_of_cut_c2):
        if can1 != can2:
            # print("No split. Same side.")
            count += 1
        # else:
            # print("Candles split. Opposite sides.")
    # print("Successful slice rate: ", count / sim_length)


    # Visualize the points:
    fig = plt.figure(figsize=(7, 7))
    # ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    # plt.xlim(-1, 1), ax.set_xticks([])
    # plt.ylim(-1, 1), ax.set_yticks([])
    ax = fig.add_axes([0, 0, 1, 1], polar=False, frameon=False)
    ax.set_xlim(-R*1.5, R*1.5)
    ax.set_ylim(-R*1.5, R*1.5)
    ax.set_xticks([])
    ax.set_yticks([])

    # Cake outline
    ax.add_patch(patches.Circle(CENTER, R, linewidth=1, edgecolor="k", facecolor="none"))

    # Candle placement path
    ax.add_patch(patches.Circle(CENTER, radius, linewidth=20, edgecolor="b", facecolor="none", alpha=0.25))
    # ax.add_patch(patches.Circle(CENTER, radius+0.05, linewidth=1, edgecolor="b", facecolor="none"))
    # ax.add_patch(patches.Circle(CENTER, radius-0.05, linewidth=1, edgecolor="b", facecolor="none"))

    ## Text
    ax.text(-1.3, 1.2, 'Probability slice will separate the two candles', fontsize=20)
    trial_num = ax.text(-1.2, 0.9, 'Trial:', fontsize=18)
    success_rate = ax.text(0, 0.9, 'Success rate:', fontsize=20)

    # Testing plot
    for i in [c1, c2, cut]:
        for idx, (x,y,*q) in enumerate(i):
            ax.text(x, y, f"{idx} ({x:.2f},{y:.2f})", fontsize=12)
    ax.text(CENTER[0], CENTER[1], f"center ({CENTER[0]:.2f},{CENTER[1]:.2f})", fontsize=12)
    ax.text(0, 0, "(0,0)", fontsize=12)
    ax.vlines(CENTER[0], CENTER[1]-R, CENTER[1]+R, "lime", lw=6)
    ax.hlines(CENTER[1], CENTER[0]-R, CENTER[0]+R, "lime", lw=6)


    ax.scatter(c1[:, 0], c1[:, 1], s=500, marker=".", color="b")
    ax.scatter(c2[:, 0], c2[:, 1], s=500, marker=".", color="g")
    for i in range(sim_length):
        cut_plot1 = ax.plot(
            [new_cut[i, 0], CENTER[0] * 2 - new_cut[i, 0]],
            [new_cut[i, 1], CENTER[1] * 2 - new_cut[i, 1]],
            linewidth=3, color="k"
        )[0]
        ## ax.axline((cut[i, 0], cut[i, 1]), slope=cut[i, 2], color="red")  # cut anywhere?
        axline(  #TODO do I really actually need this
            ax,
            xy1=(new_cut[i, 0], new_cut[i, 1]),
            xy2=(CENTER[0] * 2 - new_cut[i, 0], CENTER[1] * 2 - new_cut[i, 1]),  # point reflection
            # xy2=CENTER,
            segment=True,
            color="r"
        )  # cut through center
    # plt.show()


    ## Sim values
    candle1_plot = ax.plot(sim["candle1"][0, 0], sim["candle1"][0, 1], "b.", markersize=20)[0]
    candle2_plot = ax.plot(sim["candle2"][0, 0], sim["candle1"][0, 1], "g.", markersize=20)[0]
    cut_plot = ax.plot([], [], linewidth=3, color="k")[0]
    plt.show()



    # ## Create new Figure and an Axes which fills it.
    # fig = plt.figure(figsize=(7, 7))
    # ax = fig.add_axes([0, 0, 1, 1], frameon=False)
    # ax.set_xlim(0, 1)
    # ax.set_ylim(0, 1)
    # ax.set_xticks([])
    # ax.set_yticks([])

    # ## Background "boundaries"
    # rect = patches.Rectangle((0.1, 0.25), 0.8, 0.35, linewidth=1, edgecolor='k', facecolor='none')
    # ax.add_patch(rect)
    # circ = patches.Circle((0.5, 0.4), 0.3, linewidth=1, edgecolor="k", facecolor="none")
    # ax.add_patch(circ)

    # ## Sim values
    # # candle1_plot = ax.plot(sim['candle1'][0], 0.45, 'b.', markersize=20)[0]
    # # candle2_plot = ax.plot(sim['candle2'][0], 0.45, 'g.', markersize=20)[0]
    # # cut_plot = ax.plot([], [], linewidth=3, color='k')[0]

    # ## Text
    # ax.text(0.05, 0.9, 'Probability slice will separate the two candles', fontsize=20)
    # trial_num = ax.text(0.05, 0.8, 'Trial:', fontsize=18)
    # success_rate = ax.text(0.5, 0.8, 'Success rate:', fontsize=20)

    # scat1 = ax.scatter(c1[0,0], c1[0,1], s=10, marker='.', color='b')
    # scat2 = ax.scatter(c2[0,0], c2[0,1], s=10, marker='.', color='g')
    # line = ax.axline((cut[0,0], cut[0,1]), slope=cut[0,2], color='red')

    # def update(frame_number):
    #     scat1.set_offsets([c1[frame_number,0], c1[frame_number,1]])
    #     scat2.set_offsets([c2[frame_number,0], c2[frame_number,1]])
    #     line.set_data((cut[frame_number,0], cut[frame_number,1]), slope=cut[frame_number,2], color='red')


    #     # candle1_plot.set_data(sim['candle1'][frame_number], 0.45)
    #     # candle2_plot.set_data(sim['candle2'][frame_number], 0.45)
    #     # cut_plot.set_data(
    #     #     [sim['cut'][frame_number], sim['cut'][frame_number]], [0.2, 0.65]
    #     # )
    #     # if sim['success'][frame_number]:
    #     #     cut_plot.set_color('r')
    #     # else:
    #     #     cut_plot.set_color('k')

    #     # trial_num.set_text(f"Trial: {frame_number}/{sim_length}")
    #     # if frame_number != 0:
    #     #     success_rate.set_text(f"Success rate: {sim['success'][:frame_number].mean() * 100:0.2f}%")


    # ## Construct the animation, using the update function as the animation director.
    # animation = FuncAnimation(fig, update, interval=100, repeat=False) #fargs=(cut_plot, ),
    # # animation.save('long cake.mp4')

    # plt.show()

if __name__ == "__main__":
    rng_main = np.random.default_rng(seed=123)
    sim_length_main = 3
    save_animation_main = False

    print("The probability a slice will separate the two candles:")
    print(f"Simulation: {sim_length_main} trials.")

    # simple_simulation(rng_main, sim_length_main)
    simulation_animation(
        rng_main,
        sim_length_main,
        show_candle_region=False,
        save_animation=save_animation_main,
        save_filename=Path("./cake_cutting/long_cake.gif"),
    )
