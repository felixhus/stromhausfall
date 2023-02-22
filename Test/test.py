import plotly.graph_objs as go

# create bar graph trace
trace_bar = go.Bar(x=[1, 2, 3, 4], y=[10, 20, 30, 40])

# create draggable points trace
trace_points = go.Scatter(x=[1, 2, 3, 4], y=[10, 20, 30, 40],
                          mode='markers', marker=dict(symbol='circle', size=10),
                          dragmode='xy')

# create figure
fig = go.Figure(data=[trace_bar, trace_points])

# update layout
fig.update_layout(title='Bar Graph with Draggable Points',
                  xaxis_title='X Axis Title',
                  yaxis_title='Y Axis Title')

# show figure
fig.show()
