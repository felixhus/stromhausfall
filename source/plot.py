import matplotlib.pyplot as plt
import networkx as nx
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
    # fig.update_layout(xaxis_title='Test',
    #                   yaxis_title='Leistung in W')
    return fig
