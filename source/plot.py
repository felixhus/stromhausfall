import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

colors = ['rgb(245, 149, 178)', 'rgb(255, 179, 179)', 'rgb(255, 241, 186)', 'rgb(190, 227, 237)', 'rgb(175, 173, 222)']


def plot_graph(graph):
    nx.draw(graph)
    plt.show()


def empty_figure():
    return go.Figure()


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


def plot_pv_timeseries(timesteps, power, color):
    tick_text = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    tick_values = [12, 36, 60, 84, 106, 130, 154]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name="P",
        x=timesteps,
        y=[-i for i in power],     # Invert power for plot
        stackgroup='one',
        fillcolor=color,
        mode='none'  # this remove the lines
    ))
    fig.update_layout(template='plotly_white', margin=dict(l=0, r=0, b=0, t=0), height=200)
    fig.update_layout(xaxis=dict(tickmode='array', tickvals=tick_values, ticktext=tick_text))
    fig.update_xaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True,
                     rangemode='nonnegative')
    return fig


def plot_house_timeseries(power, color):
    tick_text = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    tick_values = [720, 2160, 3600, 5040, 6480, 7920, 9360]
    power = power
    timesteps = np.linspace(0, len(power), num=len(power), endpoint=False)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name="P",
        x=timesteps,
        y=power,     # Invert power for plot
        stackgroup='one',
        fillcolor=color,
        mode='none'  # this remove the lines
    ))
    fig.update_layout(template='plotly_white', margin=dict(l=0, r=0, b=0, t=0), height=200)
    fig.update_layout(xaxis=dict(tickmode='array', tickvals=tick_values, ticktext=tick_text))
    fig.update_xaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True,
                     rangemode='nonnegative')
    return fig


def plot_all_devices_room(df_devices, df_sum, df_energy, device_dict):
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
        line=dict(color='black', width=0.5),
        name='total',
        x=df_sum.columns,
        y=df_sum.loc['house1']
    ))
    fig.update_layout(template='plotly_white', margin=dict(l=0, r=0, b=0, t=0), width=320)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True,
                     rangemode='nonnegative')
    fig.update_layout(legend=dict(
        # orientation="h",
        # entrywidth=70,
        yanchor="top",
        y=-0.25,
        xanchor="left",
        x=0
    ))
    # fig.show()

    sunburst_labels, sunburst_parents, sunburst_values = [], [], []
    sunburst_labels.append('house1')
    sunburst_parents.append('')
    sunburst_values.append(df_energy.loc['house1']['energy'])
    for room in device_dict['rooms']:
        sunburst_labels.append(room)
        sunburst_parents.append('house1')
        sunburst_values.append(df_energy.loc[room]['energy'])
        for device in device_dict['rooms'][room]:
            sunburst_labels.append(device)
            sunburst_parents.append(room)
            sunburst_values.append(df_energy.loc[device]['energy'])

    fig_sunburst = go.Figure(go.Sunburst(
        labels=sunburst_labels,
        parents=sunburst_parents,
        values=sunburst_values,
        branchvalues='total'
    ))
    # Update layout for tight margin
    # See https://plotly.com/python/creating-and-updating-figures/
    fig_sunburst.update_layout(margin=dict(t=0, l=0, r=0, b=0), width=320)

    return fig, fig_sunburst
    # fig_sunburst.show()
