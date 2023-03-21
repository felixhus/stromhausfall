import pandas as pd
import plotly.graph_objects as go

# create sample dataframe
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y1': [10, 8, 6, 4, 2],
    'y2': [8, 6, 4, 2, 0],
    'y3': [12, 9, 6, 3, 0]
})

# create figure object
fig = go.Figure()

# add filled lines for each y column
fig.add_trace(go.Scatter(
    x=df['x'], y=df['y1'],
    mode='lines', fill='tozeroy',
    line=dict(color='red')
))
fig.add_trace(go.Scatter(
    x=df['x'], y=df['y2'],
    mode='lines', fill='tozeroy',
    line=dict(color='green')
))
fig.add_trace(go.Scatter(
    x=df['x'], y=df['y3'],
    mode='lines', fill='tozeroy',
    line=dict(color='blue')
))

# set x and y axis labels
fig.update_layout(
    xaxis_title='X-axis',
    yaxis_title='Y-axis'
)

# show figure
fig.show()
