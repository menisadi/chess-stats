import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

mean = 0
sample_size = 100
variance = 1

# Create the histogram
maxes = []
hists, bins = np.histogram(maxes, bins=40, range=(-10, 10))

fig, ax = plt.subplots()

# Function to update the plot
def update(num_points):
    ax.clear()
    ax.set_xlim(-8, 8)
    ax.set_ylim(0, 2)
    ax.get_yaxis().set_visible(False)

    # mean = slider_mean.val
    # sample_size = int(slider_sample.val)
    # variance = slider_variance.val

    ax.set_title(
        f'Normal Distribution\nSample Size: {sample_size}')

    points = np.random.normal(mean, variance, sample_size)
    rando_heights = np.random.uniform(0.05, 0.15, sample_size)
    ax.scatter(points, rando_heights, s=25, alpha=0.5)
    ax.scatter([max(points)], [0.1], s=45, c='red', alpha=0.9)

    # Accumulate maximum points in the histogram
    maxes.append(max(points))
    hists, bins = np.histogram(maxes, bins=40,
                               range=(-10, 10), density=True)
    ax.bar(bins[:-1], hists, width=0.5, alpha=0.5)

    ax.figure.canvas.draw()

# Create the animation
ani = animation.FuncAnimation(fig, update,
                              frames=100, interval=200)
# save animation as video
ani.save('static.mp4', writer='ffmpeg', fps=5)

# show animation 
# plt.show()

