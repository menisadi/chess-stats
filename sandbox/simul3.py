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

# Adjusted figure size and subplot layout
fig, axs = plt.subplots(len(sample_sizes), 1, figsize=(8, 9))

# Function to update the plot
def update(num_points):
    for i, sample_size in enumerate(sample_sizes):
        ax = axs[i]
        ax.clear()
        ax.set_xlim(-5, 5)
        ax.set_ylim(0, 1.1)
        ax.set_xticks(range(-4, 5))
        ax.get_yaxis().set_visible(False)

        points = np.random.normal(mean, variance, sample_size)
        rando_heights = np.random.uniform(0.05, 0.15, sample_size)

        # Increased scatter plot marker size
        ax.scatter(points, rando_heights, s=40, alpha=0.5)

        # Annotate the maximum point
        max_point = max(points)
        ax.scatter(max_point, np.random.uniform(0.05, 0.15), s=40, c='r', alpha=0.5)

        # Accumulate maximum points in the histogram
        maxes[i].append(max_point)
        hists[i], bins[i] = np.histogram(maxes[i], bins=40, range=(-10, 10), density=True)
        ax.bar(bins[i][:-1], hists[i], width=0.5, alpha=0.5)

        # Adjusted title placement inside the plot
        ax.text(-4.5, 1, f'Sample Size: {sample_size}', fontsize=12, fontweight='bold')

    fig.canvas.draw()

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=150, interval=200)

# Save the animation
# ani.save('simul2.gif', writer='imagemagick', fps=5)
ani.save('simul3.mp4', writer='ffmpeg', fps=5)

# Show the plots
# plt.show()

