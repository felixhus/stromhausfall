import time
import os

import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px
import source.dash_components as dash_components
import source.stylesheets as stylesheets
import dash_cytoscape as cyto
from dash import Dash, Input, Output, State, ctx, dcc, html
from dash.exceptions import PreventUpdate

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
server = app.server
df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length')

menu_objects = [
    ['button_house', 'icon_house2.png'],
    ['button_transformer', 'icon_transformer.png'],
    ['button_externalgrid', 'icon_powerplant.png'],
    ['button_pv', 'icon_pv.png'],
    ['button_battery', 'icon_battery.png'],
    ['button_smartmeter', 'icon_meter.png'],
    ['button_line', 'icon_line_lv.png'],
]

house_objects = [
    ['button_dryer', "Föhn"],
    ['button_fridge', "Kühlschrank"],
    ['button_lamp', "Lampe"],
    ['button_stove', "Herd"],
    ['button_tv', "TV"],
]

nodes = []
edges = []

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Row(dash_components.add_grid_object_button(object_id=menu_objects[i][0],
                                                               icon=app.get_asset_url('Icons/' + menu_objects[i][1])))
                for i in range(len(menu_objects))
            ], id='grid_buttons', style={'display': 'block'}),
            html.Div([
                dbc.Row(dash_components.add_grid_object_button(object_id=house_objects[i][0],
                                                               name=house_objects[i][1]))
                for i in range(len(house_objects))
            ], id='house_buttons', style={'display': 'none'}),
        ], width='auto'),
        dbc.Col([
            dash_components.add_cytoscape_grid(nodes, edges)
        ]),
        dbc.Col([
            html.Div(id='graph', style={'display': 'none'}, children=[
                dcc.Graph(figure=fig)
            ])
        ], width='auto')
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Button("README", id='button_readme', n_clicks=0, style={'margin_right': '10px', 'margin_top': '10px'})
        ], width=2),
        dbc.Col([
            dbc.Stack([
                html.P("Grid elements", style={'margin-right': '10px', 'margin-top': '27px'}),
                daq.BooleanSwitch(id='menu_switch', on=False, style={'margin-top': '15px'}),
                html.P("House elements", style={'margin-left': '10px', 'margin-top': '27px'})], direction='horizontal')
        ], width=5),
        dbc.Col([
            dbc.Stack([
                html.P("Edit Grid", style={'margin-right': '10px', 'margin-top': '27px'}),
                daq.BooleanSwitch(id='mode_switch', on=False, style={'margin-top': '15px'}),
                dbc.Spinner(html.P("Calculate", id='calculate', style={'margin-left': '10px', 'margin-top': '27px'}))],
                direction='horizontal'),
        ], width=5),
    ], justify='evenly'),
    dash_components.add_modal_edit(),
    dash_components.add_modal_readme(),
    dash_components.add_storage_variables(),
    html.P(id='dummy')
])


@app.callback(Output('cyto1', 'autoungrabify'),  # Callback to make Node ungrabbable when adding lines
              Output('button_line', 'active'),
              Output('button_line', 'color'),
              Input('button_line', 'n_clicks'),
              State('button_line', 'active'),
              prevent_initial_call=True)
def edit_mode(btn_line, btn_active):
    if not btn_active:
        return True, True, 'info'
    else:
        return False, False, 'primary'


@app.callback(Output('cyto1', 'elements'),  # Callback to change elements of cyto
              Output('start_of_line', 'data'),
              Input('store_add_node', 'data'),
              Input('cyto1', 'selectedNodeData'),
              State('cyto1', 'elements'),
              State('button_line', 'active'),
              State('start_of_line', 'data'))
def edit_grid(btn_add, node, elements, btn_line_active, start_of_line):
    triggered_id = ctx.triggered_id
    if triggered_id == 'button_add':  # # Add node to grid
        last_id = get_last_id(elements)
        new_element = {'data': {'id': 'node' + str(last_id + 1), 'label': 'Node ' + str(last_id + 1)},
                       'position': {'x': 50, 'y': 50}}
        elements.append(new_element)
        return elements, start_of_line
    elif triggered_id == 'store_add_node':
        last_id = get_last_id(elements)
        for button in menu_objects:
            if button[0] == btn_add:
                image_src = app.get_asset_url('Icons/' + button[1])
        new_element = {'data': {'id': 'node' + str(last_id + 1)}, 'position': {'x': 50, 'y': 50},
                       'classes': 'node_style', 'style': {'background-image': image_src}}
        elements.append(new_element)
        return elements, node
    elif triggered_id == 'cyto1':  # # Node was clicked
        if not node == []:
            if btn_line_active:  # Add-line-mode is on
                if start_of_line is not None:
                    new_edge = {'data': {'source': start_of_line[0]['id'], 'target': node[0]['id'], 'label': 'Edge1'}}
                    elements.append(new_edge)
                    return elements, None
                else:
                    return elements, node
            else:  # Node is clicked in normal mode
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(Output('modal', 'is_open'),
              Output('modal_body', 'children'),
              Input('cyto1', 'selectedNodeData'),
              Input('close_modal', 'n_clicks'),
              State('button_line', 'active'))
def edit_grid_element(node, btn_close, btn_line_active):
    triggered_id = ctx.triggered_id
    if triggered_id == 'cyto1':
        if not node == []:
            if not btn_line_active:
                body_text = "Edit settings of " + node[0]['id'] + " here."
                return True, body_text
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    elif triggered_id == 'close_modal':
        return False, ""
    else:
        raise PreventUpdate


@app.callback(Output('store_add_node', 'data'),
              [Input(object_id[0], 'n_clicks') for object_id in menu_objects],
              prevent_initial_call=True)
def button_add_pressed(*args):
    triggered_id = ctx.triggered_id
    if triggered_id == 'button_line':
        raise PreventUpdate
    else:
        return triggered_id


@app.callback(Output('grid_buttons', 'style'),
              Output('house_buttons', 'style'),
              Output('graph', 'style'),
              Output('calculate', 'children'),
              Input('mode_switch', 'on'),
              Input('menu_switch', 'on'),
              State('grid_buttons', 'style'),
              State('house_buttons', 'style'),
              State('graph', 'style'),
              State('calculate', 'children'),
              prevent_initial_call=True)
def switch_mode(mode_switch, menu_switch, state_grid, state_house, state_graph, state_spinner):
    triggered_id = ctx.triggered_id
    if triggered_id == 'menu_switch':
        if menu_switch:
            return {'display': 'none'}, {'display': 'block'}, state_graph, state_spinner
        else:
            return {'display': 'block'}, {'display': 'none'}, state_graph, state_spinner
    elif triggered_id == 'mode_switch':
        if mode_switch:
            time.sleep(2)
            return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, "Calculated"
        else:
            return {'display': 'block'}, state_house, {'display': 'none'}, "Calculate"
    else:
        raise PreventUpdate


@app.callback(Output('modal_readme', 'is_open'),
              Input('button_readme', 'n_clicks'),
              prevent_initial_call=True)
def open_readme(btn):
    return True


def get_last_id(elements):
    last_id = 0
    for ele in elements:
        if 'source' not in ele['data']:
            last_id = int(ele['data']['id'][4:])
    return last_id


@app.callback(Output('dummy', 'children'),
              Input('cyto1', 'cxttap'))
def dummy_callback(input):
    print("success")
    return ""


if __name__ == '__main__':
    app.run_server(debug=True)
