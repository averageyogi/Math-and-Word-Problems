import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

rng = np.random.default_rng(seed=123)

sim_length = 100

#####################################################################
## Simple simulation
#####################################################################
R = 1

theta = rng.uniform(0, 2*np.pi, (sim_length, 4))
radius = rng.uniform(0, R, (sim_length, 3)) ** 0.5

x = radius * np.cos(theta[:,0:3])
y = radius * np.sin(theta[:,0:3])

c1 = np.array([x[:,0],y[:,0]]).transpose()
c2 = np.array([x[:,1],y[:,1]]).transpose()
cut = np.array([x[:,2],y[:,2],theta[:,3]]).transpose()

# visualize the points:
# fig = plt.figure(figsize=(7, 7))
# # ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# # plt.xlim(-1, 1), ax.set_xticks([])
# # plt.ylim(-1, 1), ax.set_yticks([])
# plt.scatter(c1[:,0], c1[:,1], s=10, marker='.', color='b')
# plt.scatter(c2[:,0], c2[:,1], s=10, marker='.', color='g')
# for i in range(sim_length):
#     plt.axline((cut[i,0], cut[i,1]), slope=cut[i,2], color='red')
# plt.show()

# count = 0
# for i in range(sim_length):
#     if (((c1[i] < cut[i]) and (cut[i] < c2[i])) or
#         ((c2[i] < cut[i]) and (cut[i] < c1[i]))):
#         count += 1
# print('Successful slice rate: ', count/sim_length)



#####################################################################
## For animation plot
#####################################################################
# sim = np.zeros(
#     sim_length,
#     dtype=[
#         ('candle1', float),
#         ('candle2', float),
#         ('cut',     float),
#         ('success', bool)
#     ]
# )

# sim['candle1'] = rng.uniform(0.1, 0.9, sim_length)
# sim['candle2'] = rng.uniform(0.1, 0.9, sim_length)
# sim['cut'] = rng.uniform(0.1, 0.9, sim_length)
# sim['success'] = ((sim['candle1'] < sim['cut']) & (sim['cut'] < sim['candle2']) 
#                     | (sim['candle2'] < sim['cut']) & (sim['cut'] < sim['candle1']))
# print('Successful slice rate: ', np.average(sim['success']))


## Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])

## Background "boundaries"
rect = patches.Rectangle((0.1, 0.25), 0.8, 0.35, linewidth=1, edgecolor='k', facecolor='none')
ax.add_patch(rect)
circ = patches.Circle((0.5, 0.4), 0.3, linewidth=1, edgecolor="k", facecolor="none")
ax.add_patch(circ)

## Sim values
# candle1_plot = ax.plot(sim['candle1'][0], 0.45, 'b.', markersize=20)[0]
# candle2_plot = ax.plot(sim['candle2'][0], 0.45, 'g.', markersize=20)[0]
# cut_plot = ax.plot([], [], linewidth=3, color='k')[0]

## Text
ax.text(0.05, 0.9, 'Probability slice will separate the two candles', fontsize=20)
trial_num = ax.text(0.05, 0.8, 'Sample', fontsize=18) #TODO remove 'Sample'
success_rate = ax.text(0.5, 0.8, 'Sample', fontsize=20)

scat1 = ax.scatter(c1[0,0], c1[0,1], s=10, marker='.', color='b')
scat2 = ax.scatter(c2[0,0], c2[0,1], s=10, marker='.', color='g')
line = ax.axline((cut[0,0], cut[0,1]), slope=cut[0,2], color='red')

def update(frame_number):
    scat1.set_offsets([c1[frame_number,0], c1[frame_number,1]])
    scat2.set_offsets([c2[frame_number,0], c2[frame_number,1]])
    line.set_data((cut[frame_number,0], cut[frame_number,1]), slope=cut[frame_number,2], color='red')



    # candle1_plot.set_data(sim['candle1'][frame_number], 0.45)
    # candle2_plot.set_data(sim['candle2'][frame_number], 0.45)
    # cut_plot.set_data(
    #     [sim['cut'][frame_number], sim['cut'][frame_number]], [0.2, 0.65]
    # )
    # if sim['success'][frame_number]:
    #     cut_plot.set_color('r')
    # else:
    #     cut_plot.set_color('k')

    # trial_num.set_text(f"Trial: {frame_number}/{sim_length}")
    # if frame_number != 0:
    #     success_rate.set_text(f"Success rate: {sim['success'][:frame_number].mean() * 100:0.2f}%")


## Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=100, repeat=False) #fargs=(cut_plot, ), 
# animation.save('long cake.mp4')

plt.show()
