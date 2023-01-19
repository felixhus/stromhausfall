import time
import os

import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px
import source.dash_components as dash_components
import dash_mantine_components as dmc
from dash_iconify import DashIconify
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
            dash_components.add_cytoscape_grid(nodes, edges),
        ]),
        dbc.Col([
            html.Div(id='graph', style={'display': 'none'}, children=[
                dcc.Graph(figure=fig)
            ])
        ], width='auto')
    ]),
    dbc.Row([
        dbc.Col([
            dmc.Button("README", id='button_readme', n_clicks=0, style={'margin_right': '10px', 'margin_top': '10px'},
                       leftIcon=DashIconify(icon="mdi:file-document"), variant='gradient'),
            # dmc.Button("Debug", id='debug_button')
        ], width=2),
        dbc.Col([
            dbc.Stack([
                html.P("Grid elements", style={'margin-right': '10px', 'margin-top': '27px'}),
                daq.BooleanSwitch(id='menu_switch', style={'margin-top': '15px'}),
                html.P("House elements", style={'margin-left': '10px', 'margin-top': '27px'})], direction='horizontal')
        ], width=5),
        dbc.Col([
            dbc.Stack([
                html.P("Netz bearbeiten", style={'margin-right': '10px', 'margin-top': '27px'}),
                dmc.Switch(id='mode_switch', style={'margin-top': '15px'}, size="lg",
                           offLabel=DashIconify(icon="material-symbols:edit-outline"),
                           onLabel=DashIconify(icon="material-symbols:calculate-outline")),
                dbc.Spinner(html.P("Berechnen", id='calculate', style={'margin-left': '10px', 'margin-top': '27px'}))],
                direction='horizontal'),
        ], width=5),
    ], justify='evenly'),
    dash_components.add_modal_edit(),
    dash_components.add_modal_readme(),
    dash_components.add_storage_variables(),
    html.P(id='dummy'),
], id='main_container')


@app.callback(Output('cyto1', 'autoungrabify'),  # Callback to make Node ungrabbable when adding lines
              Output('line_edit_active', 'data'),
              Output('button_line', 'variant'),
              Input('button_line', 'n_clicks'),
              State('line_edit_active', 'data'),
              prevent_initial_call=True)
def edit_mode(btn_line, btn_active):
    if not btn_active:
        return True, True, 'light'
    else:
        return False, False, 'filled'


@app.callback(Output('cyto1', 'elements'),  # Callback to change elements of cyto
              Output('start_of_line', 'data'),
              Output('element_deleted', 'data'),
              Input('store_add_node', 'data'),
              Input('cyto1', 'selectedNodeData'),
              Input('modal_edit_delete_button', 'n_clicks'),
              Input('button_line', 'n_clicks'),
              State('cyto1', 'elements'),
              State('line_edit_active', 'data'),
              State('start_of_line', 'data'),
              State('selected_element', 'data'))
def edit_grid(btn_add, node, btn_delete, btn_line, elements, btn_line_active, start_of_line, selected_element):
    triggered_id = ctx.triggered_id
    if triggered_id == 'button_line':
        return elements, None, False
    if triggered_id == 'button_add':  # # Add node to grid
        last_id = get_last_id(elements)
        new_element = {'data': {'id': 'node' + str(last_id + 1), 'label': 'Node ' + str(last_id + 1)},
                       'position': {'x': 50, 'y': 50}}
        elements.append(new_element)
        return elements, start_of_line, False
    elif triggered_id == 'store_add_node':
        last_id = get_last_id(elements)
        for button in menu_objects:
            if button[0] == btn_add:
                image_src = app.get_asset_url('Icons/' + button[1])
        new_element = {'data': {'id': 'node' + str(last_id[0] + 1)}, 'position': {'x': 50, 'y': 50},
                       'classes': 'node_style', 'style': {'background-image': image_src}}
        elements.append(new_element)
        # return elements, node, False
        return elements, None, False
    elif triggered_id == 'cyto1':  # # Node was clicked
        if not node == []:
            if btn_line_active:  # Add-line-mode is on
                if start_of_line is not None:
                    last_id = get_last_id(elements)
                    new_edge = {'data': {'source': start_of_line[0]['id'], 'target': node[0]['id'],
                                         'id': 'edge' + str(last_id[1]+1)}}
                    elements.append(new_edge)
                    return elements, None, False
                else:
                    return elements, node, False
            else:  # Node is clicked in normal mode
                raise PreventUpdate
        else:
            raise PreventUpdate
    elif triggered_id == 'modal_edit_delete_button':     # Delete Object
        index = 0
        for ele in elements:
            if ele['data']['id'] == selected_element:
                break
            index += 1
        if 'position' in elements[index]:   # Check if it is node
            connected_edges = get_connected_edges(elements, elements[index])
        for edge in connected_edges:
            elements.pop(elements.index(edge))
        elements.pop(index)
        return elements, None, True
    else:
        raise PreventUpdate


@app.callback(Output('modal_edit', 'opened'),
              Output('modal_text', 'children'),
              Output('selected_element', 'data'),
              Output('cyto1', 'tapNodeData'),
              Output('cyto1', 'tapEdgeData'),
              Input('cyto1', 'tapNodeData'),
              Input('cyto1', 'tapEdgeData'),
              Input('modal_edit_close_button', 'n_clicks'),
              Input('element_deleted', 'data'),
              State('line_edit_active', 'data'),
              State('cyto1', 'elements'))
def edit_grid_element(node, edge, btn_close, element_deleted, btn_line_active, elements):
    triggered_id = ctx.triggered_id
    if triggered_id == 'element_deleted':
        if element_deleted:
            return False, None, None, None, None
        else:
            raise PreventUpdate
    elif triggered_id == 'cyto1':
        if node is not None and edge is None:
            if not btn_line_active:
                body_text = "Edit settings of " + node['id'] + " here."
                return True, body_text, node['id'], None, None
            else:
                raise PreventUpdate
        elif node is None and edge is not None:
            if not btn_line_active:
                body_text = "Edit settings of " + edge['label'] + " here."
                return True, body_text, edge['id'], None, None
            else:
                raise PreventUpdate
        else:
            return False, None, None, None, None
    elif triggered_id == 'modal_edit_close_button':
        return False, None, None, None, None
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


@app.callback(Output('modal_readme', 'opened'),
              Input('button_readme', 'n_clicks'),
              prevent_initial_call=True)
def open_readme(btn):
    return True


@app.callback(Output('dummy', 'children'),
              Input('debug_button', 'n_clicks'),
              State('cyto1', 'elements'),
              State('start_of_line', 'data'))
def debug(btn, elements, start_of_line):
    return None


def get_last_id(elements):
    last_id = [0, 0]
    for ele in elements:
        if 'source' not in ele['data']:
            last_id[0] = int(ele['data']['id'][4:])
    for ele in elements:
        if 'source' in ele['data']:
            last_id[1] = int(ele['data']['id'][4:])
    return last_id


def get_connected_edges(elements, selected_element):
    id_element = selected_element['data']['id']
    result = []
    for ele in elements:
        if 'source' in ele['data']:
            if ele['data']['source'] == id_element or ele['data']['target'] == id_element:
                result.append(ele)
    return result


if __name__ == '__main__':
    app.run_server(debug=True)
