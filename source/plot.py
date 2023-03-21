import matplotlib.pyplot as plt
import networkx as nx
import plotly.express as px
import plotly.graph_objects as go

colors = {
    'color1': 'rgb(245, 149, 178)',
    'color2': 'rgb(255, 179, 179)',
    'color3': 'rgb(255, 241, 186)',
    'color4': 'rgb(190, 227, 237)',
    'color5': 'rgb(175, 173, 222)',
}
colors = ['rgb(245, 149, 178)', 'rgb(255, 179, 179)', 'rgb(255, 241, 186)', 'rgb(190, 227, 237)', 'rgb(175, 173, 222)']


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


def plot_all_devices_room(df_devices, df_sum, device_dict):
    fig = go.Figure()
    color_index = 0
    for index, row in df_devices.iterrows():
        fig.add_trace(go.Scatter(
            name=device_dict['house1'][index]['name'],
            x=df_devices.columns,
            y=row,
            stackgroup='one',
            fillcolor=colors[color_index],
            mode='none'  # this remove the lines
        ))
        color_index += 1
        if color_index >= len(colors):
            color_index = 0
    fig.add_trace(go.Scatter(
        mode='lines',
        line=dict(color='black', width=1),
        name='total',
        x=df_sum.columns,
        y=df_sum.loc['house1']
    ))
    fig.update_layout(template='plotly_white', margin=dict(l=0, r=0, b=0, t=0), height=200)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True,
                     rangemode='nonnegative')
    fig.show()
