import numpy as np
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

app = dash.Dash(__name__)

sample_size = 100
frames = 100
starting_frame = 0

# Create initial data
data = pd.DataFrame({'value': np.random.normal(size=sample_size * frames),
                     'hight': np.random.uniform(size=sample_size * frames),
                     'frame': np.arange(frames).repeat(sample_size)})
data['max_value'] = data.groupby('frame')['value'].transform('max')
data['is_max'] = data['value'] == data['max_value']
colors = np.where(data['is_max'], 'red', 'blue')

fig = px.scatter(data_frame=data, x='value', y='hight', color=colors,
                 animation_frame='frame', width=800, height=300)
fig.update_xaxes(range=[-4, 4])

# Define the layout with the slider, reset button, and title
app.layout = html.Div([
    dcc.Slider(
        id='sample-size-slider',
        min=10,
        max=500,
        step=10,
        value=sample_size,
        marks={str(size): str(size) for size in range(10, 501, 50)}
    ),
    html.Button('Reset', id='reset-button', n_clicks=0),
    html.H3(id='sample-size-title'),
    dcc.Graph(id='scatter-plot', figure=fig)
])


@app.callback(
    [dash.dependencies.Output('scatter-plot', 'figure'),
     dash.dependencies.Output('sample-size-title', 'children')],
    [dash.dependencies.Input('sample-size-slider', 'value'),
     dash.dependencies.Input('reset-button', 'n_clicks')]
)
def update_scatter_plot(sample_size, reset_clicks):
    if reset_clicks > 0:
        current_frame = starting_frame
    else:
        current_frame = (reset_clicks % frames) + starting_frame

    # Generate new data based on the updated sample_size and current_frame
    data = pd.DataFrame({'value': np.random.normal(size=sample_size * frames),
                         'hight': np.random.uniform(size=sample_size * frames),
                         'frame': np.arange(frames).repeat(sample_size)})
    data['max_value'] = data.groupby('frame')['value'].transform('max')
    data['is_max'] = data['value'] == data['max_value']
    colors = np.where(data['is_max'], 'red', 'blue')

    fig = px.scatter(data_frame=data, x='value', y='hight', color=colors,
                     animation_frame='frame', width=800, height=300)
    fig.update_xaxes(range=[-4, 4])

    # Update the title with the current sample size and frame
    title = f"Sample Size: {sample_size}, Current Frame: {current_frame}"

    return fig, title


if __name__ == '__main__':
    app.run_server(debug=True)

