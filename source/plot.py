import matplotlib.pyplot as plt
import networkx as nx
import plotly.express as px
import plotly.graph_objects as go

colors = {
    'color1': ''
}


def plot_graph(graph):
    nx.draw(graph)
    plt.show()


def plot_device_timeseries(timesteps, load, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name="P",
        x=timesteps,
        y=load,
        stackgroup='one',
        fillcolor=color,
        mode='none'  # this remove the lines
    ))
    fig.update_layout(template='plotly_white', margin=dict(l=0, r=0, b=0, t=0), height=200)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True,
                     rangemode='nonnegative')
    return fig
