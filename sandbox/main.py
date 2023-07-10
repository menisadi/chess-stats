import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.widgets as widgets

# Initialize the figure and axes
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # Adjust the bottom margin for the slider bars

# Set the initial parameters
mean = 0
sample_size = 100
speed = 100

# Create the slider bars
ax_mean = plt.axes([0.15, 0.05, 0.7, 0.03])  # Slider for mean
ax_sample = plt.axes([0.15, 0.1, 0.7, 0.03])  # Slider for sample size
ax_speed = plt.axes([0.15, 0.15, 0.7, 0.03])  # Slider for speed
slider_mean = widgets.Slider(ax_mean, 'Mean', -10, 10, valinit=mean)
slider_sample = widgets.Slider(ax_sample, 'Sample Size', 10, 1000, valinit=sample_size)
slider_speed = widgets.Slider(ax_speed, 'Speed', 1, 1000, valinit=speed)

# Function to update the plot
def update(num_points):
    ax.clear()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-1.5, 1.5)
    ax.set_title('Normal Distribution')
    # ax.tick_params(axis='y', which='both', left=False, right=False) 
    # ax.spines['bottom'].set_position('center')
    # hide the y axis
    ax.get_yaxis().set_visible(False)

    # Update the parameters from the sliders
    mean = slider_mean.val
    sample_size = int(slider_sample.val)
    speed = slider_speed.val

    # Generate random points from the normal distribution
    points = np.random.normal(mean, 1, sample_size)

    # Plot the histogram of the points
    ax.scatter(points, [1]*len(points), s=25, alpha=0.5)
    ax.scatter([max(points)], [1], s=45, c='red', alpha=0.9)

# Update the plot when sliders are changed
slider_mean.on_changed(update)
slider_sample.on_changed(update)
slider_speed.on_changed(update)

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=int(speed/10), interval=500)

plt.show()

