import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set the random seed for reproducibility
np.random.seed(42)

# Initial data
x_data = []
y_data = []

# Create the figure and subplots
fig = make_subplots(rows=1, cols=2, subplot_titles=("Distribution", "Sample"))

# Create the scatter plot for the distribution
scatter = fig.add_trace(
    go.Scatter(x=x_data, y=y_data, mode="markers", marker=dict(size=8)),
    row=1, col=1
)

# Create the histogram for the sample
histogram = fig.add_trace(
    go.Histogram(x=x_data, nbinsx=30, marker=dict(color='rgba(0,0,0,0.5)')),
    row=1, col=2
)

# Set the layout
fig.update_layout(
    height=500,
    showlegend=False,
    title_text="Normal Distribution",
    xaxis=dict(title="Value"),
    yaxis=dict(title="Density"),
    bargap=0.2
)

# Update the subplot sizes
fig.update_layout(
    autosize=False,
    width=800,
    height=500,
    margin=dict(l=50, r=50, t=80, b=80),
    paper_bgcolor="white"
)

# Show the initial plot
fig.show()

# Create the sliders
speed_slider = dict(
    pad=dict(t=50, r=10),
    currentvalue=dict(visible=True, xanchor="right", prefix="Speed: ", font=dict(size=16)),
    len=0.9,
    x=0.1,
    y=0,
    steps=[
        dict(method="animate", args=[[None], {"frame": {"duration": 500, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}], label="Pause"),
        dict(method="animate", args=[[None], {"frame": {"duration": 200, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}], label="Slow"),
        dict(method="animate", args=[[None], {"frame": {"duration": 50, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}], label="Fast")
    ],
)

mean_slider = dict(
    pad=dict(t=50, r=10),
    currentvalue=dict(visible=True, xanchor="right", prefix="Mean: ", font=dict(size=16)),
    len=0.9,
    x=0.1,
    y=-0.1,
    steps=[
        dict(label="0", method="restyle", args=["mean", 0]),
        dict(label="1", method="restyle", args=["mean", 1]),
        dict(label="2", method="restyle", args=["mean", 2]),
        dict(label="3", method="restyle", args=["mean", 3])
    ],
)

sample_size_slider = dict(
    pad=dict(t=50, r=10),
    currentvalue=dict(visible=True, xanchor="right", prefix="Sample Size: ", font=dict(size=16)),
    len=0.9,
    x=0.1,
    y=-0.2,
    steps=[
        dict(label="100", method="restyle", args=["sample_size", 100]),
        dict(label="500", method="restyle", args=["sample_size", 500]),
        dict(label="1000", method="restyle", args=["sample_size", 1000])
    ],
)

# Add the sliders to the layout
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            buttons=[
                dict(label="Play", method="animate", args=[None, {"frame": {"duration": 500, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}]),
                dict(label="Pause", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]),
            ],
            pad=dict(t=50, r=10),
            x=0.1,
            y=-0.3
        )
    ],
    sliders=[speed_slider, mean_slider, sample_size_slider]
)

# Show the updated plot
fig.show()

# Define the animation frames
frames = []

# Define the number of frames
num_frames = 100

# Generate data for each frame
for frame in range(num_frames):
    # Generate random points from the normal distribution based on the current mean and sample size
    mean = fig.data[0]['mean']
    sample_size = fig.data[0]['sample_size']
    data = np.random.normal(loc=mean, scale=1, size=sample_size)

    # Update the data in the scatter plot and histogram
    fig.frames.append(go.Frame(
        data=[go.Scatter(x=data, y=np.zeros(sample_size), mode="markers", marker=dict(size=8)),
              go.Histogram(x=data, nbinsx=30, marker=dict(color='rgba(0,0,0,0.5)'))]
    ))

# Add the frames to the figure
fig.update(frames=frames)

# Play the animation
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            buttons=[
                dict(label="Play", method="animate", args=[None, {"frame": {"duration": 500, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}]),
                dict(label="Pause", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]),
            ],
            pad=dict(t=50, r=10),
            x=0.1,
            y=-0.3
        )
    ]
)

# Show the final plot
fig.show()


