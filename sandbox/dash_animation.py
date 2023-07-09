import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

app = dash.Dash(__name__)

sample_size = 100
frames = 100

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

# Define the layout with the slider and title
app.layout = html.Div([
    dcc.Slider(
        id='sample-size-slider',
        min=10,
        max=500,
        step=10,
        value=sample_size,
        marks={str(size): str(size) for size in range(10, 501, 50)}
    ),
    html.H3(id='sample-size-title'),
    dcc.Graph(id='scatter-plot', figure=fig)
])


@app.callback(
    [dash.dependencies.Output('scatter-plot', 'figure'),
     dash.dependencies.Output('sample-size-title', 'children')],
    [dash.dependencies.Input('sample-size-slider', 'value')]
)
def update_scatter_plot(sample_size):
    # Generate new data based on the updated sample_size
    data = pd.DataFrame({'value': np.random.normal(size=sample_size * frames),
                         'hight': np.random.uniform(size=sample_size * frames),
                         'frame': np.arange(frames).repeat(sample_size)})
    data['max_value'] = data.groupby('frame')['value'].transform('max')
    data['is_max'] = data['value'] == data['max_value']
    colors = np.where(data['is_max'], 'red', 'blue')

    fig = px.scatter(data_frame=data, x='value', y='hight', color=colors,
                     animation_frame='frame', width=800, height=300)
    fig.update_xaxes(range=[-4, 4])

    # Update the title with the current sample size
    title = f"Sample Size: {sample_size}"

    return fig, title


if __name__ == '__main__':
    app.run_server(debug=True)

