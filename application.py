import os
import time

import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_daq as daq
import dash_mantine_components as dmc
# import modules
import plotly.express as px
from dash import Dash, Input, Output, State, ctx, dcc, html, no_update
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

import source.dash_components as dash_components
import source.stylesheets as stylesheets
from source.modules import (calculate_power_flow, connection_allowed,
                            generate_grid_object, get_connected_edges,
                            get_last_id, get_object_from_id)

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
    ['button_switch_cabinet', 'icon_switch_cabinet.png'],
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
gridObject_list = []

app.layout = dmc.NotificationsProvider(dbc.Container([
    dbc.Col([
        dbc.Row(
            dash_components.dash_navbar(),
        ),
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
            ], width='auto'),
            dbc.Col([dash_components.card_side(),
                     dash_components.card_plot_graph()], width='auto')
        ]),
        dash_components.add_modal_edit(),
        dash_components.add_modal_readme(),
        dash_components.add_modal_voltage_level(),
        dash_components.add_storage_variables(),
        html.P(id='dummy')], width=True),
    html.Div(id='notification_container')
], id='main_container'))


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
              Output('store_notification', 'data'),
              Output('store_get_voltage', 'data'),
              Input('store_add_node', 'data'),
              Input('cyto1', 'selectedNodeData'),
              Input('modal_edit_delete_button', 'n_clicks'),
              Input('button_line', 'n_clicks'),
              State('cyto1', 'elements'),
              State('line_edit_active', 'data'),
              State('start_of_line', 'data'),
              State('selected_element', 'data'))
def edit_grid(btn_add, node, btn_delete, btn_line, elements,
              btn_line_active, start_of_line, selected_element):
    triggered_id = ctx.triggered_id
    if triggered_id == 'button_line':
        return elements, None, False, None, no_update
    elif triggered_id == 'store_add_node':
        last_id = get_last_id(elements)
        new_gridobject = generate_grid_object(btn_add, 'node' + str(last_id[0] + 1), 'node' + str(last_id[0] + 1))
        image_src = app.get_asset_url('Icons/' + new_gridobject.icon)
        gridObject_list.append(new_gridobject)
        new_element = {'data': {'id': 'node' + str(last_id[0] + 1)},
                       'position': {'x': 50, 'y': 50}, 'classes': 'node_style',
                       'style': {'background-image': image_src, 'background-color': new_gridobject.ui_color}}
        elements.append(new_element)
        return elements, None, False, None, no_update
    elif triggered_id == 'cyto1':  # # Node was clicked
        if not node == []:
            if btn_line_active:  # Add-line-mode is on
                if start_of_line is not None:
                    if connection_allowed(start_of_line[0]['id'], node[0]['id'], gridObject_list):
                        last_id = get_last_id(elements)
                        return_temp = no_update
                        start_object = get_object_from_id(start_of_line[0]['id'], gridObject_list)
                        end_object = get_object_from_id(node[0]['id'], gridObject_list)
                        if start_object.voltage is None and end_object.voltage is None: # Check if voltage level of connection is defined through one of the components
                            return_temp = [start_object.id, end_object.id]
                        new_edge = {'data': {'source': start_of_line[0]['id'], 'target': node[0]['id'],
                                             'id': 'edge' + str(last_id[1]+1)}, 'classes': 'line_style'}
                        elements.append(new_edge)
                        return elements, None, False, None, return_temp
                    else:
                        return elements, None, False, "notification_false_connection", no_update
                else:
                    return elements, node, False, None, no_update
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
        index = 0
        for obj in gridObject_list:         # Remove element from grid object list
            if obj.id == selected_element:
                break
            index += 1
        gridObject_list.pop(index)
        return elements, None, True, None, no_update
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
                body_text = "Edit settings of " + edge['id'] + " here."
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
              Output('calculate', 'children'),
              Output('graph_image', 'style'),
              Output('graph_image', 'src'),
              Input('mode_switch', 'checked'),
              Input('menu_switch', 'checked'),
              State('cyto1', 'elements'),
              prevent_initial_call=True)
def switch_mode(mode_switch, menu_switch, elements):
    triggered_id = ctx.triggered_id
    if triggered_id == 'menu_switch':
        if menu_switch:
            return {'display': 'none'}, {'display': 'block'}, no_update, no_update, no_update
        else:
            return {'display': 'block'}, {'display': 'none'}, no_update, no_update, no_update
    elif triggered_id == 'mode_switch':
        if mode_switch:
            format_img_src = calculate_power_flow(elements, gridObject_list)
            img_src = 'data:image/png;base64,{}'.format(format_img_src)
            return no_update, no_update, "Calculated", {'display': 'block'}, img_src
        else:
            return {'display': 'block'}, {'display': 'none'}, "Calculate", {'display': 'none'}, no_update
    else:
        raise PreventUpdate


@app.callback(Output('modal_readme', 'opened'),
              Input('button_readme', 'n_clicks'),
              prevent_initial_call=True)
def open_readme(btn):
    return True


@app.callback(Output('modal_voltage', 'opened'),
              Input('store_get_voltage', 'data'),
              Input('button_voltage_hv', 'n_clicks'),
              Input('button_voltage_lv', 'n_clicks'),
              State('cyto1', 'elements'),
              prevent_initial_call=True
              )
def modal_voltage(node_ids, button_hv, button_lv, elements):
    triggered_id = ctx.triggered_id
    if triggered_id == 'store_get_voltage':
        if node_ids is None:
            raise PreventUpdate
        return True
    elif triggered_id == 'button_voltage_hv':
        print("Oberspannung")
        for node_id in node_ids:
            obj = get_object_from_id(node_id, gridObject_list)
            if obj.object_type != "transformer":
                obj.voltage = 20000
        return False
    elif triggered_id == 'button_voltage_lv':
        print("Unterspannung")
        for node_id in node_ids:
            obj = get_object_from_id(node_id, gridObject_list)
            if obj.object_type != "transformer":
                obj.voltage = 400
        return False
    else:
        raise PreventUpdate


@app.callback(Output('notification_container', 'children'),
              Input('store_notification', 'data'))
def notification(data):
    if data is None:
        raise PreventUpdate
    elif data == 'notification_false_connection':
        notification_message = ["Kabelsalat!",
                                "Zwischen diesen beiden Komponenten kannst du keine Leitung ziehen."]
        icon = DashIconify(icon="mdi:connection")
        color = 'red'
    else:
        raise PreventUpdate
    return dmc.Notification(title=notification_message[0],
                            message=notification_message[1],
                            action='show', color=color,
                            icon=icon, id='notification')


# @app.callback(Output('dummy', 'children'),
#               Input('debug_button', 'n_clicks'),
#               State('cyto1', 'elements'),
#               State('start_of_line', 'data'),
#               prevent_initial_call=True)
# def debug(btn, elements, start_of_line):
#     calculate_power_flow(elements, gridObject_list)
#     return None


if __name__ == '__main__':
    app.run_server(debug=False)