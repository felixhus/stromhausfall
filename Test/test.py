import dash
import dash_html_components as html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

app = dash.Dash(__name__)

badges = [["Badge 1", "2,50€", "tabler:pig-money"], ["Badge 2", "2,50€", "tabler:pig-money"],
          ["Badge 3", "2,50€", "tabler:pig-money"], ["Badge 4", "2,50€", "tabler:pig-money"],
          ["Badge 5", "3,50€", "tabler:pig-money"], ["Badge 6", "2,50€", "tabler:pig-money"],]


def cost_badge(name, cost, icon):
    return dmc.Tooltip(
        label=name,
        position='bottom', transition='slide-down', transitionDuration=300, closeDelay=500,
        color='gray',
        children=[
            html.Div(children=[
                dmc.ThemeIcon(
                    size=60,
                    color="indigo",
                    variant="filled",
                    children=DashIconify(icon=icon, width=40),
                ),
                html.Br(),
                dmc.Badge(
                    cost
                )
            ], style={'margin-left': 10, 'margin-bottom': 10})
        ])


app.layout = dmc.Card(children=[
    dmc.Grid(children=[
        cost_badge(element[0], element[1], element[2])
        for element in badges
    ], gutter='lg')
], style={'width': 250})

if __name__ == '__main__':
    app.run_server(debug=True)
