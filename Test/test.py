import pandas as pd
import plotly.graph_objects as go

# create empty dataframe
df = pd.DataFrame(columns=['x', 'y', 'color'])

# add data to dataframe row by row
df = df.append({'x': 1, 'y': 10, 'color': 'red'}, ignore_index=True)
df = df.append({'x': 2, 'y': 8, 'color': 'red'}, ignore_index=True)
df = df.append({'x': 3, 'y': 6, 'color': 'red'}, ignore_index=True)
df = df.append({'x': 4, 'y': 4, 'color': 'red'}, ignore_index=True)
df = df.append({'x': 5, 'y': 2, 'color': 'red'}, ignore_index=True)

df = df.append({'x': 1, 'y': 8, 'color': 'green'}, ignore_index=True)
df = df.append({'x': 2, 'y': 6, 'color': 'green'}, ignore_index=True)
df = df.append({'x': 3, 'y': 4, 'color': 'green'}, ignore_index=True)
df = df.append({'x': 4, 'y': 2, 'color': 'green'}, ignore_index=True)
df = df.append({'x': 5, 'y': 0, 'color': 'green'}, ignore_index=True)

df = df.append({'x': 1, 'y': 12, 'color': 'blue'}, ignore_index=True)
df = df.append({'x': 2, 'y': 9, 'color': 'blue'}, ignore_index=True)
df = df.append({'x': 3, 'y': 6, 'color': 'blue'}, ignore_index=True)
df = df.append({'x': 4, 'y': 3, 'color': 'blue'}, ignore_index=True)
df = df.append({'x': 5, 'y': 0, 'color': 'blue'}, ignore_index=True)

# create figure object
fig = go.Figure()

# add filled lines for each y column in a loop
colors = df['color'].unique()
for color in colors:
    fig.add_trace(go.Scatter(
        x=df[df['color'] == color]['x'],
        y=df[df['color'] == color]['y'],
        mode='lines', fill='tozeroy',
        line=dict(color=color)
    ))

# set x and y axis labels
fig.update_layout(
    xaxis_title='X-axis',
    yaxis_title='Y-axis'
)

# show figure
fig.show()
