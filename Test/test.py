import numpy as np
import plotly.graph_objs as go

# Generate random data
np.random.seed(1)
y = np.random.randint(2500, size=96)

# Create the bar plot
data = [
    go.Bar(
        x=list(range(96)),
        y=y,
        # marker=dict(
            # color='rgb(50, 171, 96)',
        #     line=dict(
        #         color='rgb(0, 0, 0)',
        #         width=1.5),
        # ),
        opacity=0.8,
        width=1,
    )
]

# Set layout options
layout = go.Layout(
    title='24-Hour Power Usage',
    xaxis=dict(
        title='Timestep',
        tickvals=list(range(96)),
        ticktext=[f'{i:02d}:00' for i in range(24)]*4,
    ),
    yaxis=dict(
        title='W',
    ),
    bargap=0,
    template='seaborn',
)

# Create the figure object
fig = go.Figure(data=data, layout=layout)

# Display the plot
fig.show()
