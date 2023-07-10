import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

mean = 0
sample_sizes = [10, 100, 1000]  # Different sample sizes
variance = 1

# Create the histograms
maxes = [[] for _ in sample_sizes]
hists = [[] for _ in sample_sizes]
bins = [[] for _ in sample_sizes]

fig, axs = plt.subplots(1, len(sample_sizes), figsize=(12, 3))

# Function to update the plot
def update(num_points):
    for i, sample_size in enumerate(sample_sizes):
        ax = axs[i]
        ax.clear()
        ax.set_xlim(-5, 5)
        ax.set_ylim(0, 1.1)
        ax.set_xticks(range(-4,5))
        ax.get_yaxis().set_visible(False)

        ax.set_title(f'Sample Size: {sample_size}')

        points = np.random.normal(mean, variance, sample_size)
        rando_heights = np.random.uniform(0.05, 0.15, sample_size)
        ax.scatter(points, rando_heights, s=25, alpha=0.5)
        ax.scatter([max(points)], [0.1], s=45, c='red', alpha=0.9)

        # Accumulate maximum points in the histogram
        maxes[i].append(max(points))
        hists[i], bins[i] = np.histogram(maxes[i], bins=40, range=(-10, 10), density=True)
        ax.bar(bins[i][:-1], hists[i], width=0.5, alpha=0.5)

    fig.canvas.draw()

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=150, interval=200)

# plt.tight_layout()

# Save animation as video
ani.save('simul.mp4', writer='ffmpeg', fps=5)

# Show the plots
# plt.show()

