import plotly.graph_objects as go

# create a sample figure with lots of legend entries
fig = go.Figure()
for i in range(20):
    fig.add_trace(go.Scatter(x=[i], y=[i], name=f"Trace {i}"))

# update the layout to place the legend in a box below the plot
fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
        bgcolor="white",
        bordercolor="gray",
        borderwidth=1,
        itemwidth=80,  # set the width of each legend item
    ),
)

# display the figure
fig.show()
