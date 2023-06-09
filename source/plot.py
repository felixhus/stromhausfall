"""
plot.py contains different functions to plot data in different graph types.
"""

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

colors = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd', '#ccebc5', '#ffed6f']


def plot_device_timeseries(timesteps, load, color):
    """
    Creates the figure to plot the power profile of a device.

    :param timesteps: List with timesteps to plot
    :param load: Timeseries of device power
    :param color: Color of plot
    :type color: color
    :return: Figure
    """

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name="P",
        x=timesteps,
        y=load,
        stackgroup='one',
        line_shape='hv',
        fillcolor=color,
        mode='none'  # this remove the lines
    ))
    fig.update_layout(template='plotly_white', margin=dict(l=0, r=0, b=0, t=0), height=200)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True,
                     rangemode='nonnegative')
    return fig


def plot_pv_timeseries(timesteps, power, color):
    """
    Creates figure to display the infeed solar power. The power is inverted to positive for the graph.

    :param timesteps: List with timesteps to plot
    :param power: Timeseries of infeed pv power
    :param color: Color of plot
    :type color: color
    :return: Figure
    """

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
    """
    Creates the figure to plot the power profile of a house.

    :param power: Timeseries of house power
    :type power: list[int]
    :param color: Color of plot
    :type color: color
    :return: Figure
    """

    tick_text = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    tick_values = [720, 2160, 3600, 5040, 6480, 7920, 9360]
    timesteps = np.linspace(0, len(power), num=len(power), endpoint=False)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name="P",
        x=timesteps,
        y=power,
        stackgroup='one',
        line_shape='hv',
        fillcolor=color,
        mode='none'  # this remove the lines
    ))
    fig.update_layout(template='plotly_white', margin=dict(l=0, r=0, b=0, t=0), height=200)
    fig.update_layout(xaxis=dict(tickmode='array', tickvals=tick_values, ticktext=tick_text))
    fig.update_xaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True,
                     rangemode='nonnegative')
    # pic = pio.to_image(fig, format='png')
    return fig


def plot_grid_results(df_power):
    """
    Creates the figure to plot the power results of the grid.

    :param df_power: Timeseries of house power
    :type df_power: list[int]
    :return: Figure
    """

    tick_text = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    tick_values = [720, 2160, 3600, 5040, 6480, 7920, 9360]
    timesteps = np.linspace(0, len(df_power['generator']), num=len(df_power['generator']), endpoint=False)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name="Last",
        x=timesteps,
        y=df_power['non_generator'],
        fillcolor='rgba(64, 130, 109, 1)',
        fill='tozeroy',
        mode='none'  # this remove the lines
    ))
    fig.add_trace(go.Scatter(
        name="PV",
        x=timesteps,
        y=df_power['generator'],
        fillcolor='rgba(255, 248, 94, 0.7)',
        fill='tozeroy',
        mode='none'  # this remove the lines
    ))
    fig.add_trace(go.Scatter(
        name="Residual",
        x=timesteps,
        y=df_power['residual'],
        line=dict(color="#ff0000", width=0.75),
        visible='legendonly'
    ))
    fig.add_shape(type="line",
                  x0=0, y0=0, x1=0, y1=df_power.max().max(),
                  line=dict(color="RoyalBlue", width=1)
                  )
    fig.update_layout(xaxis_range=[0, len(df_power['generator'])])
    fig.update_layout(template='plotly_white', margin=dict(l=0, r=0, b=0, t=0), height=200)
    fig.update_layout(xaxis=dict(tickmode='array', tickvals=tick_values, ticktext=tick_text))
    fig.update_xaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True)

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5,
            bgcolor="white",
            bordercolor="gray",
            borderwidth=1,
            itemwidth=30,  # set the width of each legend item
            font={'size': 8},
        ),
        showlegend=True
    )

    return fig



def plot_all_devices_room(df_devices, df_sum, df_energy, device_dict):
    """
    Creates plots from the results of the house calculation.

    * Plot 1: Stacked scatter plot of the power timeseries of all devices
    * Plot 2: Sunburst plot showing the energy use of each room and devices in the rooms

    :param df_devices: Dataframe with power timeseries of each device
    :type df_devices: dataframe
    :param df_sum: Dataframe with sum of power for each room and house
    :type df_sum: dataframe
    :param df_energy: Dataframe with used energy of devices, rooms and house
    :type df_energy: dataframe
    :param device_dict: Dictionary containing all devices in the custom house
    :type device_dict: dict
    :return: figure scatter plot; figure sunburst plot
    """

    tick_text = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    tick_values = [720, 2160, 3600, 5040, 6480, 7920, 9360]
    fig = go.Figure()   # Create scatter plot
    color_index = 0
    for index, row in df_devices.iterrows():
        fig.add_trace(go.Scatter(
            name=device_dict['house1'][index]['name'],
            x=df_devices.columns,
            y=row,
            stackgroup='one',
            fillcolor=colors[color_index],
            # TODO: Add more colors
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
    fig.update_layout(xaxis_range=[0, len(df_sum.columns)], template='plotly_white', margin=dict(l=0, r=0, b=0, t=0), width=320, height=320)
    fig.update_layout(xaxis=dict(tickmode='array', tickvals=tick_values, ticktext=tick_text))
    fig.update_xaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='rgb(173, 174, 179)', mirror=True,
                     rangemode='nonnegative')
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5,
            bgcolor="white",
            bordercolor="gray",
            borderwidth=1,
            itemwidth=30,  # set the width of each legend item
            font={'size': 8},
        ),
        showlegend=False
    )

    # Set multiplicator for sunburst plot to get yearly consumption from week
    multiplicator_kwh = 52
    # Create labels, parents and values for sunburst plot
    color_index = 0
    sunburst_labels, sunburst_parents, sunburst_values, sunburst_colors = [], [], [], []
    sunburst_labels.append('Mein Haus')
    sunburst_parents.append('')
    sunburst_values.append(df_energy.loc['house1']['energy'])
    sunburst_colors.append('#ffffff')
    for room in device_dict['rooms']:
        sunburst_labels.append(device_dict['rooms'][room]['name'])
        sunburst_parents.append('Mein Haus')
        sunburst_values.append(df_energy.loc[room]['energy'])
        sunburst_colors.append('#ffffff')
        for device in device_dict['rooms'][room]['devices']:
            sunburst_labels.append(device_dict['house1'][device]['name'])
            sunburst_parents.append(device_dict['rooms'][room]['name'])
            sunburst_values.append(df_energy.loc[device]['energy'])
            sunburst_colors.append(colors[color_index])
            color_index += 1

    # Multiply each value with the multiplicator
    sunburst_values = [value * multiplicator_kwh for value in sunburst_values]

    fig_sunburst = go.Figure(go.Sunburst(   # Create sunburst plot
        labels=sunburst_labels,
        parents=sunburst_parents,
        values=sunburst_values,
        branchvalues='total',
        marker=dict(colors=sunburst_colors, line=dict(color='#000000'))
    ))
    # Update layout for tight margin
    # See https://plotly.com/python/creating-and-updating-figures/
    fig_sunburst.update_layout(margin=dict(t=0, l=0, r=0, b=0), width=320)

    return fig, fig_sunburst
