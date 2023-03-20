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
    # fig = px.(
    #     template='plotly_white'
    # )
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name="P",
        x=timesteps,
        y=load,
        stackgroup='one',
        fillcolor=color,
        mode='none'  # this remove the lines
    ))
    fig.update_layout(template='plotly_white')
    return fig
