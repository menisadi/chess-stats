import numpy as np
import pandas as pd

import plotly.express as px

sample_size = 100
frames = 100
data = pd.DataFrame({'value': np.random.normal(size=sample_size*frames), 
                    'hight': np.random.uniform(size=sample_size*frames),
                    'frame': np.arange(frames).repeat(sample_size)})
data['max_value'] = data.groupby('frame')['value'].transform('max')
data['is_max'] = data['value'] == data['max_value']
colors = np.where(data['is_max'], 'red', 'blue')

fig = px.scatter(data_frame=data, x='value', y='hight', color=colors,
                 animation_frame='frame', width=800, height=300)
fig.update_xaxes(range=[-4,4])

fig.write_html("scatter.html")

# fig.show()
